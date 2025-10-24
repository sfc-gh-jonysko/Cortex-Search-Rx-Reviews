 CREATE OR REPLACE STAGE demo.public.rx_reviews
    DIRECTORY = (ENABLE = TRUE)
    ENCRYPTION = (TYPE = 'SNOWFLAKE_SSE');
    
    CREATE OR REPLACE TABLE demo.public.rx_raw_text AS
SELECT
    RELATIVE_PATH,
    TO_VARCHAR (
        SNOWFLAKE.CORTEX.PARSE_DOCUMENT (
            '@demo.public.rx_reviews',
            RELATIVE_PATH,
            {'mode': 'LAYOUT'} )
        ) AS EXTRACTED_LAYOUT
FROM
    DIRECTORY('@demo.public.rx_reviews')
WHERE
    RELATIVE_PATH LIKE '%.pdf';

SELECT * FROM RX_RAW_TEXT;

-- Parse customer review text and create chunks with header concatenated to each paragraph
create
or replace table demo.public.rx_review_chunks as WITH review_data AS (
    SELECT
        relative_path,
        extracted_layout AS json_data
    FROM
        demo.public.RX_RAW_TEXT
),
parsed_content AS (
    SELECT
        relative_path,
        PARSE_JSON(json_data):content::STRING AS content,
        -- Extract header by removing the "# " prefix and getting everything before the first double newline
        REGEXP_SUBSTR(
            PARSE_JSON(json_data):content::STRING,
            '^# (.+?)\\n\\n',
            1,
            1,
            'e',
            1
        ) AS header,
        -- Get the main content after the header (everything after first double newline)
        REGEXP_SUBSTR(
            PARSE_JSON(json_data):content::STRING,
            '\\n\\n(.+)$',
            1,
            1,
            's',
            1
        ) AS main_content
    FROM
        review_data
),
paragraphs AS (
    SELECT
        relative_path,
        header,
        main_content,
        -- Split main content into paragraphs using double newlines as delimiter
        TRIM(para.value::STRING) AS paragraph,
        para.index AS paragraph_number
    FROM
        parsed_content,
        LATERAL FLATTEN(SPLIT(main_content, '\n\n')) para
    WHERE
        TRIM(para.value::STRING) != ''
),
header_paragraph_combined AS (
    SELECT
        relative_path,
        header,
        paragraph_number,
        -- Concatenate header with each paragraph
        header || ' - ' || paragraph AS combined_text
    FROM
        paragraphs
)
SELECT
    relative_path,
    BUILD_SCOPED_FILE_URL(@demo.public.rx_reviews, relative_path) AS file_url,
    --header,
    --paragraph_number,
    --combined_text,
    -- Split each header+paragraph combination into chunks
    chunk.value::STRING AS chunk,
    'English' as language
FROM
    header_paragraph_combined,
    LATERAL FLATTEN(
        SNOWFLAKE.CORTEX.SPLIT_TEXT_RECURSIVE_CHARACTER(
            combined_text,
            'none',
            1000,
            -- chunk size of 1000 characters
            100 -- 100 character overlap between chunks
        )
    ) chunk;

select * from demo.public.rx_review_chunks order by 1;

CREATE OR REPLACE CORTEX SEARCH SERVICE demo.public.rx_reviews
    ON chunk
    ATTRIBUTES language
    WAREHOUSE = WH_XSMALL
    TARGET_LAG = '1 hour'
    AS (
    SELECT
        chunk,
        relative_path,
        file_url,
        language
    FROM demo.public.rx_review_chunks
);
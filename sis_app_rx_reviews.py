import streamlit as st
from snowflake.core import Root # requires snowflake>=0.8.0
from snowflake.cortex import Complete
from snowflake.snowpark.context import get_active_session

# CVS Health color scheme
CVS_RED = "#CC0000"
CVS_DARK_RED = "#B30000"
CVS_LIGHT_RED = "#FF3333"
CVS_WHITE = "#FFFFFF"
CVS_GRAY = "#F5F5F5"
CVS_DARK_GRAY = "#666666"

# CVS Health Logo URL
CVS_LOGO_URL = "https://www.cvshealth.com/content/dam/enterprise/cvs-enterprise/media-library/logos/2024/CVS_Health_logo_h_reg_rgb_redblk.png/jcr:content/renditions/cq5dam.web.1280.1280.png"

MODELS = [
    "mistral-large2",
    "llama3.1-70b",
    "llama3.1-8b",
]

# Sample questions for CVS Health context
SAMPLE_QUESTIONS = [
    "What are CVS Health's pharmacy services?",
    "How can I find information about prescription benefits?",
    "What wellness programs does CVS Health offer?",
    "How do I schedule a health screening?",
    "What are the coverage options for preventive care?",
    "How can I access telehealth services?",
    "What mental health resources are available?",
    "How do I find in-network providers?",
    "What are the prescription drug formularies?",
    "How can I manage chronic conditions effectively?"
]

# Page configuration
st.set_page_config(
    page_title="CVS Health Assistant",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def load_cvs_css():
    """Load CVS Health branded CSS styling"""
    st.markdown(f"""
    <style>
    /* Import professional fonts */
    @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&family=Roboto:wght@400;500;700&display=swap');
    
    /* Main app styling */
    .main {{
        background-color: {CVS_WHITE};
        font-family: 'Open Sans', sans-serif;
    }}
    
    /* Header styling */
    .cvs-header {{
        background: linear-gradient(135deg, {CVS_WHITE} 0%, {CVS_GRAY} 100%);
        padding: 2.5rem 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        text-align: center;
        border: 1px solid #E0E0E0;
    }}
    
    .cvs-logo-container {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 1.5rem;
    }}
    
    .cvs-logo-img {{
        max-width: 300px;
        height: auto;
        margin: 0 auto;
    }}
    
    .cvs-tagline {{
        color: {CVS_RED};
        font-size: 1.5rem;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        font-family: 'Roboto', sans-serif;
    }}
    
    .cvs-subtitle {{
        color: {CVS_DARK_GRAY};
        font-size: 1.1rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }}
    
    /* Sample questions styling */
    .sample-questions {{
        background-color: {CVS_GRAY};
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        border-left: 4px solid {CVS_RED};
    }}
    
    .sample-questions h3 {{
        color: {CVS_RED};
        font-family: 'Roboto', sans-serif;
        margin-top: 0;
        font-size: 1.3rem;
    }}
    
    .question-button {{
        background-color: {CVS_WHITE};
        color: {CVS_RED};
        border: 2px solid {CVS_RED};
        border-radius: 20px;
        padding: 0.5rem 1rem;
        margin: 0.3rem;
        font-size: 0.9rem;
        cursor: pointer;
        transition: all 0.3s ease;
        display: inline-block;
        text-decoration: none;
    }}
    
    .question-button:hover {{
        background-color: {CVS_RED};
        color: {CVS_WHITE};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(204, 0, 0, 0.2);
    }}
    
    /* Sidebar styling */
    .css-1d391kg {{
        background-color: {CVS_GRAY};
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {CVS_RED};
        color: {CVS_WHITE};
        border: none;
        border-radius: 8px;
        font-family: 'Open Sans', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid {CVS_RED};
    }}
    
    .stButton > button:hover {{
        background-color: {CVS_DARK_RED};
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(204, 0, 0, 0.3);
    }}
    
    /* Chat message styling */
    .stChatMessage {{
        background-color: {CVS_WHITE};
        border: 1px solid #E0E0E0;
        border-radius: 10px;
        margin: 0.5rem 0;
    }}
    
    /* Chat input styling */
    .stChatInput > div > div > textarea {{
        border: 2px solid {CVS_RED};
        border-radius: 10px;
        font-family: 'Open Sans', sans-serif;
    }}
    
    .stChatInput > div > div > textarea:focus {{
        border-color: {CVS_DARK_RED};
        box-shadow: 0 0 0 3px rgba(204, 0, 0, 0.1);
    }}
    
    /* Selectbox styling */
    .stSelectbox > div > div > div {{
        border: 2px solid {CVS_RED};
        border-radius: 8px;
    }}
    
    /* Number input styling */
    .stNumberInput > div > div > input {{
        border: 2px solid {CVS_RED};
        border-radius: 8px;
    }}
    
    /* Toggle styling */
    .stToggle > div > div > div > div {{
        background-color: {CVS_RED};
    }}
    
    /* Sidebar headers */
    .sidebar-header {{
        background-color: {CVS_RED};
        color: {CVS_WHITE};
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        text-align: center;
        font-weight: 600;
    }}
    
    /* Heart icon styling */
    .heart-icon {{
        color: {CVS_RED};
        font-size: 1.2rem;
        margin-right: 0.5rem;
    }}
    
    /* Hide Streamlit branding */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header {{visibility: hidden;}}
    
    /* References table styling */
    .references-table {{
        background-color: {CVS_GRAY};
        padding: 1rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 4px solid {CVS_RED};
    }}
    
    </style>
    """, unsafe_allow_html=True)

def create_cvs_header():
    """Create CVS Health branded header with logo"""
    st.markdown(f"""
    <div class="cvs-header">
        <div class="cvs-logo-container">
            <img src="{CVS_LOGO_URL}" alt="CVS Health" class="cvs-logo-img">
        </div>
        <p class="cvs-tagline">AI-Powered Health Assistant</p>
        <p class="cvs-subtitle">Your partner in health, wellness, and pharmacy services</p>
    </div>
    """, unsafe_allow_html=True)

def display_sample_questions():
    """Display sample questions to help users get started"""
    st.markdown("""
    <div class="sample-questions">
        <h3>💡 Try asking about:</h3>
        <p>Click on any question below to get started, or type your own question in the chat!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for better layout
    cols = st.columns(2)
    
    for i, question in enumerate(SAMPLE_QUESTIONS):
        col = cols[i % 2]
        with col:
            if st.button(question, key=f"sample_q_{i}", help="Click to ask this question"):
                # Add the question to session state to be processed
                st.session_state.sample_question = question
                st.rerun()

def init_messages():
    """
    Initialize the session state for chat messages. If the session state indicates that the
    conversation should be cleared or if the "messages" key is not in the session state,
    initialize it as an empty list.
    """
    if st.session_state.clear_conversation or "messages" not in st.session_state:
        st.session_state.messages = []

def init_service_metadata():
    """
    Initialize the session state for cortex search service metadata. Query the available
    cortex search services from the Snowflake session and store their names and search
    columns in the session state.
    """
    if "service_metadata" not in st.session_state:
        services = session.sql("SHOW CORTEX SEARCH SERVICES;").collect()
        service_metadata = []
        if services:
            for s in services:
                svc_name = s["name"]
                svc_search_col = session.sql(
                    f"DESC CORTEX SEARCH SERVICE {svc_name};"
                ).collect()[0]["search_column"]
                service_metadata.append(
                    {"name": svc_name, "search_column": svc_search_col}
                )

        st.session_state.service_metadata = service_metadata

def init_config_options():
    """
    Initialize the configuration options in the Streamlit sidebar with CVS Health branding.
    """
    st.markdown("""
    <div class="sidebar-header">
        <h3>⚙️ Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.selectbox(
        "Select cortex search service:",
        [s["name"] for s in st.session_state.service_metadata],
        key="selected_cortex_search_service",
    )

    st.button("🗑️ Clear conversation", key="clear_conversation")
    st.toggle("🔍 Debug mode", key="debug", value=False)
    st.toggle("💬 Use chat history", key="use_chat_history", value=True)

    with st.expander("🔧 Advanced Options"):
        st.selectbox("AI Model:", MODELS, key="model_name")
        st.number_input(
            "Number of context chunks",
            value=5,
            key="num_retrieved_chunks",
            min_value=1,
            max_value=30,
        )
        st.number_input(
            "Chat history messages",
            value=5,
            key="num_chat_messages",
            min_value=1,
            max_value=10,
        )

    if st.session_state.debug:
        with st.expander("🔍 Debug Info"):
            st.write(st.session_state)

def query_cortex_search_service(query, columns = [], filter={}):
    """
    Query the selected cortex search service with the given query and retrieve context documents.
    Display the retrieved context documents in the sidebar if debug mode is enabled. Return the
    context documents as a string.
    """
    db, schema = session.get_current_database(), session.get_current_schema()

    cortex_search_service = (
        root.databases[db]
        .schemas[schema]
        .cortex_search_services[st.session_state.selected_cortex_search_service]
    )

    context_documents = cortex_search_service.search(
        query, columns=columns, filter=filter, limit=st.session_state.num_retrieved_chunks
    )
    results = context_documents.results

    service_metadata = st.session_state.service_metadata
    search_col = [s["search_column"] for s in service_metadata
                    if s["name"] == st.session_state.selected_cortex_search_service][0].lower()

    context_str = ""
    for i, r in enumerate(results):
        context_str += f"Context document {i+1}: {r[search_col]} \n" + "\n"

    if st.session_state.debug:
        st.sidebar.text_area("📄 Context Documents", context_str, height=500)

    return context_str, results

def get_chat_history():
    """
    Retrieve the chat history from the session state limited to the number of messages specified
    by the user in the sidebar options.
    """
    start_index = max(
        0, len(st.session_state.messages) - st.session_state.num_chat_messages
    )
    return st.session_state.messages[start_index : len(st.session_state.messages) - 1]

def complete(model, prompt):
    """
    Generate a completion for the given prompt using the specified model.
    """
    return Complete(model, prompt).replace("$", "\$")

def make_chat_history_summary(chat_history, question):
    """
    Generate a summary of the chat history combined with the current question to extend the query
    context. Use the language model to generate this summary.
    """
    prompt = f"""
        [INST]
        Based on the chat history below and the question, generate a query that extend the question
        with the chat history provided. The query should be in natural language.
        Answer with only the query. Do not add any explanation.

        <chat_history>
        {chat_history}
        </chat_history>
        <question>
        {question}
        </question>
        [/INST]
    """

    summary = complete(st.session_state.model_name, prompt)

    if st.session_state.debug:
        st.sidebar.text_area(
            "💭 Chat History Summary", summary.replace("$", "\$"), height=150
        )

    return summary

def create_prompt(user_question):
    """
    Create a prompt for the language model by combining the user question with context retrieved
    from the cortex search service and chat history (if enabled). Format the prompt according to
    the expected input format of the model with CVS Health context.
    """
    if st.session_state.use_chat_history:
        chat_history = get_chat_history()
        if chat_history != []:
            question_summary = make_chat_history_summary(chat_history, user_question)
            prompt_context, results = query_cortex_search_service(
                question_summary,
                columns=["chunk", "file_url", "relative_path"],
                filter={"@and": [{"@eq": {"language": "English"}}]},
            )
        else:
            prompt_context, results = query_cortex_search_service(
                user_question,
                columns=["chunk", "file_url", "relative_path"],
                filter={"@and": [{"@eq": {"language": "English"}}]},
            )
    else:
        prompt_context, results = query_cortex_search_service(
            user_question,
            columns=["chunk", "file_url", "relative_path"],
            filter={"@and": [{"@eq": {"language": "English"}}]},
        )
        chat_history = ""

    prompt = f"""
            [INST]
            You are a helpful CVS Health AI assistant with access to comprehensive health information.
            When a user asks you a question, you will be provided with context between <context> and </context> tags.
            Use that context with the user's chat history provided between <chat_history> and </chat_history> tags
            to provide accurate, helpful responses focused on health, wellness, pharmacy services, and healthcare benefits.

            Always prioritize:
            - Patient safety and well-being
            - Accurate health information
            - CVS Health services and programs
            - Preventive care and wellness
            - Accessible healthcare solutions

            If the user asks a question that cannot be answered with the given context or is outside the scope
            of health and wellness, politely redirect them to appropriate CVS Health resources or suggest
            they consult with a healthcare professional.

            Maintain a caring, professional, and supportive tone that reflects CVS Health's commitment to
            helping people on their path to better health.

            <chat_history>
            {chat_history}
            </chat_history>
            <context>
            {prompt_context}
            </context>
            <question>
            {user_question}
            </question>
            [/INST]
            """
    return prompt, results

def main():
    # Load CVS Health CSS
    load_cvs_css()
    
    # Create CVS Health header
    create_cvs_header()

    init_service_metadata()
    init_config_options()
    init_messages()

    # Display sample questions if no messages yet
    if len(st.session_state.messages) == 0:
        display_sample_questions()

    # Health-focused icons for chat
    icons = {"assistant": "❤️", "user": "👤"}

    # Display chat messages from history
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=icons[message["role"]]):
            st.markdown(message["content"])

    # Handle sample question selection
    if hasattr(st.session_state, 'sample_question'):
        question = st.session_state.sample_question
        del st.session_state.sample_question
        
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user", avatar=icons["user"]):
            st.markdown(question.replace("$", "\$"))
        
        # Process the question (same logic as manual input)
        with st.chat_message("assistant", avatar=icons["assistant"]):
            question_cleaned = question.replace("'", "")
            prompt, results = create_prompt(question_cleaned)
            with st.spinner("Thinking about your health question..."):
                generated_response = complete(
                    st.session_state.model_name, prompt
                )
                st.markdown(generated_response)
                
                # Build references in an expander
                with st.expander("📚 References", expanded=False):
                    for ref in results:
                        st.markdown(f"- [{ref['relative_path']}]({ref['file_url']})")


        st.session_state.messages.append(
            {"role": "assistant", "content": generated_response}
        )
        st.rerun()

    # Regular chat input
    disable_chat = (
        "service_metadata" not in st.session_state
        or len(st.session_state.service_metadata) == 0
    )
    
    if question := st.chat_input("Ask about health, wellness, pharmacy services, or benefits...", disabled=disable_chat):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": question})
        
        # Display user message
        with st.chat_message("user", avatar=icons["user"]):
            st.markdown(question.replace("$", "\$"))

        # Display assistant response
        with st.chat_message("assistant", avatar=icons["assistant"]):
            question_cleaned = question.replace("'", "")
            prompt, results = create_prompt(question_cleaned)
            with st.spinner("Thinking about your health question..."):
                generated_response = complete(
                    st.session_state.model_name, prompt
                )
                st.markdown(generated_response)
                
                # Build references in an expander
                with st.expander("📚 References", expanded=False):
                    for ref in results:
                        st.markdown(f"- [{ref['relative_path']}]({ref['file_url']})")


        st.session_state.messages.append(
            {"role": "assistant", "content": generated_response}
        )

    # CVS Health footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align: center; color: {CVS_DARK_GRAY}; font-family: 'Open Sans', sans-serif; padding: 1rem;">
        <p>❤️ <strong>CVS Health Assistant</strong> | Helping you on your path to better health</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">For medical emergencies, call 911. For urgent questions, consult your healthcare provider.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    session = get_active_session()
    root = Root(session)
    main()


"""
Streamlit Health Chatbot App
A simple and modern interface for the medical information chatbot
"""

import streamlit as st
from src.embedding import huggingface_embeddings
from src.vectorstore import load_vectorstore
from src.prompt import medical_information_prompt
from src.ollama_chain import create_rag_chain
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Health Chatbot",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="auto"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextInput > div > div > input {
        font-size: 1.1rem;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize the RAG chain (cached to avoid reloading)


@st.cache_resource
def initialize_chatbot():
    """Initialize the chatbot components"""
    with st.spinner("🔄 Loading AI model and medical knowledge base..."):
        try:
            embeddings = huggingface_embeddings(model_name="BAAI/bge-base-en-v1.5")
            vectorstore = load_vectorstore(
                embeddings=embeddings,
                vectorstore_path="faiss_index"
            )
            prompt = medical_information_prompt()
            chain = create_rag_chain(vectorstore=vectorstore, prompt=prompt)
            return chain
        except Exception as e:
            st.error(f"❌ Error initializing chatbot: {str(e)}")
            return None


# Header
st.markdown('<p class="main-header">🏥 Health Information Chatbot</p>',
            unsafe_allow_html=True)
st.markdown('<p class="sub-header">Ask questions about medical conditions, symptoms, and treatments</p>',
            unsafe_allow_html=True)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.info("""
    This chatbot uses:
    - 🤖 **Ollama** (DeepSeek-V3.1) for AI responses
    - 📚 **FAISS** vector database for medical knowledge
    - 🔍 **RAG** (Retrieval Augmented Generation) for accurate information
    """)

    st.header("💡 Tips")
    st.markdown("""
    - Ask about specific symptoms or conditions
    - Request information about treatments
    - Inquire about preventive measures
    - Be specific in your questions
    """)

    st.header("🔄 Actions")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# Initialize chatbot
chain = initialize_chatbot()

if chain is None:
    st.error(
        "Failed to initialize the chatbot. Please check your configuration and try again.")
    st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt_input := st.chat_input("Ask your health question here..."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt_input})

    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt_input)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching medical knowledge base..."):
            try:
                response = chain.invoke({"input": prompt_input})
                answer = response["answer"]

                # Display the answer
                st.markdown(answer)

                # Add assistant response to chat history
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer})

            except Exception as e:
                error_message = f"❌ An error occurred: {str(e)}"
                st.error(error_message)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_message})

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666; font-size: 0.9rem;'>"
    "Made with LangChain, Ollama and DeepSeek "
    "</p>",
    unsafe_allow_html=True
)

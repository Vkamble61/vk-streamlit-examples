import os
import streamlit as st
from crewai import Crew, Process
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from bot_crew import create_agents, create_tasks
from tools import fetch_and_store_content, process_pdf_file

# Load environment variables from .env file (for local development)
load_dotenv()

# For Streamlit Cloud deployment, use st.secrets
# This ensures API keys work both locally and in deployment
if hasattr(st, 'secrets'):
    try:
        if 'OPENAI_API_KEY' in st.secrets:
            os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
        if 'EXA_API_KEY' in st.secrets:
            os.environ['EXA_API_KEY'] = st.secrets['EXA_API_KEY']
    except Exception:
        pass  # If secrets are not configured, fall back to .env

# Streamlit UI
st.set_page_config(page_title="Website and Document Chatbot", page_icon="🤖", layout="wide")

# Sidebar
st.sidebar.title("🤖 CrewAI Setup")

# Source selection
st.sidebar.subheader("📁 Choose Content Source")
source_type = st.sidebar.radio(
    "What would you like to use as a source?",
    [ "Website URLs", "Upload PDF File"],
    index=0
)

st.sidebar.markdown("---")

# Conditional UI based on source type
if source_type == "Website URLs":
    st.sidebar.subheader("🌐 Website Source")
    website_urls = st.sidebar.text_area(
        "Enter website URLs (one per line)",
        value="https://technation-globaltalentvisa-guide.notion.site",   
        height=150
    )
    
    if st.sidebar.button("📥 Load Website Content"):
        with st.spinner("Loading content from websites..."):
            urls = [url.strip() for url in website_urls.split('\n') if url.strip()]
            vectordb = fetch_and_store_content(urls)
            if vectordb:
                st.session_state.vectordb = vectordb
                st.session_state.source_type = "website"
                st.sidebar.success("✅ Website content loaded successfully!")

else:  # Upload PDF File
    st.sidebar.subheader("📄 PDF File Source")
    uploaded_file = st.sidebar.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        help="Upload a PDF file to use as the knowledge source"
    )
    
    if uploaded_file is not None:
        if st.sidebar.button("📥 Load PDF Content"):
            with st.spinner("Processing PDF file..."):
                vectordb = process_pdf_file(uploaded_file)
                if vectordb:
                    st.session_state.vectordb = vectordb
                    st.session_state.source_type = "pdf"
                    st.sidebar.success("✅ PDF content loaded successfully!")

# Load existing database if available
if 'vectordb' not in st.session_state:
    if os.path.exists("chroma_db"):
        embeddings = OpenAIEmbeddings()
        st.session_state.vectordb = Chroma(
            persist_directory="chroma_db",
            embedding_function=embeddings
        )
        st.sidebar.info("📚 Using existing database")

# Main chat interface
st.title("💬 Website and Document Chatbot")
st.markdown("Select the content source from the sidebar and load content!")
st.markdown("Ask questions about the loaded content. The AI crew will research and answer!")

# Show current source type
if 'source_type' in st.session_state:
    source_icon = "🌐" if st.session_state.source_type == "website" else "📄"
    st.info(f"{source_icon} Currently using: **{st.session_state.source_type.upper()}** source")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about the content..."):
    # Check if database is loaded
    if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
        st.error("⚠️ Please load content first using the sidebar!")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Process with CrewAI
        with st.chat_message("assistant"):
            with st.spinner("🤖 AI Crew is working on your question..."):
                try:
                    # Create agents and tasks
                    research_agent, answer_agent = create_agents()
                    tasks = create_tasks(research_agent, answer_agent, prompt)
                    
                    # Create and run crew
                    crew = Crew(
                        agents=[research_agent, answer_agent],
                        tasks=tasks,
                        process=Process.sequential,
                        verbose=True
                    )
                    
                    # Execute crew
                    result = crew.kickoff()
                    
                    # Display result
                    st.markdown(str(result))
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": str(result)
                    })
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": error_msg
                    })

# Show database status
if 'vectordb' in st.session_state and st.session_state.vectordb is not None:
    st.sidebar.success("✅ Database loaded and ready")
else:
    st.sidebar.warning("⚠️ No database loaded")

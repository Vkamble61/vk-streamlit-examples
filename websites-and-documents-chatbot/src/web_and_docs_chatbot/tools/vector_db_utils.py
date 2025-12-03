import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings


def create_vector_db(docs):
    """
    Create a vector database from documents.
    
    Args:
        docs: List of Document objects to process        
        
    Returns:
        Chroma vector database instance or None if creation fails
    """
    persist_directory = "chroma_db"
    
    if not docs:
        st.sidebar.error("❌ No documents provided for vector database creation")
        return None
    
    try:
        # Split documents
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1500,
            chunk_overlap=300,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        split_docs = splitter.split_documents(docs)
        
        # Create vector database
        embeddings = OpenAIEmbeddings()
        vectordb = Chroma.from_documents(
            split_docs,
            embeddings,
            persist_directory=persist_directory
        )
        vectordb.persist()
        
        st.sidebar.success(f"✅ Created vector DB with {len(split_docs)} chunks")
        return vectordb
        
    except Exception as e:
        st.sidebar.error(f"❌ Failed to create vector database: {str(e)}")
        return None

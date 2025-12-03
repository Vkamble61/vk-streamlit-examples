import streamlit as st
from langchain_core.documents import Document
import PyPDF2
import io
from .vector_db_utils import create_vector_db


def process_pdf_file(uploaded_file):
    """Extract text from uploaded PDF and store in vector database."""
    docs = []
    
    try:
        st.sidebar.info(f"🔄 Processing PDF: {uploaded_file.name}")
        
        # Read PDF content
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        
        # Extract text from each page
        full_text = ""
        for page_num, page in enumerate(pdf_reader.pages):
            text = page.extract_text()
            if text and len(text.strip()) > 50:
                full_text += text + "\n\n"
        
        if not full_text.strip():
            st.sidebar.error("❌ No text content found in PDF")
            return None
        
        # Create document
        docs.append(Document(
            page_content=full_text,
            metadata={
                "source": uploaded_file.name,
                "type": "pdf"
            }
        ))
        
        st.sidebar.success(f"✅ Extracted {len(full_text)} characters from PDF")
        
    except Exception as e:
        st.sidebar.error(f"❌ Failed to process PDF: {str(e)}")
        return None
    
    # Create vector database using shared utility
    return create_vector_db(docs)

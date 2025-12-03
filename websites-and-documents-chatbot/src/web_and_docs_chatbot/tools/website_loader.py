import os
import streamlit as st
from langchain_core.documents import Document
from urllib.parse import urlparse
from exa_py import Exa
from .vector_db_utils import create_vector_db


def fetch_and_store_content(urls):
    """Fetch content from URLs using Exa and store in vector database."""
    docs = []
    
    # Initialize Exa client
    exa_api_key = os.getenv("EXA_API_KEY")
    if not exa_api_key:
        st.sidebar.error("⚠️ EXA_API_KEY not found in environment variables")
        return None
    
    exa = Exa(api_key=exa_api_key)
    
    for url in urls:
        try:
            st.sidebar.info(f"🔄 Fetching content from: {url}")
            
            # Check if URL is a Notion page
            if "notion.site" in url:
                st.sidebar.warning("⚠️ Notion pages - searching for related content")
                parsed = urlparse(url)
                domain_parts = parsed.netloc.split('.')
                if domain_parts:
                    # Extract the subdomain/site name from the Notion URL
                    site_name = domain_parts[0].replace('-', ' ')
                    search_query = f"{site_name}"
                    st.sidebar.info(f"🔍 Searching for: {search_query}")
                    
                    result = exa.search_and_contents(
                        query=search_query,
                        num_results=3,
                        text=True
                    )
                    st.sidebar.info(f"📊 Found {len(result.results)} related pages")
                else:
                    continue
            else:
                result = exa.get_contents(urls=[url], text=True)
                st.sidebar.info(f"📊 Exa returned {len(result.results)} result(s)")
            
            # Process results
            for content in result.results:
                text = content.text
                if text and len(text.strip()) > 200:
                    docs.append(Document(
                        page_content=text,
                        metadata={
                            "source": content.url if hasattr(content, 'url') else url,
                            "title": content.title or url
                        }
                    ))
                    st.sidebar.success(f"✅ Loaded: {len(text)} chars")
                    
        except Exception as e:
            st.sidebar.error(f"❌ Failed to load {url}: {str(e)}")
    
    if not docs:
        st.sidebar.error("❌ No documents were loaded")
        return None
    
    # Create vector database using shared utility
    return create_vector_db(docs)

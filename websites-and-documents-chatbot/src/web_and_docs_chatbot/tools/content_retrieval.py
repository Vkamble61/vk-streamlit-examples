import streamlit as st
from crewai.tools import BaseTool


class ContentRetrievalTool(BaseTool):
    name: str = "Content Retrieval Tool"
    description: str = "Retrieves relevant content from the vector database based on the query. Use this to search for information to answer user questions. This is your ONLY source of information."
    
    def _run(self, query: str) -> str:
        """Retrieves relevant content from the vector database based on the query."""
        if 'vectordb' not in st.session_state or st.session_state.vectordb is None:
            return "No content available. Please load URLs first."
        
        retriever = st.session_state.vectordb.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 5}
        )
        
        docs = retriever.invoke(query)
        
        if not docs:
            return "No relevant content found in the sources. The question cannot be answered based on the available information."
        
        # Format retrieved documents with source information
        context = []
        for i, doc in enumerate(docs, 1):
            source_name = doc.metadata.get('source', 'Unknown')
            title = doc.metadata.get('title', '')
            
            # Format source display
            if title and title != source_name:
                source_display = f"{title} ({source_name})"
            else:
                source_display = source_name
            
            context.append(f"[Source {i}: {source_display}]\n{doc.page_content}\n")
        
        return "\n\n".join(context)

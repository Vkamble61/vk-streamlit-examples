# Website and Document Chatbot with CrewAI

An intelligent chatbot application that uses CrewAI agents to answer questions about your source. The application supports multiple content sources (websites and PDF files), stores content in a vector database, and uses multiple AI agents to research and synthesize comprehensive answers.

## 🌟 Features

- **Multiple Content Sources**: Support for both website URLs and PDF file uploads
- **Multi-Agent AI System**: Uses CrewAI with specialized research and answer synthesis agents
- **Website Content Retrieval**: Fetches and processes website content using Exa API
- **PDF Processing**: Extracts and processes text from uploaded PDF files
- **Vector Database**: Stores content in ChromaDB for efficient semantic search with OpenAI embeddings
- **Intelligent Retrieval**: Semantic search returns top 5 most relevant content chunks
- **Context-Aware Answers**: Agents provide answers based exclusively on loaded content
- **Interactive Chat UI**: Clean Streamlit interface with chat history and sidebar controls
- **Configuration-Driven**: YAML-based configuration for agents and tasks (easy customization)
- **Modular Architecture**: Separated concerns with tools, config, and UI modules
- **Persistent Storage**: Vector database persists to disk for reuse across sessions
- **Source Indicators**: UI shows which content source (PDF or Website) is currently active

## 📁 Project Structure

```
websites-and-documents-chatbot/
├── .env                              # Environment variables (API keys)
├── .env.sample                       # Sample environment file
├── .gitignore                        # Git ignore rules
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── src/
    └── web_and_docs_chatbot/
        ├── streamlit_bot.py          # Main Streamlit application
        ├── bot_crew.py               # CrewAI agents and tasks setup
        ├── config/
        │   ├── agents.yaml           # Agent configurations
        │   └── tasks.yaml            # Task configurations
        └── tools/
            ├── __init__.py           # Tools module init
            ├── content_retrieval.py  # Content retrieval tool for CrewAI
            ├── website_loader.py     # Website content fetching and processing
            ├── pdf_loader.py         # PDF file processing and extraction
            └── vector_db_utils.py    # Shared vector database creation utility
```

**Note:** The vector database (`chroma_db/`) is auto-generated when content is loaded.

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key
- Exa API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd websites-and-documents-chatbot
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   
   Create a `.env` file in the project root and add your API keys:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   EXA_API_KEY=your_exa_api_key_here
   ```
   
   Get your API keys from:
   - OpenAI: https://platform.openai.com/api-keys
   - Exa: https://exa.ai/

### Running the Application

From the project root directory:

```bash
streamlit run src/web_and_docs_chatbot/streamlit_bot.py
```

Or navigate to the app directory first:

```bash
cd src/web_and_docs_chatbot
streamlit run streamlit_bot.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Choose Content Source**
   - Select between "Upload PDF File" or "Website URLs" in the sidebar

2. **Load Content**
   
   **For PDF Files:**
   - Upload a PDF file using the file uploader
   - Click "📥 Load PDF Content" to extract and process the text
   - Wait for the vector database to be created
   
   **For Website URLs:**
   - Enter website URLs in the text area (one per line)
   - Click "📥 Load Website Content" to fetch and process the content
   - Wait for the vector database to be created

3. **Ask Questions**
   - Type your question in the chat input
   - The AI crew will research the content and provide a detailed answer
   - Answers are based only on the loaded content
   - The chatbot will indicate which source type (PDF or Website) is currently active

## 🏗️ Architecture

### Components

- **`streamlit_bot.py`**: Main application file with Streamlit UI, chat interface, and content source management
- **`bot_crew.py`**: CrewAI setup with functions to create agents and tasks from YAML configurations
- **`config/agents.yaml`**: Agent definitions (Research Specialist and Answer Synthesizer with roles, goals, and backstories)
- **`config/tasks.yaml`**: Task definitions (research and answer synthesis with descriptions and expected outputs)
- **`tools/content_retrieval.py`**: Custom CrewAI tool for semantic search in the vector database
- **`tools/website_loader.py`**: Website content fetching via Exa API with text chunking and vector storage
- **`tools/pdf_loader.py`**: PDF text extraction using PyPDF2 with chunking and vector storage
- **`tools/vector_db_utils.py`**: Shared ChromaDB creation utility with consistent chunking (1000 chars, 200 overlap) and OpenAI embeddings

### Agent Workflow

1. **User Input**: Question submitted via Streamlit chat interface
2. **Research Agent**: 
   - Uses ContentRetrievalTool to search vector database
   - Retrieves top 5 most relevant content chunks
   - Performs semantic search based on user question
3. **Answer Agent**: 
   - Receives research findings as context
   - Synthesizes information into comprehensive answer
   - **ONLY uses provided context** - no general knowledge
   - Clearly states if information is not available in sources
4. **Sequential Process**: Tasks execute in order with context passing between agents
5. **Response**: Final answer displayed in chat interface with source type indicator

## 🔧 Configuration

### Modifying Agents

Edit `config/agents.yaml` to customize agent behavior:
- `role`: The agent's role description
- `goal`: What the agent aims to achieve
- `backstory`: Context and personality for the agent

### Modifying Tasks

Edit `config/tasks.yaml` to customize task execution:
- `description`: Detailed task instructions
- `expected_output`: What the task should produce
- `context`: Dependencies on other tasks

## 🛠️ Development

### Adding New Tools

**For CrewAI Tools:**
1. Create a new tool class in `tools/` directory
2. Inherit from `BaseTool` and implement `_run()` method
3. Add the tool to `tools/__init__.py`
4. Import and use in `bot_crew.py`

**For Processing Tools:**
1. Create a new processing function in `tools/` directory
2. Implement the processing logic (e.g., file parsing, content fetching)
3. Export the function from `tools/__init__.py`
4. Import and use in `streamlit_bot.py`

### Customizing the UI

Modify `streamlit_bot.py` to:
- Change page configuration
- Add new sidebar controls
- Customize chat message display
- Modify content loading behavior

## 📦 Dependencies

- **streamlit**: Web application framework
- **crewai**: Multi-agent AI framework
- **crewai-tools**: Additional tools for CrewAI
- **langchain-openai**: OpenAI integration for LangChain
- **langchain-community**: Community LangChain components
- **langchain-text-splitters**: Text splitting utilities for document processing
- **chromadb**: Vector database for embeddings
- **exa-py**: Exa API client for website content fetching
- **PyPDF2**: PDF file text extraction
- **python-dotenv**: Environment variable management
- **tiktoken**: Token counting for OpenAI models
- **beautifulsoup4**: HTML parsing
- **requests**: HTTP library

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## ⚠️ Troubleshooting

### Common Issues

**"streamlit: command not found"**
- Ensure you've activated your virtual environment
- Verify streamlit is installed: `pip list | grep streamlit`

**"No module named 'dotenv'"**
- Install missing dependencies: `pip install -r requirements.txt`

**API Key Errors**
- Verify `.env` file exists in the project root
- Check that API keys are valid and have no extra spaces
- Ensure `.env` file is not in `.gitignore` (it should be!)

**Vector Database Issues**
- Delete the `chromadb/` folder and reload content
- Check that content was successfully loaded before asking questions

**Path Errors**
- Make sure to run from project root: `streamlit run src/web_and_docs_chatbot/streamlit_bot.py`
- Or navigate to the directory first: `cd src/web_and_docs_chatbot` then `streamlit run streamlit_bot.py`

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- Built with [CrewAI](https://www.crewai.com/)
- Powered by [Streamlit](https://streamlit.io/)
- Content retrieval via [Exa](https://exa.ai/)

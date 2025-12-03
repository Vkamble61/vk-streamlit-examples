# Deployment Guide for Website and Document Chatbot

## 🚀 Deploy to Streamlit Community Cloud

### Step 1: Prepare Your Repository

1. **Commit your changes** (but NOT your secrets):
   ```bash
   cd /workspaces/vk-streamlit-examples
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. **Go to Streamlit Cloud**: Visit [share.streamlit.io](https://share.streamlit.io)

2. **Sign in** with your GitHub account

3. **Click "New app"**

4. **Configure your app**:
   - **Repository**: `Vkamble61/vk-streamlit-examples`
   - **Branch**: `main`
   - **Main file path**: `websites-and-documents-chatbot/src/web_and_docs_chatbot/streamlit_bot.py`

5. **Add Secrets** (Click "Advanced settings" → "Secrets"):
   ```toml
   OPENAI_API_KEY = "your_actual_openai_api_key"
   EXA_API_KEY = "your_actual_exa_api_key"
   ```

6. **Click "Deploy"** and wait for the app to start

### Step 3: Update Code to Use Streamlit Secrets

The app will automatically use secrets from both `.env` (local) and Streamlit Cloud secrets (deployed).

---

## 🐳 Alternative: Deploy with Docker

### Create Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "src/web_and_docs_chatbot/streamlit_bot.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run

```bash
cd /workspaces/vk-streamlit-examples/websites-and-documents-chatbot
docker build -t chatbot-app .
docker run -p 8501:8501 --env-file .env chatbot-app
```

---

## ☁️ Alternative: Deploy to Other Platforms

### Heroku

1. Create `Procfile`:
   ```
   web: streamlit run src/web_and_docs_chatbot/streamlit_bot.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.13
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY="your_key"
   heroku config:set EXA_API_KEY="your_key"
   git push heroku main
   ```

### AWS EC2 / Azure / GCP

1. Set up a VM instance
2. Install Python and dependencies
3. Set environment variables
4. Run with: `streamlit run src/web_and_docs_chatbot/streamlit_bot.py --server.port=8501`

---

## 📝 Important Notes

- **API Keys**: Never commit `.env` or `.streamlit/secrets.toml` to Git
- **ChromaDB**: The vector database will be recreated when users load content
- **Memory**: Ensure your deployment has sufficient memory for vector operations
- **Cold Starts**: First load may take longer as dependencies initialize

## 🔍 Verify Deployment

After deployment, test:
1. Load website content or upload a PDF
2. Ask a question
3. Verify the AI crew responds with relevant answers

## 🆘 Troubleshooting

- **Import errors**: Ensure all packages in `requirements.txt` are installed
- **API key errors**: Double-check secrets configuration
- **Memory issues**: Upgrade to higher tier or optimize chunk sizes
- **ChromaDB errors**: May need persistent storage volume for production

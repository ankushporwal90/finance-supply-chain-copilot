# Deployment Guide

The target deployment is Streamlit Community Cloud because it is free and beginner-friendly.

## Local Run

```bash
cd finance_supply_chain_copilot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
streamlit run app/main.py
```

Add your free Groq API key to `.env` before using AI features.

## Streamlit Community Cloud

1. Push the repository to GitHub.
2. Go to Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Set the main file path to:

```text
app/main.py
```

5. Add secrets in Streamlit's app settings:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
GROQ_MODEL = "llama-3.1-8b-instant"
SEC_USER_AGENT = "Your Name your.email@example.com"
```

## Free Deployment Notes

- ChromaDB local files may reset on redeploy depending on the hosting runtime.
- For portfolio demos, users can upload documents during the session.
- For persistent hosted storage, a later phase can add SQLite-backed metadata and optional external storage.

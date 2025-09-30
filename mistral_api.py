import requests
import streamlit as st

API_URL = "https://api.mistral.ai/v1/chat/completions"

def call_mistral(text):
    api_key = st.secrets.get("MISTRAL_API_KEY")

    if not api_key:
        raise Exception("⚠️ API key not found in Streamlit secrets. Please check .streamlit/secrets.toml")

    prompt = f"""
Extract semantic metadata from the following document content.

{text}

Return only a raw JSON object like this (no explanation, no markdown, no text outside JSON):

{{
  "title": "...",
  "summary": "...",
  "keywords": "...",
  "main_topics": "...",
  "document_type": "...",
  "text_length_in_characters": ...
}}
"""

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistral-medium",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

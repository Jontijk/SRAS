
import os
import requests
import streamlit as st
from sras.utils.response_formatter import format_response, show_synthesis_progress

try:
    from google.colab import userdata
    secret_value = userdata.get('sras-api')
except:
    secret_value = os.getenv("HUGGINGFACE_TOKEN")

if not secret_value:
    st.warning("⚠️ Hugging Face API token is missing. Please set it via Colab userdata or environment variable.")

headers = {"Authorization": f"Bearer {secret_value}"}

task_options = {
    "General Summary": "facebook/bart-large-cnn",
    "Scientific Paper Summary": "allenai/led-large-16384-arxiv",
    "News Headline Summary": "sshleifer/distilbart-cnn-12-6",
    "Bullet Point Summary": "philschmid/bart-large-cnn-samsum"
}

def query(payload, model):
    API_URL = f"https://api-inference.huggingface.co/models/{model}"
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        return [{"summary_text": f"Error: {response.status_code}, {response.text}"}]

def summarize_ui():
    st.header("📝 Smart Summarizer Agent")

    input_text = st.text_area("Paste your content below:", height=300)
    summary_task = st.selectbox("Choose Summary Type", list(task_options.keys()))
    model = task_options[summary_task]
    max_length = st.slider("Choose Summary Length", min_value=50, max_value=512, value=150)

    if st.button("Generate Summary"):
        if not input_text.strip():
            st.warning("Please enter some text to summarize.")
            return
        
        # Show stepwise synthesis progress to user
        show_synthesis_progress()

        # Call Hugging Face API
        output = query({"inputs": input_text, "parameters": {"max_length": max_length}}, model)
        summary_text = output[0].get("summary_text", "Error: Summary generation failed.")

        # Use centralized formatter to show output
        format_response("summarizer", summary_text)

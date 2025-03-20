import streamlit as st
import requests
from gtts import gTTS
from googletrans import Translator
import asyncio
import os

API_URL = "http://127.0.0.1:8000/scrape"

st.markdown(
    """
    <style>
    .main {
        background-color: #f4f4f4;
    }
    .title {
        font-size: 32px;
        font-weight: bold;
        color: #4a90e2;
        text-align: center;
    }
    .subtitle {
        font-size: 18px;
        font-weight: bold;
        color: #333;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 10px;
        border-radius: 8px;
        margin-bottom: 15px;
        color: #0d47a1;
    }
    .btn-custom {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 10px;
        border-radius: 5px;
        text-align: center;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# App Title
st.markdown('<div class="title">📢 News Summarization & Sentiment Analysis</div>', unsafe_allow_html=True)
st.write("Enter a **company name** to get summarized news, sentiment analysis, and a Hindi TTS output.")

# Input Section
st.markdown('<div class="subtitle">🔎 Enter Company Name:</div>', unsafe_allow_html=True)
company_name = st.text_input("", "Tesla")

# Fetch News Button
if st.button("🚀 Fetch News", help="Click to fetch the latest news articles"):
    with st.spinner("Fetching latest news..."):
        response = requests.get(API_URL, params={"company": company_name, "num_articles": 10})

        if response.status_code == 200:
            data = response.json()

            st.markdown('<div class="info-box">✅ Successfully retrieved news articles!</div>', unsafe_allow_html=True)

            st.subheader(f"📰 News Articles for {company_name}")
            st.json(data)  

            translator = Translator()
            tts_text_hindi = asyncio.run(
                translator.translate(data["final_sentiment_analysis"], src="en", dest="hi")
            ).text

            st.subheader("🔊 Hindi Text-to-Speech (TTS) Summary")
            tts = gTTS(text=tts_text_hindi, lang="hi")
            tts.save("summary.mp3")
            st.audio("summary.mp3", format="audio/mp3")

        else:
            st.markdown('<div class="info-box" style="background-color:#ffccbc; color:#d32f2f;">❌ Failed to fetch news. Please try again.</div>', unsafe_allow_html=True)

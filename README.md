News Summarization & Sentiment Analysis
A FastAPI & Streamlit-based application that fetches news articles for a given company, summarizes them, performs sentiment analysis, and generates Hindi text-to-speech (TTS) output.

📌 Features
- Fetches latest news articles using NewsAPI.
  
- Summarizes news articles using TextRank (Sumy library).
  
- Performs Sentiment Analysis using VADER (NLTK).

- Extracts Key Topics from each article.

- Generates Hindi Speech Output using Google Text-to-Speech (gTTS).

- Provides Comparative Sentiment Analysis to identify trends.

- Displays topic overlap between articles.

📌 Tech Stack
- Backend: FastAPI
- Frontend: Streamlit
- APIs Used: NewsAPI, GoogleTrans, gTTS
- NLP Libraries: Sumy, NLTK
- Speech Synthesis: gTTS

📌 Installation & Setup
🔹 Prerequisites

Python 3.8+ installed.

NewsAPI Key (Get one from https://newsapi.org/).

🔹 Step 1: Clone the Repository
```
git clone https://github.com/your-repo/news-summarization.git
cd news-summarization
```
Or manually download the project folder.

🔹 Step 2: Create a Virtual Environment
It is recommended to create a virtual environment before installing dependencies:

```
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```
🔹 Step 3: Install Dependencies
Install the required libraries using:
```
pip install -r requirements.txt
```
🔹 Step 4: Start the FastAPI Backend
Run the backend server using:

```
uvicorn api:app --reload
The API will be accessible at http://127.0.0.1:8000.
```

🔹 Step 5: Run the Streamlit Frontend
Launch the frontend UI with:

```streamlit run app.py
This will open the Streamlit UI in your web browser.
```
📌 How It Works

- User Inputs a Company Name – The system fetches news articles related to the given company.
- News Summarization – The TextRank algorithm extracts key points from each article.
- Sentiment Analysis – The VADER model determines if the article is Positive, Negative, or Neutral.
- Topic Extraction – The system extracts important topics from the article text.
- Comparative Analysis – The sentiment distribution and common/unique topics between articles are identified.
- Hindi TTS Output – The final sentiment summary is translated into Hindi and converted into audio (MP3).
- Results are Displayed – The news articles, sentiment scores, and audio output are shown on the Streamlit UI.

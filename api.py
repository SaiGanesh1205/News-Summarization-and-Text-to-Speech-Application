from fastapi import FastAPI
from utils import scrape_news
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"message": "News Summarization API is running!"}

@app.get("/scrape/")
def scrape(company: str, num_articles: int = 10):
    """
    API Endpoint to fetch relevant news, summarize, and analyze sentiment.
    """
    news_data = scrape_news(company, num_articles)

    if isinstance(news_data, dict) and "error" in news_data:
        return {"error": news_data["error"]}

    return news_data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

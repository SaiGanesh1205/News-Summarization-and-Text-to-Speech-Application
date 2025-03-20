import requests
from bs4 import BeautifulSoup
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import nltk
import re
from collections import Counter

# Download necessary NLTK data
nltk.download("stopwords")
nltk.download("vader_lexicon")
nltk.download("averaged_perceptron_tagger")
nltk.download("punkt")

NEWSAPI_KEY = "44e8b2ec1d81413fb46d559361bff2c1"  

def scrape_news(company_name, num_articles=10):
    """
    Fetches news articles related to a company from NewsAPI.

    Returns:
    - Dictionary containing articles, comparative sentiment analysis, and final sentiment summary.
    """
    base_url = "https://newsapi.org/v2/everything"

    params = {
        "q": company_name,
        "apiKey": NEWSAPI_KEY,
        "language": "en",
        "pageSize": num_articles,
        "sortBy": "relevancy"
    }

    response = requests.get(base_url, params=params)

    if response.status_code != 200:
        return {"error": f"Failed to fetch news. Status code: {response.status_code}"}

    data = response.json()

    if "articles" not in data or not data["articles"]:
        return {"error": "No articles found."}

    articles = []
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    
    for item in data["articles"]:
        title = item["title"]
        summary = item["description"] if item["description"] else "Summary not available."
        url = item["url"]

        clean_summary = clean_text(summary)

        summarized_text = summarize_text(clean_summary)

        sentiment = analyze_sentiment(summarized_text)
        sentiment_counts[sentiment] += 1

        topics = extract_topics(title + " " + summarized_text)

        articles.append({
            "title": title,
            "summary": summarized_text,
            "sentiment": sentiment,
            "topics": topics,
            "url": url
        })

    comparative_analysis = generate_comparative_analysis(articles)
    comparisons = generate_comparisons(articles)  # Call new comparison function

    return {
        "company": company_name,
        "articles": articles,
        "comparative_sentiment_score": comparative_analysis,
        "article_comparisons": comparisons,  # Include article comparisons in final output
        "final_sentiment_analysis": generate_final_sentiment(sentiment_counts,company_name)
    }


def clean_text(text):
    """Cleans text by removing HTML tags and unnecessary characters."""
    soup = BeautifulSoup(text, "html.parser")
    cleaned_text = soup.get_text(separator=" ")  
    cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
    return cleaned_text


def summarize_text(text, num_sentences=2):
    """Summarizes text using TextRank and maintains sentence structure."""
    parser = PlaintextParser.from_string(text, Tokenizer("english"))
    summarizer = TextRankSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return " ".join(str(sentence) for sentence in summary)


def analyze_sentiment(text):
    """Performs sentiment analysis using VADER."""
    sia = SentimentIntensityAnalyzer()
    sentiment_score = sia.polarity_scores(text)["compound"]

    if sentiment_score > 0.05:
        return "Positive"
    elif sentiment_score < -0.05:
        return "Negative"
    else:
        return "Neutral"


def extract_topics(text):
    """Extracts key topics by removing stop words and action words, keeping only meaningful nouns."""
    stop_words = set(stopwords.words("english"))
    words = word_tokenize(text)

    tagged_words = pos_tag(words)

    filtered_words = [word for word, tag in tagged_words if tag in ["NN", "NNS", "NNP", "NNPS"] and word.lower() not in stop_words]

    common_words = Counter(filtered_words).most_common(3)
    return [word[0] for word in common_words]  # Extract only the words, not counts


def generate_comparative_analysis(articles):
    """Dynamically generates comparative sentiment analysis & topic comparison."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for article in articles:
        sentiment_counts[article["sentiment"]] += 1

    topic_overlap = {
        "Common Topics": list(set(articles[0]["topics"]) & set(articles[1]["topics"])),
        "Unique Topics in Article 1": list(set(articles[0]["topics"]) - set(articles[1]["topics"])),
        "Unique Topics in Article 2": list(set(articles[1]["topics"]) - set(articles[0]["topics"]))
    }

    return {
        "Sentiment Distribution": sentiment_counts,
        "Topic Overlap": topic_overlap
    }


def generate_comparisons(articles):
    """Generates article comparisons and their impact dynamically."""
    comparisons = []
    
    for i in range(len(articles) - 1):
        article1 = articles[i]
        article2 = articles[i + 1]
        
        comparison_text = f"Article {i+1} focuses on {', '.join(article1['topics'])}, while Article {i+2} discusses {', '.join(article2['topics'])}."
        impact_text = f"Article {i+1} titled '{article1['title']}' discusses {article1['summary'][:50]}..., whereas Article {i+2} titled '{article2['title']}' covers {article2['summary'][:50]}..."
        
        comparisons.append({
            "Comparison": comparison_text,
            "Impact": impact_text
        })

    return comparisons


def generate_final_sentiment(sentiment_counts, company_name):
    """Generates a final sentiment summary dynamically using the company name."""
    if sentiment_counts["Positive"] > sentiment_counts["Negative"]:
        return f"{company_name}'s latest news coverage is mostly positive."
    elif sentiment_counts["Negative"] > sentiment_counts["Positive"]:
        return f"{company_name}'s latest news coverage is mostly negative."
    else:
        return f"{company_name}'s news coverage is balanced, with both positive and negative insights."
    



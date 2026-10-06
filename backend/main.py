from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from recommender import ContentRecommender
from classifier import ArticleClassifier

app = FastAPI(title="News Aggregator API")

# Add this CORS configuration right after initializing the app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, we will replace "*" with your live Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading AI Models into memory...")
recommender = ContentRecommender()
nlp = ArticleClassifier()

@app.get("/")
def read_root():
    return {"status": "Backend is running!"}

@app.get("/api/news")
def get_latest_news():
    """Returns the top 5 articles from our cached data."""
    df = pd.read_csv("news_cache.csv")
    return df.head(50).to_dict(orient="records")

@app.get("/api/recommend/{article_id}")
def recommend(article_id: int):
    """Returns 3 recommended articles similar to the provided ID."""
    results = recommender.recommend(article_id=article_id, top_n=3)
    return results.to_dict(orient="records")

@app.get("/api/classify/{article_id}")
def classify(article_id: int):
    """Classifies a specific article as Fact or Opinion."""
    df = pd.read_csv("news_cache.csv")
    article = df[df['id'] == article_id]
    
    if article.empty:
        return {"error": "Article not found"}
        
    text = article.iloc[0]['full_text']
    result = nlp.classify_text(text)
    return {"article_id": article_id, "classification": result}
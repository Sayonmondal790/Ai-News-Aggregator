import feedparser
import pandas as pd
from datetime import datetime
import re

# RSS Feeds across diverse categories (Updated to Times of India)
RSS_FEEDS = {
    "Technology": "https://timesofindia.indiatimes.com/rssfeeds/5880659.cms",
    "Business": "https://timesofindia.indiatimes.com/rssfeeds/1898055.cms",
    "General": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "World": "https://timesofindia.indiatimes.com/rssfeeds/296589292.cms"
}

def clean_html(text: str) -> str:
    """Strips HTML tags and normalizes whitespace."""
    if not isinstance(text, str):
        return ""
    clean = re.sub(r'<.*?>', '', text)
    clean = re.sub(r'\s+', ' ', clean)
    return clean.strip()

def calculate_reading_time(text: str, wpm: int = 200) -> int:
    """Estimates reading time in minutes based on word count."""
    words = len(text.split())
    minutes = round(words / wpm)
    return max(1, minutes)

def fetch_live_news() -> pd.DataFrame:
    """Fetches, cleans, and standardizes live articles from RSS feeds."""
    articles = []
    
    for category, url in RSS_FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = getattr(entry, 'title', '').strip()
            summary = clean_html(getattr(entry, 'summary', ''))
            link = getattr(entry, 'link', '').strip()
            published = getattr(entry, 'published', str(datetime.utcnow()))
            
            # Combine title and summary for feature extraction
            full_text = f"{title}. {summary}"
            read_time = calculate_reading_time(full_text)
            
            if title:
                articles.append({
                    "id": len(articles) + 1,
                    "title": title,
                    "summary": summary,
                    "full_text": full_text,
                    "category": category,
                    "source": feed.feed.get('title', 'Times of India'),
                    "url": link,
                    "published": published,
                    "reading_time_min": read_time
                })
            
    df = pd.DataFrame(articles)
    df.drop_duplicates(subset=["title"], inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df

if __name__ == "__main__":
    print("Fetching live news feed...")
    df = fetch_live_news()
    print(f"Total unique articles collected: {len(df)}")
    print("\nBreakdown by category:")
    print(df['category'].value_counts())
    
    # Save cache for downstream modeling and offline testing
    df.to_csv("news_cache.csv", index=False)
    print("\nSaved output to backend/news_cache.csv")
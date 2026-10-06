import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class ContentRecommender:
    def __init__(self, data_path: str = "news_cache.csv"):
        self.df = pd.read_csv(data_path)
        self.vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
        # Generate the TF-IDF feature matrix from full article text
        self.tfidf_matrix = self.vectorizer.fit_transform(self.df["full_text"].fillna(""))
        # Compute pairwise cosine similarity between all articles
        self.similarity_matrix = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)

    def filter_duplicates(self, threshold: float = 0.75) -> pd.DataFrame:
        """
        Removes redundant stories reporting the same event from different publishers.
        """
        to_drop = set()
        n = len(self.df)
        for i in range(n):
            if i in to_drop:
                continue
            for j in range(i + 1, n):
                if self.similarity_matrix[i, j] >= threshold:
                    to_drop.add(j)
        
        filtered_df = self.df.drop(index=list(to_drop)).reset_index(drop=True)
        return filtered_df

    def recommend(self, article_id: int, top_n: int = 5) -> pd.DataFrame:
        """
        Finds the top N articles most similar to a selected article.
        """
        if article_id not in self.df["id"].values:
            return pd.DataFrame()

        idx = self.df.index[self.df["id"] == article_id][0]
        sim_scores = list(enumerate(self.similarity_matrix[idx]))
        
        # Sort descending by similarity, excluding the article itself
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:top_n + 1]
        recommended_indices = [i[0] for i in sim_scores]

        results = self.df.iloc[recommended_indices][["id", "title", "category", "reading_time_min"]].copy()
        results["similarity_score"] = [round(score[1], 3) for score in sim_scores]
        return results

if __name__ == "__main__":
    recommender = ContentRecommender()
    print(f"Loaded {len(recommender.df)} articles into vector space.")
    
    # Test deduplication
    unique_articles = recommender.filter_duplicates(threshold=0.75)
    print(f"Articles after cross-publisher deduplication: {len(unique_articles)}")
    
    # Test recommendation based on article ID 1
    sample_id = recommender.df.iloc[0]["id"]
    sample_title = recommender.df.iloc[0]["title"]
    print(f"\nTarget Article (ID {sample_id}): {sample_title}")
    
    recommendations = recommender.recommend(article_id=sample_id, top_n=3)
    print("\nTop 3 Recommended Articles:")
    print(recommendations)
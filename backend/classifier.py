import os
import requests

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

class ArticleClassifier:
    def __init__(self):
        self.labels = ["politics", "technology", "sports", "business"]

    def classify(self, text):
        payload = {
            "inputs": text,
            "parameters": {"candidate_labels": self.labels}
        }
        try:
            response = requests.post(API_URL, headers=headers, json=payload, timeout=10)
            result = response.json()
            if isinstance(result, dict) and "labels" in result:
                return result["labels"][0]
        except Exception as e:
            print(f"Classification error: {e}")
        return "uncategorized"

    # Alias in case your code calls predict() instead of classify()
    def predict(self, text):
        return self.classify(text)
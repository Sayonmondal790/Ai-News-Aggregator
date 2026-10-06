import requests
import os

# This points to the exact same model you were using locally
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

# Render will pass your secure token into os.getenv()
headers = {"Authorization": f"Bearer {os.getenv('HF_TOKEN')}"}

def categorize_news(text, labels=["politics", "technology", "sports", "business"]):
    payload = {
        "inputs": text,
        "parameters": {"candidate_labels": labels}
    }
    
    # Send the text to Hugging Face instead of processing it on Render
    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()
    
    # Return the highest scoring label
    if "labels" in result:
        return result["labels"][0]
    
    return "uncategorized"
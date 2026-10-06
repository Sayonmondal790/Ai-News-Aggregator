from transformers import pipeline

class ArticleClassifier:
    def __init__(self):
        # Using the heavy, highly accurate BART model
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="facebook/bart-large-mnli"
        )
        self.labels = ["factual reporting", "personal opinion"]

    def classify_text(self, text: str) -> dict:
        truncated_text = text[:800]
        result = self.classifier(truncated_text, candidate_labels=self.labels)
        
        is_opinion = result['labels'][0] == "personal opinion"
        
        return {
            "label": "Opinion" if is_opinion else "Fact",
            "confidence": round(result['scores'][0], 3)
        }

if __name__ == "__main__":
    print("Downloading & Loading Heavy NLP Model (this will take a few minutes)...")
    nlp = ArticleClassifier()
    
    test_opinion = "In my view, the latest economic policies are a complete disaster and show a total lack of leadership from the government."
    print(f"\nTest 1 (Expected: Opinion): {nlp.classify_text(test_opinion)}")
    
    test_fact = "The central bank announced a 0.5% interest rate hike on Wednesday, aiming to curb rising inflation levels across the country."
    print(f"Test 2 (Expected: Fact): {nlp.classify_text(test_fact)}")
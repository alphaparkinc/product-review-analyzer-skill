"""
example_usage.py -- Demonstrates ProductReviewAnalyzerClient
"""
from client import ProductReviewAnalyzerClient

def main():
    client = ProductReviewAnalyzerClient()
    reviews = [
        {"rating": 5, "text": "Premium quality material, sturdy feel, fast shipping!"},
        {"rating": 1, "text": "The box arrived crushed and leaking. Unusable packaging."},
        {"rating": 4, "text": "Works great, but instructions were confusing and hard to set up."},
        {"rating": 5, "text": "Very affordable, worth it. Arrived early."}
    ]
    result = client.analyze(reviews)
    print("[Product Review Analyzer Result]")
    print(f"Sentiment: {result['sentiment_distribution']}")
    print(f"Pros: {result['pros']}")
    print(f"Cons: {result['cons']}")
    print(f"Feedback: {result['actionable_feedback']}")

if __name__ == "__main__":
    main()

"""
product-review-analyzer-skill: Client SDK
NLP feedback summarizer that highlights strengths, complaints, and fixes from buyer reviews.
"""
from __future__ import annotations
from typing import Optional

KEYWORD_RULES = {
    "pros": {
        "quality": ["quality", "durable", "well made", "solid", "premium", "sturdy"],
        "delivery": ["fast shipping", "delivered quickly", "arrived early", "fast delivery"],
        "effectiveness": ["works great", "perfectly", "brightens", "solved my", "helps with", "effective"],
        "design": ["beautiful", "looks good", "sleek", "modern", "aesthetic", "gorgeous"],
        "value": ["cheap", "affordable", "worth it", "good value", "price was great"],
    },
    "cons": {
        "packaging": ["damaged box", "crushed", "leaking", "broken seal", "poor package"],
        "delivery": ["late", "delayed", "slow shipping", "took forever", "lost item"],
        "quality": ["cheap material", "broke easily", "ripped", "stopped working", "flimsy"],
        "sizing": ["too small", "too big", "wrong size", "tight", "loose", "doesn't fit"],
        "instructions": ["confusing", "no manual", "hard to set up", "difficult to use"],
    }
}

RECOMMENDATION_TEMPLATES = {
    "packaging": "Audit warehouse packing steps and consider adding extra bubble wrap for fragile shipments.",
    "delivery": "Investigate shipping partner SLAs or offer alternative expedited shipping carriers.",
    "quality": "Coordinate with product supplier/manufacturer regarding component quality controls.",
    "sizing": "Update size charts on the product detail pages with explicit body measurements.",
    "instructions": "Redesign or translate setup sheets, or include a QR code linking to a step-by-step video guide.",
}


class ProductReviewAnalyzerClient:
    """
    SDK for analyzing customer reviews.
    """

    def analyze(self, reviews: list[str | dict]) -> dict:
        total = len(reviews)
        if total == 0:
            return {"sentiment_distribution": {}, "pros": [], "cons": [], "actionable_feedback": []}

        pos_count, neu_count, neg_count = 0, 0, 0
        pro_themes = {}
        con_themes = {}

        for item in reviews:
            # Parse text and rating
            if isinstance(item, dict):
                text = str(item.get("text", "")).lower()
                rating = int(item.get("rating", 3))
            else:
                text = str(item).lower()
                rating = 3

            # Rule-based sentiment
            neg_words = sum(1 for lst in KEYWORD_RULES["cons"].values() for kw in lst if kw in text)
            pos_words = sum(1 for lst in KEYWORD_RULES["pros"].values() for kw in lst if kw in text)

            if rating >= 4 or (rating == 3 and pos_words > neg_words):
                pos_count += 1
            elif rating <= 2 or (rating == 3 and neg_words > pos_words):
                neg_count += 1
            else:
                neu_count += 1

            # Extract Pros
            for label, kws in KEYWORD_RULES["pros"].items():
                if any(kw in text for kw in kws):
                    pro_themes[label] = pro_themes.get(label, 0) + 1

            # Extract Cons
            for label, kws in KEYWORD_RULES["cons"].items():
                if any(kw in text for kw in kws):
                    con_themes[label] = con_themes.get(label, 0) + 1

        # Format Pros & Cons sorted by frequency
        pros_out = sorted([k for k in pro_themes], key=lambda x: pro_themes[x], reverse=True)
        cons_out = sorted([k for k in con_themes], key=lambda x: con_themes[x], reverse=True)

        # Actionable recommendations
        action_feedback = []
        for issue in cons_out[:3]:
            if issue in RECOMMENDATION_TEMPLATES:
                action_feedback.append(RECOMMENDATION_TEMPLATES[issue])

        return {
            "sentiment_distribution": {
                "positive_pct": round(pos_count / total * 100, 1),
                "neutral_pct": round(neu_count / total * 100, 1),
                "negative_pct": round(neg_count / total * 100, 1),
            },
            "pros": pros_out[:3],
            "cons": cons_out[:3],
            "actionable_feedback": action_feedback,
        }

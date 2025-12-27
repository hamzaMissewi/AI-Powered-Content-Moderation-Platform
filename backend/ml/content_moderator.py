# backend/app/ml/content_moderator.py
from transformers import pipeline
import torch
from typing import Dict, Any

class ContentModerator:
    def __init__(self):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.text_pipeline = pipeline(
            "text-classification",
            model="facebook/bart-large-mnli",
            device=self.device
        )
        self.categories = [
            "hate_speech", "harassment", "self_harm",
            "sexual_content", "violence", "illegal_activities"
        ]
    
    async def moderate_text(self, text: str) -> Dict[str, Any]:
        results = {}
        for category in self.categories:
            result = self.text_pipeline(
                text,
                candidate_labels=[category, "neutral"],
                hypothesis_template="This text contains {}."
            )
            score = result["scores"][0] if result["labels"][0] == category else 1 - result["scores"][0]
            results[category] = {
                "score": float(score),
                "is_violation": score > 0.7
            }
        
        return {
            "is_approved": not any(r["is_violation"] for r in results.values()),
            "categories": results
        }
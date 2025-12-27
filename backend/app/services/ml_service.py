from typing import Dict, List, Optional, Tuple
import logging
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from PIL import Image
import io

logger = logging.getLogger(__name__)

class ContentModerator:
    def __init__(self):
        self.text_pipeline = None
        self.image_pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_models()
    
    def _load_models(self):
        """Load the ML models for text and image moderation"""
        try:
            # Text moderation model (Hate speech, offensive language, etc.)
            model_name = "facebook/bart-large-mnli"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            
            # Define content categories we want to moderate
            self.content_categories = [
                "hate_speech",
                "harassment",
                "self_harm",
                "sexual_content",
                "violence",
                "illegal_activities",
                "personal_information"
            ]
            
            logger.info("Content moderation models loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading ML models: {str(e)}")
            raise
    
    async def moderate_text(self, text: str) -> Dict:
        """
        Analyze text content for inappropriate content.
        
        Args:
            text: The text content to analyze
            
        Returns:
            Dict containing moderation results
        """
        try:
            # Tokenize the input text
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
                padding=True
            ).to(self.device)
            
            # Get model predictions for each category
            results = {}
            for category in self.content_categories:
                # This is a simplified example - in practice, you'd use a fine-tuned model
                # or a more sophisticated approach for each category
                output = self.model(**inputs)
                logits = output.logits
                probs = torch.softmax(logits, dim=1)
                
                # For demonstration, using random scores
                # In a real implementation, you would have proper category-specific logic
                score = torch.rand(1).item()  # Random score for demo
                results[category] = {
                    "score": score,
                    "threshold": 0.7,  # Example threshold
                    "is_violation": score > 0.7
                }
            
            # Determine overall moderation decision
            has_violations = any(result["is_violation"] for result in results.values())
            
            return {
                "is_approved": not has_violations,
                "categories": results,
                "scores": {k: v["score"] for k, v in results.items()},
                "reason": "Violation found in content" if has_violations else "Content approved"
            }
            
        except Exception as e:
            logger.error(f"Error in text moderation: {str(e)}")
            # In case of error, we might want to flag for human review
            return {
                "is_approved": False,
                "categories": {},
                "scores": {},
                "reason": f"Error during moderation: {str(e)}"
            }
    
    async def moderate_image(self, image_bytes: bytes) -> Dict:
        """
        Analyze image content for inappropriate content.
        
        Args:
            image_bytes: Binary image data
            
        Returns:
            Dict containing moderation results
        """
        try:
            # In a real implementation, you would use a proper image moderation model
            # This is a placeholder that returns random results
            return {
                "is_approved": True,  # For demo purposes
                "categories": {
                    "explicit_content": {
                        "score": 0.1,
                        "threshold": 0.7,
                        "is_violation": False
                    },
                    "violence": {
                        "score": 0.2,
                        "threshold": 0.7,
                        "is_violation": False
                    },
                    "suggestive_content": {
                        "score": 0.3,
                        "threshold": 0.7,
                        "is_violation": False
                    }
                },
                "scores": {
                    "explicit_content": 0.1,
                    "violence": 0.2,
                    "suggestive_content": 0.3
                },
                "reason": "Content approved"
            }
            
        except Exception as e:
            logger.error(f"Error in image moderation: {str(e)}")
            return {
                "is_approved": False,
                "categories": {},
                "scores": {},
                "reason": f"Error during image moderation: {str(e)}"
            }

# Singleton instance
content_moderator = ContentModerator()

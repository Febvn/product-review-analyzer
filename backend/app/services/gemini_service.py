"""
Key Points Extraction Service using Google Gemini AI
Falls back to simple NLP techniques if API key is missing or call fails.
"""
import logging
import re
import google.generativeai as genai
from typing import List, Optional
from app.config import settings

logger = logging.getLogger(__name__)


class KeyPointsExtractor:
    """
    Key Points Extractor using Google Gemini AI.
    Falls back to simple NLP techniques if necessary.
    """
    
    def __init__(self):
        """Initialize the extractor with Gemini API key."""
        self.api_key = settings.GEMINI_API_KEY
        self.use_ai = False
        
        if self.api_key and not self.api_key.startswith("your_"):
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.use_ai = True
                logger.info("Gemini AI initialized for key points extraction")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {str(e)}")
                self.use_ai = False
        else:
            logger.warning("Gemini API Key not found or invalid. Using lightweight fallback mode.")
            self.use_ai = False
        
    def extract_key_points(self, review_text: str, product_name: Optional[str] = None) -> List[str]:
        """
        Extract key points from a product review.
        """
        if not review_text or not review_text.strip():
            raise ValueError("Review text cannot be empty")
        
        # Try AI first
        if self.use_ai:
            try:
                return self._extract_with_gemini(review_text, product_name)
            except Exception as e:
                logger.error(f"Gemini extraction failed: {str(e)}. Falling back to local method.")
                # Fallthrough to fallback
        
        # Fallback to local method
        return self._extract_fallback(review_text, product_name)

    def _extract_with_gemini(self, text: str, product_name: str = None) -> List[str]:
        """Extract key points using Gemini API."""
        product_context = f" for '{product_name}'" if product_name else ""
        prompt = f"""
        Analyze the following product review{product_context} and extract 3-5 brief, bulleted key points.
        Focus on product features, quality, and user sentiment.
        Return ONLY the bullet points, one per line, without asterisks or numbering.
        If the review is gibberish or has no meaningful content, return "No clear key points found".
        
        Review: "{text}"
        """
        
        response = self.model.generate_content(prompt)
        content = response.text.strip()
        
        # Process response into list
        points = [
            line.strip().replace('*', '').replace('-', '').strip() 
            for line in content.split('\n') 
            if line.strip()
        ]
        
        # Filter out empty or "No clear key points" results
        points = [p for p in points if len(p) > 3 and "No clear key points" not in p]
        
        if not points:
            return ["No clear key points found"]
            
        return points[:5]
    
    def _extract_fallback(self, text: str, product_name: Optional[str] = None) -> List[str]:
        """
        Extract key points using simple NLP techniques (Fallback).
        """
        # Clean the text
        text = text.strip()
        
        # Split into sentences
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 5]
        
        # If very short text (likely 1 sentence), just return it if it looks meaningful
        if len(sentences) == 1 and len(sentences[0]) < 100:
             return [sentences[0]]

        key_points = []
        
        # Keywords for detecting important points
        positive_keywords = [
            'great', 'excellent', 'amazing', 'love', 'best', 'good', 'nice', 
            'recommend', 'happy', 'perfect', 'fantastic', 'awesome', 'wonderful',
            'satisfied', 'worth', 'quality', 'fast', 'quick', 'easy',
            # Indonesian
            'bagus', 'mantap', 'suka', 'puas', 'keren', 'recommended', 'banget',
            'cepat', 'mudah', 'worth it', 'oke', 'ok', 'top', 'jos', 'mantul'
        ]
        
        negative_keywords = [
            'bad', 'poor', 'terrible', 'hate', 'worst', 'disappointed', 
            'broken', 'slow', 'expensive', 'waste', 'horrible', 'awful',
            'regret', 'useless', 'cheap', 'fake', 'defective', 'damaged',
            # Indonesian
            'jelek', 'kecewa', 'rusak', 'mahal', 'lambat', 'bohong', 'palsu',
            'tidak bagus', 'buruk', 'parah', 'zonk', 'nyesel', 'kapok', 'gak'
        ]
        
        feature_keywords = [
            'battery', 'screen', 'camera', 'design', 'quality', 'price', 
            'delivery', 'shipping', 'fast', 'size', 'color', 'package',
            'packaging', 'performance', 'speed', 'material', 'build',
            # Indonesian
            'baterai', 'layar', 'kamera', 'desain', 'kualitas', 'harga',
            'pengiriman', 'ongkir', 'ukuran', 'warna', 'kemasan', 'packing',
            'bahan', 'model', 'fitur'
        ]
        
        scored_sentences = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = 0
            
            # Check for keywords
            for kw in positive_keywords + negative_keywords:
                if kw in sentence_lower:
                    score += 2
            
            for kw in feature_keywords:
                if kw in sentence_lower:
                    score += 1
            
            # Bonus for sentences with product name
            if product_name and product_name.lower() in sentence_lower:
                score += 1
            
            # Penalty for very short sentences being key points (unless highly scored)
            if len(sentence) < 20: 
                score -= 1
            
            scored_sentences.append((sentence, score))
        
        # Sort by score
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        # Take top scoring sentences
        for sentence, score in scored_sentences:
            if score > 0 and len(sentence) < 300: # Removed min length strict check 
                # Capitalize first letter
                point = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence
                if point not in key_points:
                    key_points.append(point)
                if len(key_points) >= 5:
                    break
        
        # If no keywords matched but we have sentences, take the longest ones (usually more info)
        if not key_points and sentences:
             # Sort by length
            sentences_by_len = sorted(sentences, key=len, reverse=True)
            for sentence in sentences_by_len[:3]:
                 if len(sentence) < 300:
                    point = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence
                    key_points.append(point)

        # Final check
        if not key_points:
            key_points = ["Review text analysis completed"]
        
        logger.info(f"Extracted {len(key_points)} key points (Fallback)")
        return key_points


# Singleton instance
_extractor: Optional[KeyPointsExtractor] = None


def get_key_points_extractor() -> KeyPointsExtractor:
    """Get or create the key points extractor singleton."""
    global _extractor
    if _extractor is None:
        _extractor = KeyPointsExtractor()
    return _extractor


def extract_key_points(review_text: str, product_name: Optional[str] = None) -> List[str]:
    """
    Convenience function to extract key points.
    """
    extractor = get_key_points_extractor()
    return extractor.extract_key_points(review_text, product_name)

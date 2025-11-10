import re
import nltk
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class TextProcessor: #
    @staticmethod
    def clean_text(text):
        """Clean and preprocess text for summarization"""
        # Remove HTML tags
        soup = BeautifulSoup(text, 'html.parser')
        text = soup.get_text()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def estimate_reading_time(text, words_per_minute=200):
        """Estimate reading time in minutes"""
        word_count = len(text.split())
        return max(1, round(word_count / words_per_minute))
    
    @staticmethod
    def calculate_compression_ratio(original_text, summary_text):
        """Calculate compression ratio"""
        original_words = len(original_text.split())
        summary_words = len(summary_text.split())
        
        if original_words == 0:
            return 0
        
        return round((1 - (summary_words / original_words)) * 100, 2)
    
    @staticmethod
    def extract_key_phrases(text, max_phrases=5):
        """Extract potential key phrases (simple implementation)"""
        words = text.lower().split()
        # Simple stop words list
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return most frequent words as simple key phrases
        from collections import Counter
        return [phrase for phrase, count in Counter(meaningful_words).most_common(max_phrases)]

class ContentValidator:
    @staticmethod
    def validate_text_length(text, min_length=10):
        """Validate that text is long enough to summarize"""
        word_count = len(text.split())
        if word_count < min_length:
            raise ValueError(f"Text too short for summarization. Minimum {min_length} words required, got {word_count}.")
        return True
    
    @staticmethod
    def is_url(text):
        """Check if text is a URL"""
        url_pattern = re.compile(r'https?://\S+')
        return bool(url_pattern.match(text))
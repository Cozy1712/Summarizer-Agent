import openai
import logging
import uuid
from django.conf import settings
from .models import SummaryRequest
from .prompts import SUMMARY_PROMPTS, LENGTH_GUIDELINES
from .utils import TextProcessor, ContentValidator

logger = logging.getLogger(__name__)

class SummarizerService:
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        self.text_processor = TextProcessor()
        self.validator = ContentValidator()
    
    def generate_summary(self, text, summary_type='general', length='medium', include_bullet_points=True, include_key_points=True, language='english'):
        """Generate AI-powered summary"""
        
        try:
            #check if openai key is configured
            if not settings.OPENAI_API_KEY:
                raise ValueError("OpenAI API key is not configured.")
            # Validate input text
            self.validator.validate_text_length(text)
            
            # Clean text
            cleaned_text = self.text_processor.clean_text(text)
            
            # Get appropriate prompts
            if summary_type not in SUMMARY_PROMPTS:
                summary_type = 'general'
            
            system_prompt = SUMMARY_PROMPTS[summary_type]['system']
            user_prompt_template = SUMMARY_PROMPTS[summary_type]['user']
            
            # Format user prompt
            user_prompt = user_prompt_template.format(
                text=cleaned_text,
                length=length
            )
            
            # Add bullet points instruction if requested
            if include_bullet_points:
                user_prompt += "\nPlease use bullet points for better readability."
            
            # Generate summary using OpenAI
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=500 if length == 'short' else 800 if length == 'medium' else 1200,
                temperature=0.3  # Lower temperature for more consistent summaries
            )
            
            summary = response.choices[0].message.content.strip()
            
            # Calculate metrics
            word_count_original = len(cleaned_text.split())
            word_count_summary = len(summary.split())
            compression_ratio = self.text_processor.calculate_compression_ratio(cleaned_text, summary)
            
            result = {
                'summary': summary,
                'word_count_original': word_count_original,
                'word_count_summary': word_count_summary,
                'compression_ratio': compression_ratio,
                'reading_time_original': self.text_processor.estimate_reading_time(cleaned_text),
                'reading_time_summary': self.text_processor.estimate_reading_time(summary),
                'key_phrases': self.text_processor.extract_key_phrases(cleaned_text)
            }
            
            # Add bullet points flag to result
            if include_bullet_points:
                result['format'] = 'bullet_points'
            if include_key_points:
                result['key_points_included'] = True
                
            return result
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            raise
    
    def process_telex_message(self, message, user_id, conversation_id, options=None):
        """Process message from Telex.im and generate summary"""
        
        if options is None:
            options = {}
        
        summary_type = options.get('summary_type', 'general')
        length = options.get('length', 'medium')
        
        try:
            # Remove "summarizing..." prefix if present
            clean_message = message
            if message.startswith(('meeting:', 'news:', 'tech:', 'conv:', 'log:')):
                # Extract the actual content after the prefix
                parts = message.split(':', 1)
                if len(parts) > 1:
                    clean_message = parts[1].strip()
            
            # Generate summary
            result = self.generate_summary(clean_message, summary_type, length, options)
            
            # Save to database (optional)
            request_id = str(uuid.uuid4())
            summary_request = SummaryRequest.objects.create(
                request_id=request_id,
                user_id=user_id,
                conversation_id=conversation_id,
                original_text=clean_message[:10000],
                summary_type=summary_type,
                summary_length=length,
                summary=result['summary'],
                word_count_original=result['word_count_original'],
                word_count_summary=result['word_count_summary'],
                compression_ratio=result['compression_ratio']
            )
            
            # Format response for Telex.im
            response_message = self._format_telex_response(result, summary_type, length)
            
            return response_message
            
        except ValueError as e:
            return f"{str(e)} Please provide longer text for summarization."
        except Exception as e:
            logger.error(f"Error processing telex message: {str(e)}")
            return "I apologize, but I'm having trouble generating a summary right now. Please try again."
                
    def _format_telex_response(self, result, summary_type, length):
        """Format the summary response for Telex.im"""
        
        summary_type_display = dict(SummaryRequest.SUMMARY_TYPES).get(summary_type, 'Summary')
        
        response = f"""
    **{summary_type_display}** ({length})

    {result['summary']}

---
*Statistics:*
• Original: {result['word_count_original']} words
• Summary: {result['word_count_summary']} words  
• Compression: {result['compression_ratio']}% reduced
• Reading time saved: {result['reading_time_original'] - result['reading_time_summary']} minutes

*Key phrases:* {', '.join(result['key_phrases'][:3])}
"""
        
        return response.strip()
    
class QuickSummarizer:
    """Lightweight summarizer for simple cases without AI"""
    
    @staticmethod
    def extract_first_sentences(text, num_sentences=3):
        """Extract first few sentences as a simple summary"""
        sentences = text.split('. ')
        if len(sentences) <= num_sentences:
            return text
        
        summary = '. '.join(sentences[:num_sentences]) + '.'
        return summary
    
    @staticmethod
    def create_bullet_summary(text, max_bullets=5):
        """Create a simple bullet-point summary"""
        sentences = text.split('. ')
        key_sentences = sentences[:max_bullets]
        
        summary = "**Quick Summary:**\n\n"
        for i, sentence in enumerate(key_sentences, 1):
            if sentence.strip():
                summary += f"• {sentence.strip()}.\n"
        
        return summary
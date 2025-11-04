from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .serializers import WebhookSerializer, SummaryOptionsSerializer
from .services import SummarizerService, QuickSummarizer
from .utils import ContentValidator

logger = logging.getLogger(__name__)

@api_view(['POST'])
def telex_webhook(request):
    """
    Main webhook endpoint for Telex.im integration
    Handles summarization requests
    """
    try:
        serializer = WebhookSerializer(data=request.data)
        
        if serializer.is_valid():
            message = serializer.validated_data['message']
            user_id = serializer.validated_data['user_id']
            conversation_id = serializer.validated_data['conversation_id']
            options = serializer.validated_data.get('options', {})
            
            logger.info(f"Received summarization request from user {user_id}")
            
            # Check for quick commands
            if message.strip().lower() in ['/help', 'help']:
                return Response({
                    "response": get_help_message(),
                    "status": "success"
                })
            
            # Process the message using our summarizer
            summarizer = SummarizerService()
            response = summarizer.process_telex_message(message, user_id, conversation_id, options)
            
            return Response({
                "response": response,
                "status": "success",
                "user_id": user_id,
                "conversation_id": conversation_id
            })
            
        else:
            return Response({
                "error": "Invalid request data",
                "details": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
            
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        return Response({
            "error": "Internal server error",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def custom_summarize(request):
    """Custom summarization endpoint with options"""
    try:
        text = request.data.get('text', '')
        options_data = request.data.get('options', {})
        
        if not text:
            return Response({
                "error": "No text provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate options
        options_serializer = SummaryOptionsSerializer(data=options_data)
        if not options_serializer.is_valid():
            return Response({
                "error": "Invalid options",
                "details": options_serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        options = options_serializer.validated_data
        
        # Generate summary with explicit parameters
        summarizer = SummarizerService()
        result = summarizer.generate_summary(
            text, 
            summary_type=options.get('summary_type', 'general'),
            length=options.get('length', 'medium'),
            include_bullet_points=options.get('include_bullet_points', True),
            include_key_points=options.get('include_key_points', True),
            language=options.get('language', 'english')
        )
        
        return Response({
            "summary": result,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error in custom summarization: {str(e)}")
        return Response({
            "error": "Error generating summary",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        "status": "healthy",
        "service": "Summarizer Agent",
        "version": "1.0.0",
        "capabilities": ["general", "meeting", "news", "technical", "conversation", "log"]
    })

@api_view(['POST'])
def quick_summarize(request):
    """Quick summarization without AI"""
    try:
        text = request.data.get('text', '')
        
        if not text:
            return Response({
                "error": "No text provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        
        summarizer = QuickSummarizer()
        summary = summarizer.create_bullet_summary(text)
        
        return Response({
            "summary": summary,
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error in quick summarization: {str(e)}")
        return Response({
            "error": "Error generating quick summary",
            "details": str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_help_message():
    """Generate help message for users"""
    return """
**Telex Summarizer Agent Help**

I can summarize various types of content:

**Usage:**
Just send me any text and I'll summarize it automatically!

**Special Formats:**
- `meeting:` - For meeting notes
- `news:` - For news articles  
- `tech:` - For technical documents
- `conv:` - For conversations
- `log:` - For system logs

**Examples:**

meeting: Today we discussed Q3 goals...
news: Breaking: New AI model released...

**Quick Commands:**
- `help` - Show this message

I'll provide a summary with statistics and key points!
"""

# Workflow definition for Telex.im
@api_view(['GET'])
def workflow_definition(request):
    """Provide workflow definition for Telex.im"""
    workflow = {
        "active": True,
        "category": "productivity",
        "description": "An AI agent that summarizes long texts, meeting notes, news articles, and system logs",
        "id": "summarizer_agent_001",
        "long_description": """
        You are an intelligent summarization assistant that can process and condense various types of content into concise, informative summaries.

        Supported content types:
        - General texts and documents
        - Meeting notes and transcripts
        - News articles and reports
        - Technical documentation
        - Conversation threads
        - System logs and API responses

        When processing content:
        - Identify the main points and key information
        - Remove redundant and irrelevant details
        - Preserve important facts, figures, and context
        - Adapt summary length based on user needs
        - Provide statistics about the summarization

        You automatically detect content type or can be guided by user commands.
        """,
        "name": "summarizer_agent",
        "nodes": [
            {
                "id": "summarizer_agent",
                "name": "Summarizer Agent",
                "parameters": {},
                "position": [600, 150],
                "type": "a2a/django-a2a-node",
                "typeVersion": 1,
                "url": ""  # actual URL
            }
        ],
        "pinData": {},
        "settings": {
            "executionOrder": "v1"
        },
        "short_description": "AI-powered text summarization for various content types"
    }
    
    return Response(workflow)
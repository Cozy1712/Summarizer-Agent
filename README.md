# Telex Summarizer Agent

A Django REST Framework-based AI agent that provides intelligent text summarization for Telex.im. This agent can summarize various types of content including meeting notes, news articles, technical documents, conversation threads, and system logs.

## 🚀 Features

- 📊 **Multiple Summary Types**: General, meeting, news, technical, conversation, and log summaries
- 🔢 **Adjustable Length**: Short, medium, and long summary options
- 📈 **Detailed Statistics**: Word counts, compression ratios, and reading time estimates
- 🔍 **Key Phrase Extraction**: Automatic extraction of important keywords and phrases
- ⚡ **Quick Summarization**: Lightweight summarization without AI dependency
- 💬 **Natural Language Processing**: AI-powered understanding of context and content
- 🛡️ **Error Handling**: Comprehensive validation and error management
- 📝 **Conversation History**: Maintains context across multiple interactions

## 🏗️ Architecture

## 📋 Prerequisites

- Python 3.8+
- Django 4.2+
- OpenAI API key
- PostgreSQL (recommended) or SQLite

## 🛠️ Installation

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd telex-summarizer-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

2. Environment Configuration
Create a .env file in the project root:

# Django Settings
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com

# Database (PostgreSQL recommended)
DATABASE_URL=postgres://username:password@localhost:5432/telex_summarizer

# OpenAI API
OPENAI_API_KEY=your-openai-api-key-here

# Optional: For production
DJANGO_SETTINGS_MODULE=telex_agent.settings

3. Database Setup

# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

4. Start Development Server

python manage.py runserver

The application will be available at http://localhost:8000

🔌 API Endpoints
Base URL: http://localhost:8000/
1. Health Check
GET /health

Check service status and capabilities.

Response:

{
    "status": "healthy",
    "service": "Telex Summarizer Agent",
    "version": "1.0.0",
    "capabilities": [
        "general",
        "meeting",
        "news",
        "technical",
        "conversation",
        "log"
    ]
}

2. Telex Webhook
POST /webhook

Main endpoint for Telex.im integration.

Request: 
{
    "message": "Long text to summarize...",
    "user_id": "user_123",
    "conversation_id": "conv_456",
    "options": {
        "summary_type": "meeting",
        "length": "medium",
        "include_bullet_points": true,
        "include_key_points": true,
        "language": "english"
    }
}
Response:
{
    "response": "Meeting Summary (medium)\n\n• Reviewed Q3 performance: 15% user growth\n• Approved dark mode feature (Nov 15 release)\n• Allocated $50K for Q4 marketing\n\n---\n*Statistics:*\n• Original: 150 words (1 min read)\n• Summary: 45 words (0 min read)  \n• Compression: 70% reduced\n\n*Key phrases:* meeting, growth, feature, marketing, budget",
    "status": "success",
    "user_id": "user_123",
    "conversation_id": "conv_456"
}

3. Custom Summarize
POST /summarize

Advanced summarization with full options.

Request:

{
    "text": "Long text content here...",
    "options": {
        "summary_type": "technical",
        "length": "medium",
        "include_bullet_points": true,
        "include_key_points": true,
        "language": "english"
    }
}

4. Quick Summarize
POST /quick-summarize

Fast summarization without AI.

Request:

{
    "text": "Text to summarize quickly..."
}


5. Workflow Definition
GET /workflow

Get Telex.im workflow configuration.

🎯 Usage Examples

meeting: Team Meeting - October 15, 2024

Attendees: John, Sarah, Mike, Lisa

Discussion:
- Reviewed Q3 performance metrics: 15% growth in user acquisition
- Discussed new feature rollout for mobile app
- Budget approval for Q4 marketing campaign

Decisions:
- Move forward with dark mode feature (target release: Nov 15)
- Allocate $50,000 for Q4 marketing

🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request


🆘 Support
For support and questions:

Create an issue in the repository

Check Django logs for error details

Verify environment configuration

Test with Postman collection first
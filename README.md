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

## 🌐 API Endpoints

**Base URL:** `https://your-deployed-domain.com/api/`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/health` | ✅ Service status and capabilities check |
| POST | `/webhook` | 🤖 Main Telex.im AI summarization endpoint |
| POST | `/summarize` | ⚙️ Customizable summarization with advanced options |
| POST | `/quick-summarize` | ⚡ Fast bullet-point summarization without AI |
| GET | `/workflow` | 🔧 Telex.im integration configuration |

### Detailed Endpoint Descriptions

**GET** `/health` → Check service status and available capabilities  
**POST** `/webhook` → Process Telex.im messages and return AI-powered summaries  
**POST** `/summarize` → Advanced summarization with configurable options (length, type, format)  
**POST** `/quick-summarize` → Fast bullet-point summarization without AI dependency  
**GET** `/workflow` → Get Telex.im workflow configuration JSON 

## 🏗️ Architecture
telex-summarizer-agent/
├── manage.py
├── requirements.txt
├── telex_agent/
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│ └── asgi.py
├── summarizer_agent/
│ ├── init.py
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── serializers.py
│ ├── services.py
│ ├── utils.py
│ └── prompts.py
└── docs/
└── README.md
## 📋 Prerequisites

- Python 3.13+
- Django 5.2+
- OpenAI API key
- MYSQL (recommended) or SQLite

## 🛠️ Installation

### 1. Clone and Setup

```bash
git clone https://github.com/cozy/summarizer-agent
cd summarizer-agent
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
DATABASE_URL=postgres://username:password@localhost:5432/telex_summarizer
OPENAI_API_KEY=your-openai-api-key-here
DJANGO_SETTINGS_MODULE=telex_agent.settings
```

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Development Server

```bash
python manage.py runserver
```
The application will be available at http://localhost:8000

---
## 🔌 API Endpoints

### **Base URL** 
Server runs on:

👉 http://127.0.0.1:8000/

👉 cozy.pythonanywhere.com

---

1. Health Check
GET /health
Check service status and capabilities.

```bash
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
```
----
2. Telex Webhook
POST /webhook
Main endpoint for Telex.im integration.

```bash
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

----
Response:
{
    "response": "Meeting Summary (medium)\n\n• Reviewed Q3 performance: 15% user growth\n• Approved dark mode feature (Nov 15 release)\n• Allocated $50K for Q4 marketing\n\n---\n*Statistics:*\n• Original: 150 words (1 min read)\n• Summary: 45 words (0 min read)  \n• Compression: 70% reduced\n\n*Key phrases:* meeting, growth, feature, marketing, budget",
    "status": "success",
    "user_id": "user_123",
    "conversation_id": "conv_456"
}
```
3. Custom Summarize
POST /summarize
Advanced summarization with full options.
```bash
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
----
4. Quick Summarize
POST /quick-summarize
Fast summarization without AI.
```bash
Request:
{
    "text": "Text to summarize quickly..."
}
```
----

5. Workflow Definition
GET /workflow

Get Telex.im workflow configuration.
----
### 🔧 Telex.im Integration
Workflow Configuration
Use this JSON in Telex.im to integrate the summarizer agent:

```bash
{
    "active": true,
    "category": "productivity",
    "description": "An AI agent that summarizes long texts, meeting notes, news articles, and system logs",
    "id": "summarizer_agent_001",
    "long_description": "You are an intelligent summarization assistant that can process and condense various types of content into concise, informative summaries.\n\nSupported content types:\n- General texts and documents\n- Meeting notes and transcripts\n- News articles and reports\n- Technical documentation\n- Conversation threads\n- System logs and API responses\n\nWhen processing content:\n- Identify the main points and key information\n- Remove redundant and irrelevant details\n- Preserve important facts, figures, and context\n- Adapt summary length based on user needs\n- Provide statistics about the summarization",
    "name": "summarizer_agent",
    "nodes": [
        {
            "id": "summarizer_agent",
            "name": "Summarizer Agent",
            "parameters": {},
            "position": [600, 150],
            "type": "a2a/django-a2a-node",
            "typeVersion": 1,
            "url": "https://cozy.pythonanywhere/webhook"
        }
    ],
    "pinData": {},
    "settings": {
        "executionOrder": "v1"
    },
    "short_description": "AI-powered text summarization for various content types"
}
```

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
----
🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature/amazing-feature

Commit changes: git commit -m 'Add amazing feature'

Push to branch: git push origin feature/amazing-feature

Open a Pull Request
----

🆘 Support
For support and questions:

Create an issue in the repository

Check Django logs for error details

Verify environment configuration

Test with Postman collection first


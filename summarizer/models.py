from django.db import models

# Create your models here.

class SummaryRequest(models.Model):
    SUMMARY_TYPES = [
        ('general', 'General Summary'),
        ('meeting', 'Meeting Notes'),
        ('news', 'News Article'),
        ('technical', 'Technical Document'),
        ('conversation', 'Conversation Thread'),
        ('log', 'API/System Logs'),
    ]
    
    request_id = models.CharField(max_length=255, unique=True)
    user_id = models.CharField(max_length=255)
    conversation_id = models.CharField(max_length=255)
    original_text = models.TextField()
    summary_type = models.CharField(max_length=20, choices=SUMMARY_TYPES, default='general')
    summary_length = models.CharField(max_length=20, default='medium')  # short, medium, long
    summary = models.TextField()
    word_count_original = models.IntegerField()
    word_count_summary = models.IntegerField()
    compression_ratio = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'summary_requests'
        ordering = ['-created_at']

class SummaryTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    system_prompt = models.TextField()
    user_prompt_template = models.TextField()
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'summary_templates'
    
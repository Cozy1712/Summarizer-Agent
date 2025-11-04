from django.urls import path
from . import views

urlpatterns = [
    path('api/webhook', views.telex_webhook, name='telex-webhook'),
    path('api/health', views.health_check, name='health-check'),
    path('api/summarize', views.custom_summarize, name='custom-summarize'),
    path('api/quick-summarize', views.quick_summarize, name='quick-summarize'),
    path('api/workflow', views.workflow_definition, name='workflow-definition'),
]
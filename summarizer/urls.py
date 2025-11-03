from django.urls import path
from . import views

urlpatterns = [
    path('webhook/', views.telex_webhook, name='telex-webhook'),
    path('health/', views.health_check, name='health-check'),
    path('summarize/', views.custom_summarize, name='custom-summarize'),
    path('quick-summarize/', views.quick_summarize, name='quick-summarize'),
    path('workflow/', views.workflow_definition, name='workflow-definition'),
]
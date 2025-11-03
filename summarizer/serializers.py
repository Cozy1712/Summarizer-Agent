from rest_framework import serializers
from .models import SummaryRequest, SummaryTemplate

class WebhookSerializer(serializers.Serializer):
    message = serializers.CharField(required=True)
    user_id = serializers.CharField(required=True)
    conversation_id = serializers.CharField(required=True)
    channel_id = serializers.CharField(required=False)
    options = serializers.JSONField(required=False)

class SummaryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryRequest
        fields = '__all__'


class SummaryTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryTemplate
        fields = '__all__'


class SummaryOptionsSerializer(serializers.Serializer):
    summary_type = serializers.ChoiceField(
        choices=['general', 'meeting', 'news', 'technical', 'conversation', 'log'],
        default='general'
    )
    length = serializers.ChoiceField(
        choices=['short', 'medium', 'long'],
        default='medium'
    )
    include_bullet_points = serializers.BooleanField(default=True)
    include_key_points = serializers.BooleanField(default=True)
    language = serializers.CharField(default='english')
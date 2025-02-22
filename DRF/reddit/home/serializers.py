from rest_framework import serializers
from .models import Resume,JobDescription

class ResumeSerializer(serializers.ModelSerializer):
    skills = serializers.JSONField(required = False , allow_null=True)
    total_expericence = serializers.FloatField(required = False , allow_null=True)
    project_category = serializers.JSONField(required = False , allow_null=True)
    class Meta:
        model = Resume
        fields = '__all__'
    

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDescription
        fields = '__all__'
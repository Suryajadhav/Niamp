from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProjectSerializer(serializers.ModelSerializer):
    users = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Project
        fields = '__all__'
class CustomProjectSerializer(serializers.ModelSerializer):
    # Define the fields you want to include in the response
    created_by = serializers.CharField(source='created_by.username', read_only=True)  # Assuming created_by is a ForeignKey to User
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%S%z', read_only=True)  # Format to ISO 8601

    class Meta:
        model = Project
        fields = ['id', 'project_name', 'created_at','created_by'] 
class ClientSerializer(serializers.ModelSerializer):
    # projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    
    # Making `created_at`, `created_by`, and `id` read-only
    created_at = serializers.DateTimeField(read_only=True)
    created_by = serializers.StringRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Client
        fields = ['id', 'client_name', 'created_at', 'created_by']

class ClientSerializer1(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True, read_only=True)  # Include related projects
    created_by = serializers.StringRelatedField(read_only=True)  # Display username of created_by
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'client_name', 'projects', 'created_at', 'created_by', 'updated_at']
from rest_framework import serializers
from django.contrib.auth import get_user_model
from happy import models

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

    class Meta:
        model = User
        fields = ["id", "username", "password"]

class ContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contributor
        fields = "__all__"

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"

class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Issue
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = "__all__"


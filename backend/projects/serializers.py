from rest_framework import serializers

from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    task_count = serializers.IntegerField(source="tasks.count", read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "task_count", "created_at"]
        read_only_fields = ["created_at"]

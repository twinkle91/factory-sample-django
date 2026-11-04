from rest_framework import viewsets

from .models import Comment, Task
from .serializers import CommentSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    """Tasks, filterable with ?project=<id>, ?status=<status> and ?priority=<priority>."""

    queryset = Task.objects.select_related("project")
    serializer_class = TaskSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        project = params.get("project")
        if project:
            queryset = queryset.filter(project_id=project)

        status = params.get("status")
        if status:
            queryset = queryset.filter(status=status)

        priority = params.get("priority")
        if priority:
            queryset = queryset.filter(priority__iexact=priority)

        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """Comments, filterable with ?task=<id>."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        task = self.request.query_params.get("task")
        if task:
            queryset = queryset.filter(task_id=task)
        return queryset

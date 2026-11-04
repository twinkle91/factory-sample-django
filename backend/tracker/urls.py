from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import health
from projects.views import ProjectViewSet
from tasks.views import CommentViewSet, TaskViewSet

router = DefaultRouter()
router.register("projects", ProjectViewSet)
router.register("tasks", TaskViewSet)
router.register("comments", CommentViewSet)

urlpatterns = [
    path("health/", health, name="health"),
    path("api/", include(router.urls)),
    path("admin/", admin.site.urls),
]

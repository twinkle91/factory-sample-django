from django.test import TestCase

from projects.models import Project
from tasks.models import Comment, Task


class TaskModelTests(TestCase):
    def test_str_is_title(self):
        project = Project.objects.create(name="Website")
        task = Task.objects.create(project=project, title="Write copy")
        self.assertEqual(str(task), "Write copy")

    def test_deleting_project_deletes_tasks_and_comments(self):
        project = Project.objects.create(name="Website")
        task = Task.objects.create(project=project, title="Write copy")
        Comment.objects.create(task=task, author="sam", body="Hi")
        project.delete()
        self.assertFalse(Task.objects.exists())
        self.assertFalse(Comment.objects.exists())

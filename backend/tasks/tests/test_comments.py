from rest_framework.test import APITestCase

from projects.models import Project
from tasks.models import Comment, Task


class CommentApiTests(APITestCase):
    def setUp(self):
        project = Project.objects.create(name="Website")
        self.task = Task.objects.create(project=project, title="Write copy")
        self.other = Task.objects.create(project=project, title="Pick fonts")

    def test_add_comment(self):
        response = self.client.post(
            "/api/comments/",
            {"task": self.task.id, "author": "sam", "body": "First draft is up."},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(self.task.comments.count(), 1)

    def test_filter_comments_by_task(self):
        Comment.objects.create(task=self.task, author="sam", body="One")
        Comment.objects.create(task=self.other, author="ana", body="Two")
        bodies = [c["body"] for c in self.client.get(
            f"/api/comments/?task={self.task.id}"
        ).json()]
        self.assertEqual(bodies, ["One"])

    def test_comment_body_is_required(self):
        response = self.client.post(
            "/api/comments/", {"task": self.task.id, "author": "sam", "body": ""}
        )
        self.assertEqual(response.status_code, 400)

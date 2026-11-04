import datetime

from rest_framework.test import APITestCase

from projects.models import Project
from tasks.models import Task


class TaskApiTests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(name="Website")
        self.other = Project.objects.create(name="Mobile")

    def make_task(self, title, **kwargs):
        kwargs.setdefault("project", self.project)
        return Task.objects.create(title=title, **kwargs)

    def test_list_returns_json_list(self):
        response = self.client.get("/api/tasks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_task_with_defaults(self):
        response = self.client.post(
            "/api/tasks/", {"project": self.project.id, "title": "Write copy"}
        )
        self.assertEqual(response.status_code, 201)
        body = response.json()
        self.assertEqual(body["status"], "todo")
        self.assertEqual(body["priority"], "medium")
        self.assertIsNone(body["due_date"])

    def test_create_task_with_due_date(self):
        response = self.client.post(
            "/api/tasks/",
            {"project": self.project.id, "title": "Launch", "due_date": "2026-12-01"},
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["due_date"], "2026-12-01")

    def test_rejects_unknown_status(self):
        response = self.client.post(
            "/api/tasks/",
            {"project": self.project.id, "title": "Bad", "status": "blocked"},
        )
        self.assertEqual(response.status_code, 400)

    def test_filter_by_project(self):
        self.make_task("A")
        self.make_task("B", project=self.other)
        titles = [t["title"] for t in self.client.get(
            f"/api/tasks/?project={self.other.id}"
        ).json()]
        self.assertEqual(titles, ["B"])

    def test_filter_by_status(self):
        self.make_task("Open")
        self.make_task("Finished", status=Task.Status.DONE)
        titles = [t["title"] for t in self.client.get("/api/tasks/?status=done").json()]
        self.assertEqual(titles, ["Finished"])

    def test_filter_by_priority_ignores_case(self):
        self.make_task("Urgent", priority=Task.Priority.HIGH)
        self.make_task("Someday", priority=Task.Priority.LOW)
        titles = [t["title"] for t in self.client.get("/api/tasks/?priority=High").json()]
        self.assertEqual(titles, ["Urgent"])

    def test_update_status(self):
        task = self.make_task("Review", due_date=datetime.date(2026, 11, 30))
        response = self.client.patch(f"/api/tasks/{task.id}/", {"status": "in_progress"})
        self.assertEqual(response.status_code, 200)
        task.refresh_from_db()
        self.assertEqual(task.status, Task.Status.IN_PROGRESS)

    def test_delete_task(self):
        task = self.make_task("Obsolete")
        response = self.client.delete(f"/api/tasks/{task.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Task.objects.exists())

    def test_project_task_count(self):
        self.make_task("A")
        self.make_task("B")
        response = self.client.get(f"/api/projects/{self.project.id}/")
        self.assertEqual(response.json()["task_count"], 2)

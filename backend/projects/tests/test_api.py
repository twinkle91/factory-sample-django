from rest_framework.test import APITestCase

from projects.models import Project


class ProjectApiTests(APITestCase):
    def test_list_is_empty_json_list(self):
        response = self.client.get("/api/projects/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [])

    def test_create_and_list(self):
        response = self.client.post(
            "/api/projects/", {"name": "Website", "description": "Relaunch"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["task_count"], 0)

        names = [p["name"] for p in self.client.get("/api/projects/").json()]
        self.assertEqual(names, ["Website"])

    def test_name_must_be_unique(self):
        Project.objects.create(name="Website")
        response = self.client.post("/api/projects/", {"name": "Website"})
        self.assertEqual(response.status_code, 400)

    def test_projects_are_ordered_by_name(self):
        Project.objects.create(name="Zeta")
        Project.objects.create(name="Alpha")
        names = [p["name"] for p in self.client.get("/api/projects/").json()]
        self.assertEqual(names, ["Alpha", "Zeta"])

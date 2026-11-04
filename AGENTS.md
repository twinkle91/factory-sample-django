# Rules for agents in factory-sample-django (Backend)

## Stack

Python 3.12, Django 5.1 with Django REST Framework, SQLite, pip.

## You may

- Change application code in `backend/core/`, `backend/projects/`, `backend/tasks/` and `backend/tracker/` to deliver the story.
- Add tests for every behavior you change, using the Django test runner.

## You must not

- Edit MISSION.md, AGENTS.md, architecture.md, conventions.md, design.md or anything in `harness/`.
- Add, remove or upgrade dependencies, or edit lockfiles.
- Change CI, deployment or Docker files.
- Weaken or delete existing tests.
- Commit secrets or credentials.

## Checks

Run all commands from `backend/`.

- Install: `pip install -r requirements.txt -r requirements-dev.txt`
- Build: `python manage.py check`
- Test: `python manage.py test`
- Start: `python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000 --noreload` (serves on port 8000)

# Factory sample: Django task tracker

A small task tracker API (projects, tasks with status, priority and due date, and comments) built with
Django 5.1 and Django REST Framework on SQLite. It is a sample repository for onboarding into the
Software Factory: it exercises the repository scan, mapping tests, feature stories, migrations and bug triage
on a real Python project before client repositories are onboarded.

Nothing here needs network access at test time and there are no external services (no Postgres, no Redis).

## Layout

This is a monorepo with three projects, so the scan's monorepo detection has something to find.

| Folder | Stack | Factory support | What it is |
| --- | --- | --- | --- |
| `backend/` | Python 3.12, Django 5.1, DRF | Supported | The task tracker API |
| `web/` | Node 20, no dependencies | Supported | A static status page with `build` and `test` scripts |
| `services/notifier/` | Go 1.22 | Not supported (named, not run) | A placeholder reminder service |
| `docs/` | | | `sample-stories.md`: stories and a bug report to paste into Jira |

Inside `backend/`:

| Path | Contents |
| --- | --- |
| `manage.py` | Sets `DJANGO_SETTINGS_MODULE=tracker.settings` with `os.environ.setdefault` |
| `tracker/` | Settings, URLs, WSGI and ASGI |
| `core/` | `GET /health/` |
| `projects/` | `Project` model and `/api/projects/` |
| `tasks/` | `Task` and `Comment` models, `/api/tasks/` and `/api/comments/` |
| `<app>/tests/test_*.py` | Tests per app, runnable by dotted label, for example `tasks.tests.test_api` |

### API

| Method and path | Result |
| --- | --- |
| `GET /health/` | `{"status": "ok"}`; needs no database |
| `GET /api/projects/` | JSON list of projects, each with `task_count` |
| `GET /api/tasks/` | JSON list of tasks; filters `?project=<id>`, `?status=<status>`, `?priority=<priority>` |
| `GET /api/comments/` | JSON list of comments; filter `?task=<id>` |

Statuses are `todo`, `in_progress` and `done`; priorities are `low`, `medium` and `high`. Every list
endpoint returns a plain JSON list (no pagination). The API is open (no authentication) so smoke checks
need no credentials.

## Running it locally

```bash
cd backend
python3.12 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
python manage.py check
python manage.py test
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000 --noreload
```

The web page: `cd web && npm run build && npm test`.

## Mapping values for the Factory

### Mapping 1: the API (working directory `backend`)

| Setting | Value |
| --- | --- |
| Working directory | `backend` |
| Runtime | Python 3.12 (from `backend/.python-version`) |
| Environment variable | `DJANGO_SETTINGS_MODULE` = `tracker.settings` |
| Install | `pip install -r requirements.txt -r requirements-dev.txt` |
| Build | `python manage.py check` |
| Test | `python manage.py test` |
| Start | `python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000 --noreload` |
| Port | `8000` |
| Health path | `/health/` |
| Smoke checks | `GET /health/` → 200; `GET /api/projects/` → 200; `GET /api/tasks/` → 200 |

About the start command: the scan suggests `python manage.py runserver 0.0.0.0:8000 --noreload`. That serves
`/health/`, but the SQLite database has no tables until migrations run, so `/api/projects/` and `/api/tasks/`
answer 500. Running `migrate` first creates `db.sqlite3` in the working directory and makes every smoke path
pass. If you keep the suggested start command, keep only `/health/` as a smoke check.

### Mapping 2 (optional): the web page (working directory `web`)

Used by story SAMPLE-5, which names it with `Repo: tracker-web`. Give this mapping (or its repository
connection) the name `tracker-web`.

| Setting | Value |
| --- | --- |
| Working directory | `web` |
| Runtime | Node 20 |
| Install | none needed (no dependencies); `npm install` is harmless |
| Build | `npm run build` |
| Test | `npm test` |

The page is static, so leave start, port and health empty.

## Use-case checklist

1. **Repository scan and stack detection.** Scan `main`. Expect three projects: `backend` as Python 3.12 with
   Django (suggested commands as above), `web` as Node, and `services/notifier` as Go, named and marked
   unsupported rather than "unrecognized". The `DJANGO_SETTINGS_MODULE` variable should be suggested from
   `manage.py`.
2. **Required guidance files.** `AGENTS.md`, `MISSION.md`, `design.md` and `harness/harness.config.json` are
   deliberately absent. The Factory should list them as missing and offer the **Create Starter Files** pull
   request. Merge that pull request (into `dev` or `main`) before running stories.
3. **Mapping settings.** Enter the Mapping 1 values above.
4. **Test This Mapping.** Run it on `main`; install, build, test, start, health and the smoke checks should
   all pass as committed.
5. **Feature work.** Paste SAMPLE-1, SAMPLE-3 and SAMPLE-4 from [docs/sample-stories.md](docs/sample-stories.md)
   into Jira. SAMPLE-5 checks routing to the `web` mapping with a `Repo:` line. SAMPLE-6 is deliberately
   vague and should make the planner ask a clarification question.
6. **Bug triage.** SAMPLE-BUG-1 reports the seeded bug below. Expect the Factory to write a failing regression
   test first (narrowed with a dotted label such as `tasks.tests.test_api`), then fix it, then show the test
   passing.
7. **Migrations.** SAMPLE-2 adds an `archived` field to `Task`, so the change must include a new migration in
   `backend/tasks/migrations/`, and the sandbox runs it during tests.

## The seeded bug

`TaskViewSet.get_queryset` in `backend/tasks/views.py` filters status with an exact match
(`status=status`), while priority uses `priority__iexact`. So `GET /api/tasks/?status=Done` returns `[]` even
when done tasks exist. The existing tests only call `?status=done`, so they pass. The fix is a one-word change
(`status__iexact`) plus a regression test.

## Branches

- `main`: the committed baseline; Test This Mapping should pass here.
- `dev`: starts identical to `main`; use it as the base branch for Factory pull requests if you prefer not to
  target `main`.

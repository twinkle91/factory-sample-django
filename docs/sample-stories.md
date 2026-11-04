# Sample Jira stories

Ready-to-paste stories for exercising the Software Factory on this repository.
Paste the **Summary** into the Jira summary field and everything under
**Description** into the description. They are ordered from smallest to largest.

| Key in this file | Kind | Size | Exercises |
| --- | --- | --- | --- |
| SAMPLE-1 | Story | S | Plain feature work on `backend` |
| SAMPLE-2 | Story | M | A schema change with a migration |
| SAMPLE-3 | Story | M | Query annotation, list serializer change |
| SAMPLE-4 | Story | M | A new custom endpoint |
| SAMPLE-5 | Story | S | Routing with a `Repo:` line to the `web` mapping |
| SAMPLE-6 | Story | ? | Deliberately ambiguous: the planner should ask |
| SAMPLE-BUG-1 | Bug | S | Regression-test-first bug triage |

---

## SAMPLE-1: Search tasks by title

**Summary:** Search tasks by title

**Description:**

As a team member I want to search the task list by title so I can find a task without scrolling.

Acceptance criteria:
- `GET /api/tasks/?search=<text>` returns only tasks whose title contains `<text>`, ignoring case.
- `search` combines with the existing `project`, `status` and `priority` filters.
- An empty `search` value returns the unfiltered list.
- Tests cover a match, a case-insensitive match, no match, and a combination with `project`.

---

## SAMPLE-2: Archive tasks (needs a migration)

**Summary:** Let tasks be archived and hide archived tasks by default

**Description:**

As a project lead I want to archive finished tasks so the task list stays short, without deleting history.

Acceptance criteria:
- Tasks have an `archived` boolean field, default `false`, included in the task API's responses and writable with PATCH.
- `GET /api/tasks/` leaves archived tasks out by default.
- `GET /api/tasks/?archived=true` returns only archived tasks; `?archived=all` returns both.
- A Django migration adds the field; existing tasks become unarchived.
- `python manage.py makemigrations --check --dry-run` reports no missing migrations.
- Tests cover the default, both filter values, and archiving through PATCH.

---

## SAMPLE-3: Comment counts in the task list

**Summary:** Show how many comments each task has in the task list

**Description:**

As a team member I want to see how many comments a task has from the list, so I know where the discussion is.

Acceptance criteria:
- Every task in `GET /api/tasks/` and `GET /api/tasks/<id>/` has a read-only `comment_count`.
- The count is computed in the same database query as the list (an annotation), not one query per task.
- A test asserts the count, and a test with `assertNumQueries` shows the list does not issue a query per task.

---

## SAMPLE-4: Overdue tasks endpoint

**Summary:** Add an endpoint that lists overdue tasks

**Description:**

As a project lead I want a list of overdue tasks so I can chase them in stand-up.

Acceptance criteria:
- `GET /api/tasks/overdue/` returns tasks whose `due_date` is before today (UTC) and whose status is not `done`.
- Tasks without a due date are never overdue.
- Results are ordered by `due_date`, oldest first, then by `id`.
- The endpoint accepts the existing `project` filter.
- Tests pin "today" so they do not depend on the date they run on.

---

## SAMPLE-5: Status summary on the web page (routes to the web mapping)

**Summary:** Show a task status summary on the web status page

**Description:**

Repo: tracker-web

As a visitor to the status page I want to see how many tasks are in each status.

Acceptance criteria:
- `web/src/index.html` shows a "To do / In progress / Done" summary area.
- The summary uses `summarize` and `statusLabel` from `web/src/format.mjs`.
- `npm run build` still writes `web/dist/index.html`.
- `npm test` covers any new helper.
- Only files under `web/` change.

> `tracker-web` must be the name of the second mapping (working directory `web`); see the README.
> If both mappings of this repository answer to the same name, the Factory reports that the story
> matched more than one mapping, which is itself a useful case to see.

---

## SAMPLE-6: Make tasks better (deliberately ambiguous)

**Summary:** Improve task priorities

**Description:**

Priorities don't really work for us. Make them better so the team can see what matters. It should be
like what the other team has.

> Expected outcome: the planner asks a clarification question (which behaviour is wrong, what "the other
> team" uses, whether this is a new field, new values, sorting, or UI) instead of guessing.

---

## SAMPLE-BUG-1: Status filter ignores tasks when the status is capitalised

**Type:** Bug

**Summary:** Task list status filter returns nothing for "Done"

**Description:**

Steps to reproduce:
1. Create a project and a task with status `done`.
2. Call `GET /api/tasks/?status=done`: the task is returned.
3. Call `GET /api/tasks/?status=Done`: an empty list `[]` is returned.

Expected: the status filter ignores case, as the `priority` filter already does (`?priority=High` works).

Actual: `?status=Done` and `?status=DONE` return no tasks. Our reporting dashboard sends capitalised
statuses, so every "Done" column is empty.

Area: `backend/tasks/views.py`, `TaskViewSet.get_queryset`. Existing tests live in
`backend/tasks/tests/test_api.py`; the regression test can be run alone with
`python manage.py test tasks.tests.test_api`.

# Architecture of factory-sample-django (Backend)

## Overview

A Django 5.1 project that exposes a REST API through Django REST Framework. The API covers projects, tasks and comments. It runs from the `backend/` directory and serves on port 8000.

## Folders

- `backend/core/`: <!-- TODO: what lives in backend/core -->
- `backend/projects/`: <!-- TODO: what lives in backend/projects -->
- `backend/tasks/`: <!-- TODO: what lives in backend/tasks -->
- `backend/tracker/`: <!-- TODO: what lives in backend/tracker -->

## Data and integrations

State lives in a SQLite database. The start command applies migrations (`python manage.py migrate --noinput`) before the server starts.

<!-- TODO: APIs this app calls, where the database file is configured, and how data flows between apps. -->

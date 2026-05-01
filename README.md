# BiFrost — Travel Planning Web Application

BiFrost is a Django 6 web application for building and managing travel itineraries. Users create trips, attach typed events (transportation, food, entertainment), track budgets, receive alerts, and export itineraries to PDF.

---

## Table of Contents

1. [Project Architecture](#project-architecture)
2. [Prerequisites](#prerequisites)
3. [Quick Start (Docker)](#quick-start-docker)
4. [Environment Configuration](#environment-configuration)
5. [Running Without Docker](#running-without-docker)
6. [Seeding Demo Data](#seeding-demo-data)
7. [Configuration Files & Deployment Scripts](#configuration-files--deployment-scripts)
8. [Builder Design Pattern](#builder-design-pattern)
9. [Code Organisation & Structure](#code-organisation--structure)
10. [Code Quality Notes](#code-quality-notes)

---

## Project Architecture

```
BiFrost_docker/                  ← repo root
├── compose.yaml                 ← Docker Compose (web + db + cache)
├── .env.dev                     ← development environment variables
├── README.Docker.md             ← Docker-specific quick start (generated)
└── BiFrost_SWD_django/          ← Django project root
    ├── Dockerfile
    ├── pyproject.toml           ← uv / PEP 517 project manifest
    ├── requirements.txt         ← pinned dependency list
    ├── manage.py
    ├── seed.py                  ← demo data seeder
    ├── BiFrost/                 ← Django settings package
    │   ├── settings.py
    │   ├── urls.py
    │   ├── asgi.py
    │   └── wsgi.py
    ├── itinerary/               ← core app (trips + events)
    │   ├── models.py            ← Itinerary, Event, and three specialisations
    │   ├── builders.py          ← Builder Design Pattern implementation ← NEW
    │   ├── views.py             ← HTTP handlers (updated to use Builder)
    │   └── urls.py
    ├── finance/                 ← budget tracking
    ├── users/                   ← auth, registration, profile
    └── utility/                 ← Place, Alert, map/alert views
```

**Service stack (Docker Compose)**

| Service | Image / Build | Port |
|---------|--------------|------|
| `web`   | Local Dockerfile (Python 3.14 + uv) | `8000` |
| `db`    | `postgres:16.5` | internal |
| `cache` | `redis:7.2.4` | `6379` |

---

## Prerequisites

| Tool | Minimum version | Notes |
|------|----------------|-------|
| Docker Desktop | 24+ | Includes Docker Compose v2 |
| Git | any | |
| (optional) Python | 3.14 | Only needed for local dev without Docker |
| (optional) uv | latest | `pip install uv` or `curl -LsSf https://astral.sh/uv/install.sh \| sh` |

---

## Quick Start (Docker)

### 1 — Clone and enter the repo

```bash
git clone <your-repo-url> BiFrost_docker
cd BiFrost_docker
```

### 2 — Verify the dev environment file

A ready-to-use `.env.dev` is included for local development. **Do not commit real secrets** — replace `SECRET_KEY` before deploying to any shared environment.

```bash
cat .env.dev          # review values; change SECRET_KEY if desired
```

### 3 — Build and start all services

```bash
docker compose up --build
```

This command:
- Builds the Django image using `BiFrost_SWD_django/Dockerfile`
- Starts PostgreSQL (`db`) and Redis (`cache`) containers
- Runs `manage.py runserver 0.0.0.0:8000` inside the `web` container

### 4 — Apply database migrations

Open a second terminal:

```bash
docker compose exec web uv run manage.py migrate
```

### 5 — Create a superuser (optional — or use seed data instead)

```bash
docker compose exec web uv run manage.py createsuperuser
```

### 6 — Open the application

Navigate to **http://localhost:8000** in your browser.

The root URL redirects to `/users/login/` if unauthenticated, or to `/itinerary/` if logged in.

---

## Environment Configuration

All runtime configuration is injected via environment variables loaded from `.env.dev` (development) or your production secrets manager.

| Variable | Description | Default in `.env.dev` |
|----------|-------------|----------------------|
| `DEBUG` | Enable Django debug mode | `True` |
| `SECRET_KEY` | Django cryptographic key | dev placeholder — **change in prod** |
| `ALLOWED_HOSTS` | Comma-separated host list | `localhost,127.0.0.1,0.0.0.0` |
| `DATABASE` | `postgres` or `sqlite` | `postgres` |
| `SQL_ENGINE` | Django DB backend | `django.db.backends.postgresql` |
| `SQL_DATABASE` | PostgreSQL database name | `dev_db` |
| `SQL_USER` | PostgreSQL user | `dev_user` |
| `SQL_PASSWORD` | PostgreSQL password | `dev_password` |
| `SQL_HOST` | PostgreSQL host (Docker service name) | `db` |
| `SQL_PORT` | PostgreSQL port | `5432` |
| `REDIS_HOST` | Redis host (Docker service name) | `cache` |
| `REDIS_PORT` | Redis port | `6379` |

Settings are read by `django-environ` in `BiFrost/settings.py`.

---

## Running Without Docker

For local development without containers (SQLite fallback):

```bash
cd BiFrost_SWD_django

# Install uv if not present
pip install uv

# Create virtual environment and install dependencies
uv sync

# Point to SQLite by overriding DATABASE in your shell
export DATABASE=sqlite
export SECRET_KEY="local-dev-key"
export ALLOWED_HOSTS="localhost,127.0.0.1"
export REDIS_HOST="localhost"
export REDIS_PORT="6379"

# Apply migrations
uv run manage.py migrate

# Start development server
uv run manage.py runserver
```

> **Note:** Redis must still be available locally (or you can configure Django's cache to use `LocMemCache` for fully offline development).

---

## Seeding Demo Data

`seed.py` inserts four fully-populated demo trips (Paris, London, New York, Roan Mountain) with events, budgets, and alerts under the user `root` / `root1234`.

```bash
# With Docker running:
cat BiFrost_SWD_django/seed.py | docker compose exec -T web uv run manage.py shell

# Without Docker:
cat seed.py | uv run manage.py shell
```

The seeder is wrapped in `transaction.atomic()` — it will roll back entirely on any error and cleans previous demo data before inserting fresh records.

---

## Configuration Files & Deployment Scripts

### `compose.yaml` — Docker Compose

Defines three services: `web`, `db`, `cache`. Key decisions:

- **Volume mounts** on `web` map individual app directories from host into the container, enabling live-reload during development without a full rebuild.
- `depends_on` ensures the database and cache are started before Django.
- The `postgres_data` named volume persists database state between `docker compose down` / `up` cycles.

**Production hardening checklist for `compose.yaml`:**
- Add `healthcheck` to `db` and make `web` wait on `condition: service_healthy`
- Remove host-volume mounts (copy files into image instead)
- Use Docker secrets or a `.env.prod` for credentials

### `BiFrost_SWD_django/Dockerfile`

- Base image: `python:3.14-slim-bookworm`
- System dependencies: `libpq-dev` (PostgreSQL), `libcairo2` + friends (PDF generation via xhtml2pdf/pycairo)
- Package manager: `uv` binary copied from `ghcr.io/astral-sh/uv:0.8.14`
- Dependency install: `uv sync --frozen` (respects `uv.lock` for reproducible builds)
- Entry point: `uv run manage.py runserver 0.0.0.0:8000`

### `pyproject.toml`

PEP 517 project manifest consumed by `uv`. Lists direct (non-pinned) dependencies. `uv` generates `uv.lock` from this for reproducible installs.

### `requirements.txt`

Fully-pinned flat dependency list — used for auditing and as a reference. The canonical install source for Docker is `pyproject.toml` + `uv.lock`.

### `BiFrost/settings.py`

Central Django configuration. Notable patterns:
- `django-environ` reads all secrets from environment variables — no hardcoded credentials in code
- Database engine switches between PostgreSQL and SQLite based on `DATABASE` env var
- Redis is configured as the Django cache backend

### `.env.dev`

Non-secret development defaults committed to the repository. **Never commit `.env.prod`** or any file containing real secrets.

---

## Builder Design Pattern

### Why the original code needed updating

`itinerary/views.py` (`add_event`) contained a three-branch `if/elif/else` block that called `TransportationEvent.objects.create()`, `FoodEvent.objects.create()`, and `EntertainmentEvent.objects.create()` directly. This means:

- Object construction was tightly coupled to HTTP request handling
- Adding a new event type required editing view code
- Unit-testing construction logic required mocking an HTTP request

### Pattern implementation

Two new files implement the full Builder pattern:

**`itinerary/builders.py`**

```
EventBuilder (Abstract)
    ├── set_base_fields()   ← shared step: populates common Event fields
    └── build()             ← abstract: must be implemented by each subclass

TransportationEventBuilder(EventBuilder)
    └── build(transport_type=1) → TransportationEvent

FoodEventBuilder(EventBuilder)
    └── build(menu="")      → FoodEvent

EntertainmentEventBuilder(EventBuilder)
    └── build()             → EntertainmentEvent

EventDirector
    └── construct(...)      ← drives set_base_fields() → build() in order
```

**`itinerary/views_updated.py`** — updated `add_event` view

```python
# Select builder by event type
BuilderClass = builder_map.get(event_type, EntertainmentEventBuilder)
director = EventDirector(BuilderClass(itinerary=trip))

# Director drives the full construction sequence
director.construct(
    name=..., category=..., cost=...,
    **product_kwargs,          # transport_type / menu forwarded here
)
```

### Applying the changes

Replace `itinerary/views.py` with `itinerary/views_updated.py`:

```bash
cp BiFrost_SWD_django/itinerary/views_updated.py \
   BiFrost_SWD_django/itinerary/views.py
```

No migrations are needed — the pattern only affects Python construction logic, not database schema.

---

## Code Organisation & Structure

### Strengths

**Clear Django app boundaries.** Each domain concern lives in its own app with a single responsibility:

| App | Responsibility |
|-----|---------------|
| `itinerary` | Core trip and event data |
| `finance` | Budget tracking |
| `users` | Auth, registration, profile |
| `utility` | Places, map views, alerts |

**Multi-table inheritance is used appropriately.** `TransportationEvent`, `FoodEvent`, and `EntertainmentEvent` each extend `Event` via Django's concrete model inheritance, keeping the shared schema DRY while allowing type-specific fields.

**Environment-driven configuration.** No secrets in code; `django-environ` handles all runtime configuration cleanly.

**Reproducible dependency management.** `uv` with a lockfile ensures every environment gets identical packages.

### Issues & Recommendations

#### 1. Duplicate `@login_required` decorator on `index`

`itinerary/views.py` applies `@login_required` twice to the `index` view. The second decorator is redundant and should be removed.

```python
# Before (bug)
@login_required
@login_required
def index(request): ...

# After
@login_required
def index(request): ...
```

#### 2. Missing `__str__` on utility models

`Place` and `Alert` in `utility/models.py` have no `__str__`, making them appear as `Place object (1)` in the Django admin and shell.

```python
# Add to Place
def __str__(self):
    return f"{self.name} ({self.category})"

# Add to Alert
def __str__(self):
    return f"[{self.type.upper()}] {self.message[:50]}"
```

#### 3. `itinerary_events` counter is not maintained

`Itinerary.itinerary_events` is a static `IntegerField(default=0)` that is never incremented or decremented. Consider replacing it with a `@property` that queries the related manager:

```python
@property
def event_count(self) -> int:
    return self.events.count()
```

#### 4. Missing `healthcheck` in `compose.yaml`

The `db` service has no healthcheck, and `web` uses only `depends_on` (which only waits for the container to start, not for PostgreSQL to be ready). This can cause connection errors on first boot.

Add a healthcheck to the `db` service:

```yaml
db:
  image: postgres:16.5
  healthcheck:
    test: ["CMD", "pg_isready", "-U", "dev_user", "-d", "dev_db"]
    interval: 5s
    retries: 5
  ...

web:
  depends_on:
    db:
      condition: service_healthy
```

#### 5. `seed.py` ships with a hardcoded default password

`user.set_password("root1234")` is acceptable for demo seeding, but should be noted clearly in documentation and never used in production. Consider reading the password from an environment variable.

#### 6. `.venv` directory committed to the repository

The `.venv/` directory inside `BiFrost_SWD_django/` is committed to git (visible in the zip). It should be excluded via `.gitignore`. The existing `.gitignore` likely already lists `.venv` — verify the entry is present and that git has not already tracked those files.

```bash
git rm -r --cached BiFrost_SWD_django/.venv
```

#### 7. `finance/views.py` lacks ownership check

`dashboard()` fetches an `Itinerary` by `id` without filtering by `user`, meaning any authenticated user can view any trip's budget by guessing the `trip_id`. Add the ownership guard:

```python
# Before
trip = get_object_or_404(Itinerary, id=trip_id)

# After
trip = get_object_or_404(Itinerary, id=trip_id, user=request.user)
```

---

## App URL Map

| Prefix | App | Key Routes |
|--------|-----|-----------|
| `/` | root redirect | → `/itinerary/` or `/users/login/` |
| `/itinerary/` | itinerary | index, add, edit, add-event, export-pdf |
| `/finance/` | finance | budget dashboard per trip |
| `/utility/` | utility | map view, alerts view |
| `/users/` | users | register, login, logout, profile, change-password |
| `/admin/` | Django admin | superuser management |

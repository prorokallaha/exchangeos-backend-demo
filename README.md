# ExchangeOS Backend

Backend prototype for ExchangeOS built with FastAPI, async SQLAlchemy and Alembic.

## Stack

- FastAPI
- SQLAlchemy 2.0 (async)
- PostgreSQL
- Alembic
- Pydantic v2

## Architecture

Project structure is split into clear layers:

- `src/app/api` – HTTP routers and dependencies
- `src/app/services` – business logic
- `src/app/db/repositories` – database access layer
- `src/app/db/models` – SQLAlchemy models
- `src/app/schemas` – request/response schemas
- `src/app/db/migrations` – Alembic migrations

## Implemented modules

- organizations
- organization members
- requisites
- ledger
- orders
- settings
- stats
- RBAC and permissions
- bootstrap services

## Local setup

### Requirements

- Python 3.12+
- PostgreSQL 14+

### Install

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
copy .env.example .env

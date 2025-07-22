# Personal Semantic Engine

A personal knowledge management system with semantic search capabilities.

## Database Setup

1. Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

2. Update the database connection string in `.env`:

```
DATABASE_URL=postgresql+asyncpg://username:password@localhost/personal_semantic_engine
```

3. Initialize the database:

```bash
python scripts/init_db.py
```

## Running Tests

To run the repository integration tests:

```bash
# Install test dependencies
pip install pytest pytest-asyncio

# Run tests
pytest tests/infrastructure/repositories/
```

## Database Migrations

To create a new migration:

```bash
alembic revision -m "description_of_changes" --autogenerate
```

To apply migrations:

```bash
alembic upgrade head
```

To downgrade:

```bash
alembic downgrade -1  # Go back one revision
```
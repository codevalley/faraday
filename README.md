# Personal Semantic Engine (Faraday)

A comprehensive system that allows users to create a unified, searchable repository of their personal data by ingesting plain English thoughts and connecting to various structured APIs. The system builds a semantic understanding of the user's life and provides both timeline visualization and intelligent search capabilities across all personal data sources.

## Features

- Natural language thought input with entity extraction
- Semantic search with filtering by entity types
- Timeline visualization of personal data
- Clean architecture with domain-driven design
- API-first design with FastAPI

## Architecture

The project follows clean architecture principles with the following layers:

- **Domain Layer**: Core business entities and interfaces
- **Application Layer**: Use cases that orchestrate business logic
- **Infrastructure Layer**: Implementations of interfaces
- **API Layer**: FastAPI routes and controllers

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Poetry

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Copy `.env.example` to `.env` and update with your configuration
4. Run database migrations:
   ```bash
   alembic upgrade head
   ```
5. Start the application:
   ```bash
   poetry run python -m src.main
   ```

## Development

### Code Quality

The project uses the following tools for code quality:

- Black for code formatting
- isort for import sorting
- mypy for type checking
- flake8 for linting
- pytest for testing

Run all checks:

```bash
poetry run black .
poetry run isort .
poetry run mypy src/
poetry run flake8 src/
poetry run pytest
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
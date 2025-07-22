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

## LLM Configuration

The Personal Semantic Engine uses LiteLLM to provide a unified interface for multiple LLM providers. This allows you to easily switch between different models from OpenAI, Anthropic, DeepSeek, and others.

### Environment Variables

Configure your LLM settings in the `.env` file:

```
# LLM Configuration
LLM_MODEL=gpt-4                # Default model to use
LLM_TEMPERATURE=0.0            # Temperature for generation (0.0 = deterministic)
LLM_MAX_TOKENS=4096            # Maximum tokens to generate

# API Keys for different providers
OPENAI_API_KEY=your-openai-api-key-here
ANTHROPIC_API_KEY=your-anthropic-api-key-here
DEEPSEEK_API_KEY=your-deepseek-api-key-here
```

### Customizing Prompts

All prompts are stored as external files in `src/infrastructure/llm/prompts/` and can be modified without changing code:

1. **System Prompts**: `entity_extraction_system.txt` - Contains instructions for the LLM
2. **User Prompts**: `entity_extraction.txt` - Template for user prompts with placeholders
3. **JSON Schemas**: `entity_extraction_schema.json` - Schema for structured LLM output

### Adding New LLM Providers

To add support for a new LLM provider:

1. Update `src/infrastructure/llm/config/llm_config.json` with the new provider and models
2. Add the appropriate API key to your `.env` file
3. The LiteLLM library will handle the rest!

Example configuration:

```json
{
  "providers": {
    "new-provider": {
      "models": {
        "new-model-name": {
          "description": "Description of the new model",
          "max_tokens": 4096,
          "default_temperature": 0.0
        }
      }
    }
  }
}
```

### Testing Different Models

To test different LLM models:

1. Update the `LLM_MODEL` environment variable in `.env`
2. Or specify the model directly when creating the LLMService:

```python
llm_service = LLMService(model="claude-3-opus")
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
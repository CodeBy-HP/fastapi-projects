# Tests Directory

This directory contains automated tests for the Movie Collection API.

## Running Tests

### Install test dependencies
```bash
pip install pytest pytest-asyncio httpx
```

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run specific test file
```bash
pytest tests/test_movies.py -v
```

### Run specific test
```bash
pytest tests/test_movies.py::test_create_movie_success -v
```

### Run with coverage
```bash
pip install pytest-cov
pytest --cov=app tests/
```

## Test Structure

- `conftest.py` - Pytest configuration and fixtures
- `test_movies.py` - Tests for movie endpoints

## Note

These tests require a running MongoDB instance. Make sure MongoDB is running before executing tests.

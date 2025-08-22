# Test Execution Guide

This document provides comprehensive instructions for running tests in the Threads Analytics project.

## Prerequisites

1. **Install Dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

2. **Environment Setup**
```bash
# Create test environment file (optional)
cp .env.example .env.test
# Note: Tests use mock data, so API keys are not required for testing
```

## Running Tests

### Quick Test Commands

```bash
# Run all tests
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py

# Run specific test class
pytest tests/test_analytics.py::TestContentAnalyzer

# Run specific test function
pytest tests/test_data_collector.py::TestThreadsAPIClient::test_calculate_engagement_rate_normal
```

### Test Categories

#### 1. Unit Tests
Test individual functions and classes in isolation:

```bash
# Data collector tests
pytest tests/test_data_collector.py -v

# Analytics engine tests  
pytest tests/test_analytics.py -v

# Database models tests
pytest tests/test_models.py -v

# Configuration tests
pytest tests/test_config.py -v
```

#### 2. Integration Tests
Test API endpoints and full workflows:

```bash
# API endpoint tests
pytest tests/test_api.py -v

# Database integration tests
pytest tests/test_models.py -v
```

### Coverage Reports

```bash
# Run tests with coverage
pytest --cov=. --cov-report=html

# View coverage report
open htmlcov/index.html

# Terminal coverage report
pytest --cov=. --cov-report=term-missing
```

### Advanced Test Options

```bash
# Run tests in parallel (install pytest-xdist first)
pip install pytest-xdist
pytest -n auto

# Run tests with specific markers
pytest -m "not slow"  # Skip slow tests

# Stop on first failure
pytest -x

# Run last failed tests only
pytest --lf

# Run tests matching pattern
pytest -k "test_analyze"
```

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                # Shared test fixtures and configuration
├── test_data_collector.py     # ThreadsAPIClient unit tests
├── test_analytics.py          # ContentAnalyzer & MetricsCalculator tests
├── test_models.py             # Database model tests
├── test_config.py             # Configuration tests
└── test_api.py                # FastAPI endpoint integration tests
```

## Test Coverage Goals

- **Unit Tests**: All core business logic functions
- **Integration Tests**: All API endpoints and database operations  
- **Error Handling**: Exception cases and edge conditions
- **Mocking**: External API calls (Threads API, OpenAI API)

## Mock Data

Tests use mock data and don't require actual API keys:

- **Threads API**: Mocked with sample post and metrics data
- **OpenAI API**: Mocked with sample analysis responses
- **Database**: In-memory SQLite for isolation

## Continuous Integration

For CI/CD pipelines, use:

```bash
# Install dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run tests with coverage
pytest --cov=. --cov-report=xml

# Upload coverage to codecov (optional)
# codecov -f coverage.xml
```

## Debugging Tests

```bash
# Run tests with debugging output
pytest -s -v

# Drop into debugger on failure
pytest --pdb

# Print statements in tests
pytest -s tests/test_specific.py::test_function

# Capture logs
pytest --log-cli-level=DEBUG
```

## Performance Testing

```bash
# Time test execution
pytest --durations=10

# Profile test performance  
pip install pytest-profiling
pytest --profile
```

## Test Data Cleanup

Tests automatically handle cleanup:
- Temporary databases are created and destroyed per test
- Mock API calls don't persist data
- No external API calls are made during testing

## Common Issues

### 1. Import Errors
```bash
# Ensure you're in the project root directory
cd /path/to/threads_analytics
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest
```

### 2. Database Connection Issues
```bash
# Tests use in-memory SQLite, but if issues occur:
rm -f test_*.db
pytest
```

### 3. Async Test Issues
```bash
# Ensure pytest-asyncio is installed
pip install pytest-asyncio
pytest
```

## Writing New Tests

### Test Naming Convention
- File: `test_<module_name>.py`
- Class: `Test<ClassName>`
- Function: `test_<function_description>`

### Example Test Structure
```python
import pytest
from unittest.mock import patch, MagicMock

class TestYourClass:
    
    @pytest.fixture
    def sample_data(self):
        return {"key": "value"}
    
    def test_your_function_success(self, sample_data):
        # Arrange
        expected = "expected_result"
        
        # Act
        result = your_function(sample_data)
        
        # Assert
        assert result == expected
    
    @pytest.mark.asyncio
    async def test_async_function(self):
        # Test async functions
        result = await async_function()
        assert result is not None
```

## Test Metrics

Current test coverage targets:
- **Overall Coverage**: >90%
- **Critical Functions**: 100%
- **API Endpoints**: 100%
- **Error Paths**: >80%

Run `pytest --cov=. --cov-report=term-missing` to see current coverage.
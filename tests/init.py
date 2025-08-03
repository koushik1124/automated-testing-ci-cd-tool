# tests/__init__.py
"""
This package contains all tests for the automated testing CI/CD tool.
"""

import pytest
import tempfile
import json
import os
from typing import Dict, Any, Generator
from io import TextIOWrapper

# Define common test fixtures that can be used across all test modules
@pytest.fixture
def sample_valid_data() -> Dict[str, Any]:
    """Fixture providing valid sample data for testing."""
    return {"name": "Test Sample", "value": 42}

@pytest.fixture
def sample_invalid_data() -> Dict[str, Any]:
    """Fixture providing invalid sample data for testing."""
    return {"name": "", "value": -1}

@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """Fixture that creates a temporary JSON file and returns its path."""
    # Create a temporary file in text mode
    with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.json', encoding='utf-8') as temp_file:
        # Write sample data to the file
        sample_data = {"name": "Temp File Test", "value": 100}
        json.dump(sample_data, temp_file)
        file_path = temp_file.name
    
    # Yield the file path
    yield file_path
    
    # Cleanup: delete the temporary file after tests
    os.unlink(file_path)

@pytest.fixture
def mock_api_response() -> Dict[str, Any]:
    """Fixture providing a mock API response for testing."""
    return {
        "userId": 1,
        "id": 1,
        "title": "delectus aut autem",
        "completed": False
    }

# Configure pytest options
def pytest_configure(config):
    """Configure pytest with custom options."""
    # Add custom markers
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "unit: marks tests as unit tests"
    )

# Custom pytest hooks
def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers based on test names."""
    for item in items:
        # Add 'unit' marker to unit tests
        if "test_core" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Add 'integration' marker to integration tests
        if "test_integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
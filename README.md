Automated Testing CI/CD Tool

A Python-based tool for automated testing and data processing with configurable behavior and CI/CD integration.

What This Project Does

This tool provides a framework for:
- Processing structured data from files and API responses
- Validating input data according to defined rules
- Automating file operations and API interactions
- Running automated tests to ensure functionality
- Integrating with CI/CD pipelines through GitHub Actions

Implemented Features

Core Functionality
- Data Validation: Validates input data structure and content
- Data Processing: Transforms data using configurable parameters
- File Processing: Reads and processes JSON files
- API Integration: Fetches and processes data from REST APIs
- Configuration System: JSON-based configuration for customization
- Logging: Configurable logging with console and file output

Testing Framework
- Unit Tests: Testing core functions in isolation
- Integration Tests: Testing combined functionality
- Test Coverage: Coverage reporting with HTML output
- Test Fixtures: Reusable test data and temporary file handling

CI/CD Integration
- GitHub Actions Workflow: Automated testing on multiple Python versions
- Test Coverage Reporting: Integration with Codecov for coverage tracking
- Multi-Version Testing: Supports Python 3.8, 3.9, 3.10, and 3.11

Command-Line Interface
- Flexible Arguments: Support for different input sources and configurations
- Verbose Logging: Optional detailed output for debugging
- Custom Configuration: Ability to specify alternative configuration files

Installation

Prerequisites
- Python 3.8 or higher
- pip package manager

Setup
1. Clone the repository:
   git clone https://github.com/yourusername/automated-testing-ci-cd-tool.git
   cd automated-testing-ci-cd-tool

2. Create a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install -r requirements.txt

4. Install the package:
   pip install -e .

5. Create configuration file:
   cp config.example.json config.json

Usage

Basic Usage
Run the tool with default settings:
python -m src.main

Process Data from a File
# Create a sample data file
echo '{"name": "Test Data", "value": 10}' > sample.json

# Process the file
python -m src.main --input sample.json

Process Data from an API
python -m src.main --api https://jsonplaceholder.typicode.com/todos/1

Custom Configuration
# Use a custom configuration file
python -m src.main --config myconfig.json

# Enable verbose logging
python -m src.main --verbose

Configuration

The tool uses a JSON configuration file (config.json) to customize behavior. Key sections include:

- api_endpoints: Default API endpoints for testing
- test_data: Sample data for testing
- logging: Logging configuration (level, format, file output)
- processing: Processing parameters (multiplier, retries, timeout)
- output: Output settings (directory, format)

Example configuration:
{
  "test_data": {
    "valid_sample": {
      "name": "Test Data",
      "value": 42
    }
  },
  "logging": {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "file": "app.log"
  },
  "processing": {
    "default_multiplier": 2
  }
}

Testing

Run All Tests
pytest tests/ -v

Run Tests with Coverage
pytest tests/ --cov=src --cov-report=html

View Coverage Report
Open reports/coverage/index.html in your browser.

Run Specific Test Categories
# Run only unit tests
pytest tests/test_core.py -v

# Run only integration tests
pytest tests/test_integration.py -v

Project Structure

automated-testing-ci-cd-tool/
├── .github/
│   └── workflows/
│       └── ci.yml            # GitHub Actions workflow
├── .vscode/
│   └── settings.json         # VS Code configuration
├── tests/
│   ├── __init__.py           # Test package initialization
│   ├── conftest.py           # Pytest configuration
│   ├── test_core.py          # Unit tests
│   └── test_integration.py   # Integration tests
├── src/
│   ├── __init__.py           # Source package initialization
│   ├── main.py               # Main application logic
│   ├── automation.py         # File and API automation
│   └── utils.py              # Utility functions
├── config.example.json       # Configuration template
├── config.json               # Application configuration
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── README.txt                # This file
├── .gitignore                # Git ignore rules
└── reports/
    └── coverage/             # Test coverage reports

Key Components

src/main.py
- Entry point for the application
- Handles command-line arguments
- Orchestrates data processing
- Configures logging

src/utils.py
- Configuration loading and management
- File system utilities
- Environment variable handling

src/automation.py
- File automation functions
- API interaction functions
- Error handling for external operations

tests/
- Comprehensive test suite
- Test fixtures for reusable components
- Integration tests for end-to-end functionality

How It Works

1. Configuration Loading: The tool loads settings from config.json (or a custom file)
2. Input Handling: Accepts data from files, APIs, or uses sample data
3. Validation: Checks input data against defined rules
4. Processing: Applies transformations (e.g., multiplying values)
5. Output: Returns processed results with status information
6. Logging: Records operations and errors at configured levels

Error Handling

The tool handles common error scenarios:
- Missing or invalid configuration files
- File not found errors
- Invalid JSON data
- Network request failures
- Invalid input data

Each error is logged with descriptive messages for debugging.

Development

Adding New Features
1. Implement functionality in the appropriate module
2. Add corresponding tests
3. Update configuration schema if needed
4. Update documentation

Running Tests Locally
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_core.py

Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

License

This project is licensed under the MIT License.
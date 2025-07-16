# Test Suite for Competitive Analysis Crew

This directory contains comprehensive unit tests for the Competitive Analysis Crew's custom tools.

## Test Structure

### `test_tools.py`
Comprehensive unit tests for all custom tools:

- **TestCompetitiveSearchTool**: Tests for the competitive intelligence search functionality
- **TestMarketAnalysisTool**: Tests for market positioning and landscape analysis
- **TestReportValidationTool**: Tests for report quality validation
- **TestToolIntegration**: Integration tests for tool interactions

## Running Tests

### Basic Test Execution
```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_tools.py

# Run specific test class
python -m pytest tests/test_tools.py::TestCompetitiveSearchTool

# Run specific test method
python -m pytest tests/test_tools.py::TestCompetitiveSearchTool::test_basic_search_execution
```

### Coverage Testing
```bash
# Run tests with coverage
python -m pytest tests/ --cov=src/Competitive_analysis_crew/tools --cov-report=term-missing

# Generate HTML coverage report
python -m pytest tests/ --cov=src/Competitive_analysis_crew/tools --cov-report=html
```

### Using the Test Runner Script
```bash
# Basic test run
python run_tests.py

# With coverage
python run_tests.py --coverage

# With verbose output
python run_tests.py --verbose

# Run specific test
python run_tests.py --test tests/test_tools.py::TestCompetitiveSearchTool
```

## Test Coverage

Current test coverage: **98%**

- CompetitiveSearchTool: 100% coverage
- MarketAnalysisTool: 98% coverage  
- ReportValidationTool: 97% coverage

## Test Categories

### Unit Tests
- Individual tool functionality testing
- Input validation and error handling
- Output format verification
- Edge case handling

### Integration Tests
- Tool interaction workflows
- End-to-end data flow testing
- Cross-tool compatibility

## Test Data

Tests use realistic mock data that simulates actual competitive analysis scenarios:

- Company profiles with various characteristics
- Industry-specific market trends
- Realistic business intelligence reports
- Validation scenarios with different quality levels

## Adding New Tests

When adding new functionality to the tools, ensure you:

1. Add corresponding unit tests
2. Test both success and error scenarios
3. Verify input validation
4. Check output formatting
5. Maintain high test coverage (>95%)

## Dependencies

Test dependencies are defined in `pyproject.toml`:

- `pytest>=8.0.0`: Test framework
- `pytest-cov>=4.0.0`: Coverage reporting
- Standard library modules for mocking and testing

## Continuous Integration

These tests are designed to run in CI/CD environments and provide:

- Fast execution (< 5 seconds)
- Reliable results with deterministic test data
- Clear error reporting
- Coverage metrics for quality assurance
# Testing Guide - Ecosystem Simulation

This document provides comprehensive information about testing the ecosystem simulation project.

## 📋 Test Overview

The project includes extensive unit tests covering all major components:

- **🌍 World Module**: Grid operations, time management, lighting calculations
- **🌱 Plant Module**: Growth mechanics, reproduction, environmental interactions  
- **🔄 Simulation Module**: Update cycles, population control, atmospheric management
- **📱 Visualization Module**: ASCII rendering, character mapping, display formatting
- **⚙️ Main Module**: Command-line parsing, simulation execution flow

## 🚀 Running Tests

### Quick Start

```bash
# Run all tests with basic output
python -m unittest discover tests

# Run all tests with verbose output
python -m unittest discover tests -v

# Run tests using our custom test suite
python tests/test_suite.py

# Run tests with coverage reporting
python tests/test_suite.py --coverage
```

### Using the Test Suite Runner

Our custom test suite provides additional features:

```bash
# Run all tests
python tests/test_suite.py

# Run tests for specific module
python tests/test_suite.py --module world
python tests/test_suite.py --module plant
python tests/test_suite.py --module simulation
python tests/test_suite.py --module visualization
python tests/test_suite.py --module main

# Run with verbose output
python tests/test_suite.py --verbose

# Run with coverage reporting
python tests/test_suite.py --coverage
```

### Using Pytest (Alternative)

If you prefer pytest, install the requirements and run:

```bash
# Install testing dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=ecosystem_sim

# Run specific test file
pytest tests/test_world.py

# Run specific test method
pytest tests/test_world.py::TestWorld::test_world_initialization
```

## 📊 Test Coverage

Our test suite aims for high coverage across all modules:

### Coverage Goals
- **World Module**: 95%+ coverage
- **Plant Module**: 90%+ coverage  
- **Simulation Module**: 90%+ coverage
- **Visualization Module**: 85%+ coverage
- **Main Module**: 80%+ coverage

### Coverage Reporting

```bash
# Generate coverage report
python tests/test_suite.py --coverage

# View HTML coverage report
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
```

## 🧪 Test Structure

### Test Organization

```
tests/
├── __init__.py              # Test package initialization
├── test_world.py           # World module tests (18 test methods)
├── test_plant.py           # Plant module tests (15 test methods)
├── test_simulation.py      # Simulation module tests (16 test methods)
├── test_visualization.py   # Visualization module tests (20 test methods)
├── test_main.py            # Main module tests (12 test methods)
├── test_suite.py           # Custom test runner
└── TESTING.md              # This documentation
```

### Test Categories

#### 🔧 Unit Tests
- Test individual methods and functions in isolation
- Use mocking for external dependencies
- Fast execution (< 1 second per test)

#### 🔗 Integration Tests  
- Test interaction between components
- Use real objects when possible
- Moderate execution time (1-5 seconds per test)

#### 🎯 Edge Case Tests
- Test boundary conditions
- Test error handling
- Test with invalid inputs

## 📝 Test Examples

### Basic Test Structure

```python
class TestWorld(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.world = World(10, 8)
    
    def test_world_initialization(self):
        """Test world is properly initialized with correct dimensions."""
        self.assertEqual(self.world.width, 10)
        self.assertEqual(self.world.height, 8)
        # ... more assertions
```

### Using Mocks

```python
@patch('ecosystem_sim.main.time.sleep')
@patch('ecosystem_sim.main.Simulation')
def test_main_with_mocks(self, mock_simulation, mock_sleep):
    """Test main function with mocked dependencies."""
    mock_sim = Mock()
    mock_simulation.return_value = mock_sim
    
    main()
    
    mock_simulation.assert_called_once()
```

### Testing Random Behavior

```python
def test_reproduction_success_rate(self):
    """Test reproduction has reasonable success rate over many attempts."""
    self.plant.age = 50
    self.plant.size = 0.8
    
    total_offspring = 0
    for _ in range(100):  # Multiple attempts
        offspring = self.plant.reproduce()
        total_offspring += len(offspring)
    
    # Should have some reproduction success
    self.assertGreater(total_offspring, 0)
```

## 🛠️ Writing New Tests

### Guidelines

1. **Test Naming**: Use descriptive names starting with `test_`
   ```python
   def test_plant_growth_with_optimal_conditions(self):
   def test_world_lighting_at_noon(self):
   ```

2. **Arrange-Act-Assert Pattern**:
   ```python
   def test_example(self):
       # Arrange: Set up test data
       plant = Plant((5, 5), self.world)
       
       # Act: Execute the code under test
       result = plant.grow()
       
       # Assert: Verify the results
       self.assertTrue(result)
   ```

3. **Use setUp and tearDown**:
   ```python
   def setUp(self):
       """Set up test fixtures before each test method."""
       self.world = World(10, 10)
   
   def tearDown(self):
       """Clean up after each test method."""
       # Usually not needed for our tests
       pass
   ```

4. **Test Edge Cases**:
   ```python
   def test_world_bounds_checking(self):
       """Test behavior at world boundaries."""
       # Test negative coordinates
       self.assertIsNone(self.world.get_cell(-1, 0))
       
       # Test out of bounds coordinates  
       self.assertIsNone(self.world.get_cell(100, 100))
   ```

### Testing Checklist

When adding new tests, ensure:

- [ ] Test covers the happy path (normal operation)
- [ ] Test covers edge cases and boundary conditions  
- [ ] Test covers error conditions and invalid inputs
- [ ] Test uses appropriate assertions
- [ ] Test is independent (doesn't rely on other tests)
- [ ] Test has clear, descriptive name and docstring
- [ ] Test runs quickly (< 5 seconds)

## 🐛 Debugging Failed Tests

### Common Issues

1. **Random Test Failures**: Use seeds or multiple attempts for random behavior
2. **Timing Issues**: Mock time-dependent functions
3. **State Pollution**: Ensure tests are independent
4. **Mock Configuration**: Verify mocks are set up correctly

### Debugging Tips

```bash
# Run single test with verbose output
python -m unittest tests.test_world.TestWorld.test_specific_method -v

# Run with Python debugger
python -m pdb -m unittest tests.test_world.TestWorld.test_specific_method

# Print debug information
def test_debug_example(self):
    print(f"Plant health: {self.plant.health}")
    print(f"World state: {self.world.get_cell(0, 0)}")
    # ... test code
```

## 📈 Performance Testing

### Benchmarking Tests

```python
import time

def test_simulation_performance(self):
    """Test simulation performance with large population."""
    start_time = time.time()
    
    # Run simulation steps
    for _ in range(100):
        self.sim.update()
    
    elapsed = time.time() - start_time
    self.assertLess(elapsed, 5.0)  # Should complete in < 5 seconds
```

## 🔧 Test Configuration

### Environment Variables

```bash
# Set test environment
export ECOSYSTEM_TEST_MODE=1

# Disable random seeding for consistent tests
export ECOSYSTEM_DETERMINISTIC=1
```

### Custom Test Settings

Modify `tests/test_suite.py` to adjust:
- Test verbosity
- Coverage thresholds  
- Timeout values
- Output formatting

## 📚 Additional Resources

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Pytest documentation](https://docs.pytest.org/)
- [Testing best practices](https://docs.python-guide.org/writing/tests/)

## 🤝 Contributing Tests

When contributing new features:

1. Write tests before implementing features (TDD)
2. Ensure all tests pass before submitting
3. Maintain or improve overall coverage
4. Follow existing test patterns and naming conventions
5. Document complex test scenarios

---

**Happy Testing! 🧪**
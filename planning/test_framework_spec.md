# Link Loader Test Framework Specification

**Author**: Bob (Engineering)  
**Date**: Today  
**Version**: 1.0

## Overview

This document specifies the automated testing framework for Link Loader, built on top of the text-based Ren'Py player.

## Architecture

```
┌─────────────────────┐
│   Test Runner CLI   │
├─────────────────────┤
│   TestRunner Core   │
├─────────────────────┤
│  RenpyGamePlayer    │
├─────────────────────┤
│    Game Scripts     │
└─────────────────────┘
```

## Core Components

### 1. TestRunner Class

```python
class TestRunner:
    """Automated test runner for Ren'Py games"""
    
    def __init__(self, game_path: str):
        self.game_path = game_path
        self.player = RenpyGamePlayer(game_path)
        self.test_results = []
        self.coverage_data = {}
    
    def run_test_scenario(self, scenario: TestScenario) -> TestResult:
        """Execute a single test scenario"""
        pass
    
    def run_all_tests(self) -> TestReport:
        """Run all defined test scenarios"""
        pass
    
    def assert_variable(self, name: str, expected: Any) -> bool:
        """Assert a variable has expected value"""
        pass
    
    def assert_label_reached(self, label: str) -> bool:
        """Assert a specific label was reached"""
        pass
    
    def generate_coverage_report(self) -> CoverageReport:
        """Generate test coverage report"""
        pass
```

### 2. Test Scenario Definition

```python
@dataclass
class TestScenario:
    """Defines a single test scenario"""
    name: str
    description: str
    choices: List[Choice]
    assertions: List[Assertion]
    
@dataclass
class Choice:
    """A choice to make at a menu"""
    menu_text: str  # Text to match in menu
    option: int     # Which option to choose (1-based)
    
@dataclass
class Assertion:
    """An assertion to check"""
    type: AssertionType
    target: str
    expected: Any
    label: Optional[str] = None  # When to check
```

### 3. Test Definition Format

Tests will be defined in YAML format for easy maintenance:

```yaml
name: "Test Cosmonaut Path"
description: "Verify the cosmonaut character creation and approach"
choices:
  - menu: "Choose your character background"
    option: 1  # Welcome Comrade
  - menu: "What will you do?"
    option: 1  # Robot language reply
  - menu: "How would you approach this?"
    option: 1  # Cosmonaut approach
assertions:
  - type: variable
    target: cos
    expected: 2
  - type: variable
    target: approach
    expected: "cosmonaut"
  - type: label_reached
    target: scene3_cosmonaut
```

## Test Categories

### 1. Path Coverage Tests
- Test all character creation options
- Test all approach paths
- Test all ending choices
- Verify all major story branches

### 2. Variable State Tests
- Character stats (COS/COW/COD)
- Story variables (approach, mission)
- Game state consistency
- Save/load integrity

### 3. Dialogue Tests
- Character appearance consistency
- Conditional dialogue triggers
- Menu option availability
- Text variable substitution

### 4. Error Handling Tests
- Invalid choices
- Missing labels
- Undefined variables
- Script errors

## Implementation Plan

### Phase 1: Core Framework (Week 1)
1. Implement TestRunner base class
2. Create test scenario loader
3. Add basic assertions
4. Simple CLI interface

### Phase 2: Advanced Features (Week 2)
1. Coverage tracking
2. HTML report generation
3. Parallel test execution
4. CI/CD integration

### Phase 3: Extended Testing (Future)
1. Performance benchmarks
2. Memory usage tracking
3. Regression detection
4. A/B test support

## Usage Examples

### Command Line Interface

```bash
# Run all tests
python test_runner.py

# Run specific test suite
python test_runner.py --suite character_creation

# Run with coverage report
python test_runner.py --coverage

# Run in CI mode (exit codes)
python test_runner.py --ci
```

### Test Definition

```python
# tests/test_character_creation.py
from linkloader.testing import TestRunner, TestScenario

def test_cosmonaut_path():
    runner = TestRunner("../game")
    
    scenario = TestScenario(
        name="Cosmonaut Path",
        choices=[
            Choice("Choose your character", 1),
            Choice("What will you do?", 1)
        ],
        assertions=[
            VariableAssertion("cos", 2),
            VariableAssertion("approach", "cosmonaut")
        ]
    )
    
    result = runner.run_test_scenario(scenario)
    assert result.passed
```

## Report Format

### Console Output
```
Link Loader Test Results
========================
✓ Test Cosmonaut Path.............. PASSED
✓ Test Cowboy Path................. PASSED
✗ Test Coder Path.................. FAILED
  - Expected cod=2, got cod=1

Coverage: 87% (26/30 labels reached)
Total: 2/3 passed
```

### HTML Report
- Interactive flow chart showing tested paths
- Detailed assertion results
- Variable state snapshots
- Performance metrics
- Coverage heatmap

## Integration Points

### 1. CI/CD Pipeline
```yaml
# .github/workflows/test.yml
name: Game Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - run: python test_runner.py --ci
      - uses: actions/upload-artifact@v2
        with:
          name: test-report
          path: test_report.html
```

### 2. Pre-commit Hooks
```bash
#!/bin/bash
# .git/hooks/pre-commit
python test_runner.py --quick
```

### 3. Development Workflow
- Run tests locally before committing
- View coverage reports to find untested paths
- Add tests for new features
- Use TDD for dialogue branches

## Future Enhancements

1. **Visual Testing**: Screenshot comparison for UI changes
2. **Performance Testing**: Track frame rates and load times
3. **Accessibility Testing**: Screen reader compatibility
4. **Localization Testing**: Multi-language support
5. **Player Analytics**: Track real player choices vs test coverage

## Conclusion

This testing framework will significantly improve Link Loader's quality and development speed by catching bugs early and ensuring comprehensive coverage of all game paths.
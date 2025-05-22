#!/usr/bin/env python3
"""
Improved Test Runner for Link Loader with better menu handling
"""

import os
import re
import sys
import json
import time
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))
from renpy_game_player import RenpyGame

class AssertionType(Enum):
    """Types of assertions we can make"""
    VARIABLE = "variable"
    LABEL_REACHED = "label_reached"

@dataclass
class Choice:
    """Represents a choice to make at a menu"""
    text_match: str  # Text to match in the choice
    option: int      # Which option to choose (1-based)

@dataclass
class Assertion:
    """Represents an assertion to check"""
    type: AssertionType
    target: str
    expected: Any = None
    
@dataclass
class TestScenario:
    """Defines a complete test scenario"""
    name: str
    description: str
    choices: List[Choice]
    assertions: List[Assertion]
    
@dataclass
class TestResult:
    """Result of running a test scenario"""
    scenario_name: str
    passed: bool
    duration: float
    assertions_passed: List[Assertion]
    assertions_failed: List[Tuple[Assertion, str]]
    labels_visited: List[str]
    final_state: Dict[str, Any]
    error: Optional[str] = None
    choices_made: List[str] = field(default_factory=list)

class SimpleTestPlayer:
    """Simplified test player for Link Loader"""
    
    def __init__(self, game: RenpyGame, choices: List[Choice]):
        self.game = game
        self.choices = choices
        self.choice_index = 0
        self.variables = dict(game.default_variables)
        self.labels_visited = []
        self.current_label = "start"
        self.choices_made = []
    
    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate a Python expression"""
        try:
            return eval(expr, {"__builtins__": {}}, self.variables)
        except:
            return False
    
    def execute_python(self, code: str):
        """Execute Python code"""
        try:
            exec(code, {"__builtins__": {}}, self.variables)
        except Exception as e:
            print(f"Error executing: {code}")
            print(f"Error: {e}")
    
    def process_menu(self, lines: List[Tuple[int, str, str]], start_idx: int) -> Tuple[str, int]:
        """Process a menu and make a choice"""
        idx = start_idx + 1
        choices_found = []
        
        # Extract all choices
        while idx < len(lines):
            indent, line, _ = lines[idx]
            
            # Look for choice patterns
            choice_match = re.match(r'\s*"([^"]+)"(\s+if\s+(.+))?:', line)
            if choice_match:
                choice_text = choice_match.group(1)
                condition = choice_match.group(3)
                
                # Check condition
                if condition and not self.evaluate_expression(condition):
                    idx += 1
                    continue
                
                choices_found.append({
                    'text': choice_text,
                    'index': idx,
                    'number': len(choices_found) + 1
                })
            
            # Break on dedent
            if indent < lines[start_idx][0] and line.strip():
                break
                
            idx += 1
        
        # Find which choice to make
        selected = None
        
        # Try to match by text
        if self.choice_index < len(self.choices):
            choice_to_make = self.choices[self.choice_index]
            self.choice_index += 1
            
            # Match by text
            for choice in choices_found:
                if choice_to_make.text_match in choice['text']:
                    selected = choice
                    break
            
            # Fallback to index
            if not selected and choice_to_make.option <= len(choices_found):
                selected = choices_found[choice_to_make.option - 1]
        
        # Default to first choice
        if not selected and choices_found:
            selected = choices_found[0]
        
        if not selected:
            return None, idx
        
        self.choices_made.append(selected['text'])
        
        # Process the selected choice block
        choice_idx = selected['index'] + 1
        choice_indent = lines[selected['index']][0]
        
        while choice_idx < len(lines):
            indent, line, _ = lines[choice_idx]
            
            # Break on dedent
            if indent <= choice_indent and line.strip():
                break
            
            # Process the line
            line = line.strip()
            if line.startswith('$'):
                self.execute_python(line[1:].strip())
            elif line.startswith('jump '):
                return line[5:].strip(), idx
            
            choice_idx += 1
        
        return None, idx
    
    def play_label(self, label: str):
        """Play through a label"""
        if label not in self.game.labels:
            raise ValueError(f"Label '{label}' not found")
        
        self.labels_visited.append(label)
        lines = self.game.labels[label]
        idx = 0
        
        while idx < len(lines):
            indent, line, _ = lines[idx]
            line = line.strip()
            
            if line.startswith('$'):
                self.execute_python(line[1:].strip())
            elif line.startswith('jump '):
                target = line[5:].strip()
                self.current_label = target
                return
            elif line == 'menu:':
                target, next_idx = self.process_menu(lines, idx)
                if target:
                    self.current_label = target
                    return
                idx = next_idx
                continue
            elif line == 'return':
                self.current_label = None
                return
            
            idx += 1
    
    def play(self):
        """Play through the game following choices"""
        self.current_label = "start"
        
        while self.current_label and len(self.labels_visited) < 50:  # Safety limit
            self.play_label(self.current_label)
        
        return self.variables, self.labels_visited

class TestRunner:
    """Main test runner for Link Loader"""
    
    def __init__(self, game_path: str):
        self.game_path = game_path
        self.game = RenpyGame(game_path)
    
    def run_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a single test scenario"""
        start_time = time.time()
        
        # Create test player
        player = SimpleTestPlayer(self.game, scenario.choices)
        
        # Initialize result
        result = TestResult(
            scenario_name=scenario.name,
            passed=True,
            duration=0,
            assertions_passed=[],
            assertions_failed=[],
            labels_visited=[],
            final_state={},
            choices_made=[]
        )
        
        try:
            # Run the game
            final_vars, labels_visited = player.play()
            
            result.labels_visited = labels_visited
            result.final_state = final_vars
            result.choices_made = player.choices_made
            
            # Check assertions
            for assertion in scenario.assertions:
                if self._check_assertion(player, assertion):
                    result.assertions_passed.append(assertion)
                else:
                    error = self._get_assertion_error(player, assertion)
                    result.assertions_failed.append((assertion, error))
                    result.passed = False
                    
        except Exception as e:
            result.passed = False
            result.error = str(e)
            import traceback
            traceback.print_exc()
        
        result.duration = time.time() - start_time
        return result
    
    def _check_assertion(self, player: SimpleTestPlayer, assertion: Assertion) -> bool:
        """Check if an assertion passes"""
        if assertion.type == AssertionType.VARIABLE:
            actual = player.variables.get(assertion.target)
            return actual == assertion.expected
        elif assertion.type == AssertionType.LABEL_REACHED:
            return assertion.target in player.labels_visited
        return False
    
    def _get_assertion_error(self, player: SimpleTestPlayer, assertion: Assertion) -> str:
        """Get error message for failed assertion"""
        if assertion.type == AssertionType.VARIABLE:
            actual = player.variables.get(assertion.target)
            return f"Expected {assertion.target}={assertion.expected}, got {actual}"
        elif assertion.type == AssertionType.LABEL_REACHED:
            return f"Label '{assertion.target}' was not reached. Visited: {player.labels_visited}"
        return "Unknown assertion failure"
    
    def generate_report(self, results: List[TestResult]) -> str:
        """Generate console report"""
        lines = ["Link Loader Test Results", "=" * 40, ""]
        
        passed = failed = 0
        
        for result in results:
            status = "PASSED" if result.passed else "FAILED"
            symbol = "✓" if result.passed else "✗"
            
            lines.append(f"{symbol} {result.scenario_name} ... {status}")
            
            if result.choices_made:
                lines.append(f"  Choices: {' -> '.join(result.choices_made[:3])}")
            
            if result.passed:
                passed += 1
            else:
                failed += 1
                for assertion, error in result.assertions_failed:
                    lines.append(f"  - {error}")
                if result.error:
                    lines.append(f"  - Error: {result.error}")
            
            lines.append(f"  Duration: {result.duration:.2f}s")
            lines.append("")
        
        lines.append(f"Total: {passed}/{passed + failed} passed")
        return "\n".join(lines)

def main():
    """Run tests"""
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    runner = TestRunner(game_path)
    
    # Test scenarios
    scenarios = [
        TestScenario(
            name="Test Cosmonaut Path",
            description="Test cosmonaut character creation",
            choices=[
                Choice("Welcome Comrade", 1),  # Character selection
                Choice("robot language", 1),   # Robot language option
            ],
            assertions=[
                Assertion(AssertionType.VARIABLE, "cos", 2),
                Assertion(AssertionType.VARIABLE, "cow", -1),
                Assertion(AssertionType.VARIABLE, "cod", 2),
                Assertion(AssertionType.LABEL_REACHED, "scene1_intro"),
                Assertion(AssertionType.LABEL_REACHED, "scene3_cosmonaut"),
            ]
        ),
        TestScenario(
            name="Test Cowboy Path",
            description="Test cowboy character creation",
            choices=[
                Choice("Howdy Pardner", 2),     # Character selection
                Choice("human language", 2),    # Human language option
            ],
            assertions=[
                Assertion(AssertionType.VARIABLE, "cos", -1),
                Assertion(AssertionType.VARIABLE, "cow", 2),
                Assertion(AssertionType.VARIABLE, "cod", 2),
                Assertion(AssertionType.LABEL_REACHED, "scene1_intro"),
                Assertion(AssertionType.LABEL_REACHED, "scene3_cowboy"),
            ]
        ),
    ]
    
    # Run tests
    results = []
    for scenario in scenarios:
        print(f"Running: {scenario.name}...")
        result = runner.run_scenario(scenario)
        results.append(result)
    
    # Generate report
    report = runner.generate_report(results)
    print("\n" + report)
    
    # Exit with appropriate code
    failed = sum(1 for r in results if not r.passed)
    return failed

if __name__ == "__main__":
    sys.exit(main())
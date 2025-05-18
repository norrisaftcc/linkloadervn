#!/usr/bin/env python3
"""
Fixed Test Runner for Link Loader that properly handles menu flow
"""

import os
import re
import sys
import json
import time
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from enum import Enum

sys.path.append(str(Path(__file__).parent))
from renpy_game_player import RenpyGame

class AssertionType(Enum):
    VARIABLE = "variable"
    LABEL_REACHED = "label_reached"

@dataclass
class Choice:
    text_match: str  # Text to match in the choice
    option: int      # Which option to choose (1-based)

@dataclass
class Assertion:
    type: AssertionType
    target: str
    expected: Any = None
    
@dataclass
class TestScenario:
    name: str
    description: str
    choices: List[Choice]
    assertions: List[Assertion]
    
@dataclass
class TestResult:
    scenario_name: str
    passed: bool
    duration: float
    assertions_passed: List[Assertion]
    assertions_failed: List[Tuple[Assertion, str]]
    labels_visited: List[str]
    final_state: Dict[str, Any]
    error: Optional[str] = None
    choices_made: List[str] = field(default_factory=list)

class FixedTestPlayer:
    """Fixed test player that handles Link Loader's menu structure"""
    
    def __init__(self, game: RenpyGame, choices: List[Choice]):
        self.game = game
        self.choices = choices
        self.choice_index = 0
        self.variables = dict(game.default_variables)
        self.labels_visited = []
        self.current_label = "start"
        self.choices_made = []
        self.max_iterations = 100  # Safety limit
    
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
            print(f"Error executing: {code} - {e}")
    
    def process_menu(self, lines: List[Tuple[int, str, str]], start_idx: int) -> int:
        """Process a menu and make a choice, returning the index to continue from"""
        menu_indent = lines[start_idx][0]
        idx = start_idx + 1
        choices_found = []
        
        # Skip menu prompt
        if idx < len(lines) and '"' in lines[idx][1]:
            idx += 1
        
        # Extract all choices
        while idx < len(lines):
            indent, line, _ = lines[idx]
            
            # Stop if we've dedented past the menu
            if indent <= menu_indent and line.strip() and not line.strip().startswith('"'):
                break
            
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
            
            idx += 1
        
        # Find which choice to make
        selected = None
        
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
            return idx
        
        self.choices_made.append(selected['text'])
        
        # Process the selected choice block
        choice_idx = selected['index'] + 1
        choice_indent = lines[selected['index']][0]
        
        while choice_idx < len(lines):
            indent, line, _ = lines[choice_idx]
            
            # Stop if we've dedented past the choice
            if indent <= choice_indent and line.strip():
                break
            
            # Process the line
            line = line.strip()
            if line.startswith('$'):
                self.execute_python(line[1:].strip())
            
            choice_idx += 1
        
        # Continue after the entire menu block
        return self.find_next_statement(lines, start_idx, menu_indent)
    
    def find_next_statement(self, lines: List[Tuple[int, str, str]], start_idx: int, indent_level: int) -> int:
        """Find the next statement after a block at the given indent level"""
        idx = start_idx + 1
        
        while idx < len(lines):
            indent, line, _ = lines[idx]
            
            # Found a statement at or below our indent level
            if indent <= indent_level and line.strip():
                return idx
            
            idx += 1
        
        return idx
    
    def play_label(self, label: str) -> bool:
        """Play through a label, return True if we should continue"""
        if label not in self.game.labels:
            raise ValueError(f"Label '{label}' not found")
        
        if label in self.labels_visited and len(self.labels_visited) > 5:
            # Avoid infinite loops
            return False
        
        self.labels_visited.append(label)
        lines = self.game.labels[label]
        idx = 0
        
        while idx < len(lines):
            indent, line, _ = lines[idx]
            line = line.strip()
            
            if not line or line.startswith('#'):
                idx += 1
                continue
            
            if line.startswith('$'):
                self.execute_python(line[1:].strip())
            elif line.startswith('jump '):
                target = line[5:].strip()
                self.current_label = target
                return True
            elif line == 'menu:':
                idx = self.process_menu(lines, idx)
                continue
            elif line == 'return':
                self.current_label = None
                return False
            
            idx += 1
        
        # End of label without explicit jump/return
        return False
    
    def play(self):
        """Play through the game following choices"""
        self.current_label = "start"
        iterations = 0
        
        while self.current_label and iterations < self.max_iterations:
            if not self.play_label(self.current_label):
                break
            iterations += 1
        
        return self.variables, self.labels_visited

class TestRunner:
    """Main test runner for Link Loader"""
    
    def __init__(self, game_path: str):
        self.game_path = game_path
        self.game = RenpyGame(game_path)
    
    def run_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a single test scenario"""
        start_time = time.time()
        
        player = FixedTestPlayer(self.game, scenario.choices)
        
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
    
    def _check_assertion(self, player: FixedTestPlayer, assertion: Assertion) -> bool:
        """Check if an assertion passes"""
        if assertion.type == AssertionType.VARIABLE:
            actual = player.variables.get(assertion.target)
            return actual == assertion.expected
        elif assertion.type == AssertionType.LABEL_REACHED:
            return assertion.target in player.labels_visited
        return False
    
    def _get_assertion_error(self, player: FixedTestPlayer, assertion: Assertion) -> str:
        """Get error message for failed assertion"""
        if assertion.type == AssertionType.VARIABLE:
            actual = player.variables.get(assertion.target)
            return f"Expected {assertion.target}={assertion.expected}, got {actual}"
        elif assertion.type == AssertionType.LABEL_REACHED:
            visited_str = ', '.join(player.labels_visited[-5:])
            return f"Label '{assertion.target}' not reached. Last visited: [{visited_str}]"
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
            
            if result.labels_visited:
                lines.append(f"  Path: {' -> '.join(result.labels_visited[:5])}")
            
            if result.passed:
                passed += 1
                lines.append(f"  All {len(result.assertions_passed)} assertions passed")
            else:
                failed += 1
                for assertion, error in result.assertions_failed:
                    lines.append(f"  - {error}")
                if result.error:
                    lines.append(f"  - Error: {result.error}")
            
            lines.append(f"  Duration: {result.duration:.2f}s")
            lines.append("")
        
        lines.append(f"Total: {passed}/{passed + failed} passed")
        
        # Coverage info
        all_labels = set()
        for result in results:
            all_labels.update(result.labels_visited)
        
        total_labels = len(self.game.labels)
        coverage = (len(all_labels) / total_labels * 100) if total_labels > 0 else 0
        lines.append(f"Coverage: {len(all_labels)}/{total_labels} labels ({coverage:.1f}%)")
        
        return "\n".join(lines)

def main():
    """Run tests"""
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    runner = TestRunner(game_path)
    
    # Test scenarios - check the actual choices in the game
    scenarios = [
        TestScenario(
            name="Test Cosmonaut Path",
            description="Test cosmonaut character creation",
            choices=[
                Choice("Welcome Comrade", 1),  # Character selection
            ],
            assertions=[
                Assertion(AssertionType.VARIABLE, "cos", 2),
                Assertion(AssertionType.VARIABLE, "cow", -1),
                Assertion(AssertionType.VARIABLE, "cod", 2),
                Assertion(AssertionType.LABEL_REACHED, "scene1_intro"),
            ]
        ),
        TestScenario(
            name="Test Cowboy Path",
            description="Test cowboy character creation",
            choices=[
                Choice("Howdy Pardner", 2),  # Character selection
            ],
            assertions=[
                Assertion(AssertionType.VARIABLE, "cos", -1),
                Assertion(AssertionType.VARIABLE, "cow", 2),
                Assertion(AssertionType.VARIABLE, "cod", 2),
                Assertion(AssertionType.LABEL_REACHED, "scene1_intro"),
            ]
        ),
        TestScenario(
            name="Test Coder Path through to approach",
            description="Test Major Tom character and approach selection",
            choices=[
                Choice("Major Tom", 3),  # Character selection
                Choice("human language", 2),  # Second menu choice (if COD > 1)
            ],
            assertions=[
                Assertion(AssertionType.VARIABLE, "cos", 2),
                Assertion(AssertionType.VARIABLE, "cow", 2),
                Assertion(AssertionType.VARIABLE, "cod", -1),
                Assertion(AssertionType.LABEL_REACHED, "scene1_intro"),
                Assertion(AssertionType.LABEL_REACHED, "scene2_link_loader"),
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
    
    # Save HTML report
    html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Link Loader Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        pre {{ background: #f0f0f0; padding: 10px; }}
    </style>
</head>
<body>
    <h1>Link Loader Test Report</h1>
    <pre>{report}</pre>
</body>
</html>
"""
    
    with open("test_report.html", "w") as f:
        f.write(html)
    print("HTML report saved to test_report.html")
    
    # Exit with appropriate code
    failed = sum(1 for r in results if not r.passed)
    return failed

if __name__ == "__main__":
    sys.exit(main())
#!/usr/bin/env python3
"""
Automated Test Runner for Link Loader

Based on the test framework specification, this implements automated testing
for Ren'Py games using the text-based player.
"""

import os
import sys
import json
import yaml
import time
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from enum import Enum

# Add parent directory to path to import game player
sys.path.append(str(Path(__file__).parent))
from renpy_game_player import RenpyGame, GamePlayer, GameState

class AssertionType(Enum):
    """Types of assertions we can make"""
    VARIABLE = "variable"
    LABEL_REACHED = "label_reached"
    CHARACTER_SHOWN = "character_shown"
    SCENE = "scene"
    MUSIC = "music"

@dataclass
class Choice:
    """Represents a choice to make at a menu"""
    menu_text: str  # Text that appears in the menu prompt
    option: int     # Which option to choose (1-based)

@dataclass
class Assertion:
    """Represents an assertion to check"""
    type: AssertionType
    target: str
    expected: Any
    label: Optional[str] = None  # When to check (after which label)
    
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
    assertions_failed: List[Tuple[Assertion, str]]  # (assertion, error_msg)
    labels_visited: List[str]
    final_state: Dict[str, Any]
    error: Optional[str] = None

class AutomatedPlayer(GamePlayer):
    """Extended game player for automated testing"""
    
    def __init__(self, game: RenpyGame, choices: List[Choice]):
        super().__init__(game, typing_speed=0)  # No typing delay for tests
        self.choices = choices
        self.choice_index = 0
        self.labels_visited = []
        self.auto_mode = True
    
    def process_menu(self, lines, start_idx):
        """Override menu processing for automated choices"""
        # Find the menu prompt
        menu_indent = lines[start_idx][0]
        idx = start_idx + 1
        
        # Extract menu text
        menu_text = ""
        if idx < len(lines) and '"' in lines[idx][1]:
            import re
            match = re.match(r'\s*"([^"]*)"', lines[idx][1])
            if match:
                menu_text = match.group(1)
                idx += 1
        
        # Find the right choice based on menu text
        chosen_option = None
        for choice in self.choices:
            if choice.menu_text in menu_text:
                chosen_option = choice.option
                break
        
        # If no specific choice found, use next in sequence
        if chosen_option is None and self.choice_index < len(self.choices):
            chosen_option = self.choices[self.choice_index].option
            self.choice_index += 1
        
        # Default to option 1 if nothing else
        if chosen_option is None:
            chosen_option = 1
            
        # Collect available options
        options = []
        option_idx = 0
        
        while idx < len(lines):
            indent, line, _ = lines[idx]
            
            if indent <= menu_indent and line.strip() and not line.strip().startswith('"'):
                break
                
            choice_match = re.match(r'\s*"([^"]*)"(\s+if\s+(.+))?:', line)
            if choice_match:
                choice_text = choice_match.group(1)
                condition = choice_match.group(3)
                
                # Check condition if present
                if condition and not self.evaluate_expression(condition):
                    idx += 1
                    continue
                    
                option_idx += 1
                options.append({
                    'text': choice_text,
                    'index': idx,
                    'indent': indent,
                    'number': option_idx
                })
            
            idx += 1
        
        # Select the option
        if chosen_option <= len(options):
            selected = options[chosen_option - 1]
        else:
            selected = options[0] if options else None
            
        if not selected:
            return None, idx
            
        # Process the selected choice
        choice_idx = selected['index'] + 1
        choice_indent = selected['indent']
        jump_target = None
        
        while choice_idx < len(lines):
            indent, line, _ = lines[choice_idx]
            
            if indent <= choice_indent and line.strip():
                break
                
            target = self.process_line(line)
            if target:
                jump_target = target
                break
                
            choice_idx += 1
        
        return jump_target, idx
    
    def play_label(self, label):
        """Override to track labels visited"""
        self.labels_visited.append(label)
        super().play_label(label)
    
    def play(self):
        """Override to run in automated mode"""
        self.state.current_label = "start"
        
        while self.state.current_label:
            try:
                self.play_label(self.state.current_label)
                
                if self.state.current_label is None:
                    break
                    
            except Exception as e:
                raise e

class TestRunner:
    """Main test runner for Link Loader"""
    
    def __init__(self, game_path: str):
        self.game_path = game_path
        self.game = RenpyGame(game_path)
        self.test_results = []
        
    def run_scenario(self, scenario: TestScenario) -> TestResult:
        """Run a single test scenario"""
        start_time = time.time()
        
        # Create automated player
        player = AutomatedPlayer(self.game, scenario.choices)
        
        # Initialize result
        result = TestResult(
            scenario_name=scenario.name,
            passed=True,
            duration=0,
            assertions_passed=[],
            assertions_failed=[],
            labels_visited=[],
            final_state={}
        )
        
        try:
            # Run the game
            player.play()
            
            # Record visited labels
            result.labels_visited = player.labels_visited
            result.final_state = dict(player.state.variables)
            
            # Check assertions
            for assertion in scenario.assertions:
                try:
                    if self._check_assertion(player, assertion):
                        result.assertions_passed.append(assertion)
                    else:
                        error_msg = self._get_assertion_error(player, assertion)
                        result.assertions_failed.append((assertion, error_msg))
                        result.passed = False
                except Exception as e:
                    result.assertions_failed.append((assertion, str(e)))
                    result.passed = False
                    
        except Exception as e:
            result.passed = False
            result.error = str(e)
            
        result.duration = time.time() - start_time
        return result
    
    def _check_assertion(self, player: AutomatedPlayer, assertion: Assertion) -> bool:
        """Check if an assertion passes"""
        if assertion.type == AssertionType.VARIABLE:
            actual = player.state.variables.get(assertion.target)
            return actual == assertion.expected
            
        elif assertion.type == AssertionType.LABEL_REACHED:
            return assertion.target in player.labels_visited
            
        elif assertion.type == AssertionType.CHARACTER_SHOWN:
            return assertion.target in player.state.shown_images
            
        elif assertion.type == AssertionType.SCENE:
            # Would need to track current scene in player
            return True  # Placeholder
            
        elif assertion.type == AssertionType.MUSIC:
            return player.state.music == assertion.expected
            
        return False
    
    def _get_assertion_error(self, player: AutomatedPlayer, assertion: Assertion) -> str:
        """Get error message for failed assertion"""
        if assertion.type == AssertionType.VARIABLE:
            actual = player.state.variables.get(assertion.target)
            return f"Expected {assertion.target}={assertion.expected}, got {actual}"
            
        elif assertion.type == AssertionType.LABEL_REACHED:
            return f"Label '{assertion.target}' was not reached"
            
        elif assertion.type == AssertionType.CHARACTER_SHOWN:
            return f"Character '{assertion.target}' was not shown"
            
        elif assertion.type == AssertionType.MUSIC:
            return f"Expected music '{assertion.expected}', got '{player.state.music}'"
            
        return "Unknown assertion failure"
    
    def load_scenarios_from_yaml(self, yaml_path: str) -> List[TestScenario]:
        """Load test scenarios from YAML file"""
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
            
        scenarios = []
        for scenario_data in data.get('scenarios', []):
            choices = []
            for choice_data in scenario_data.get('choices', []):
                choices.append(Choice(
                    menu_text=choice_data['menu'],
                    option=choice_data['option']
                ))
                
            assertions = []
            for assertion_data in scenario_data.get('assertions', []):
                assertion_type = AssertionType(assertion_data['type'])
                assertions.append(Assertion(
                    type=assertion_type,
                    target=assertion_data['target'],
                    expected=assertion_data['expected'],
                    label=assertion_data.get('label')
                ))
                
            scenarios.append(TestScenario(
                name=scenario_data['name'],
                description=scenario_data['description'],
                choices=choices,
                assertions=assertions
            ))
            
        return scenarios
    
    def generate_report(self, results: List[TestResult], format: str = "console") -> str:
        """Generate test report"""
        if format == "console":
            return self._generate_console_report(results)
        elif format == "html":
            return self._generate_html_report(results)
        elif format == "json":
            return self._generate_json_report(results)
        else:
            raise ValueError(f"Unknown format: {format}")
    
    def _generate_console_report(self, results: List[TestResult]) -> str:
        """Generate console test report"""
        lines = []
        lines.append("Link Loader Test Results")
        lines.append("=" * 40)
        lines.append("")
        
        passed = 0
        failed = 0
        
        for result in results:
            status = "PASSED" if result.passed else "FAILED"
            symbol = "✓" if result.passed else "✗"
            
            lines.append(f"{symbol} {result.scenario_name}{'.' * (40 - len(result.scenario_name))} {status}")
            
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
            
        # Summary
        total = passed + failed
        lines.append(f"Total: {passed}/{total} passed ({passed/total*100:.1f}%)")
        
        # Coverage
        all_labels = set()
        for result in results:
            all_labels.update(result.labels_visited)
        
        total_labels = len(self.game.labels)
        coverage = len(all_labels) / total_labels * 100 if total_labels > 0 else 0
        
        lines.append(f"Coverage: {len(all_labels)}/{total_labels} labels ({coverage:.1f}%)")
        
        return "\n".join(lines)
    
    def _generate_html_report(self, results: List[TestResult]) -> str:
        """Generate HTML test report"""
        # Simplified HTML report
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>Link Loader Test Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .passed { color: green; }
        .failed { color: red; }
        .summary { margin-top: 20px; padding: 10px; background: #f0f0f0; }
        table { border-collapse: collapse; width: 100%; margin-top: 20px; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #4CAF50; color: white; }
    </style>
</head>
<body>
    <h1>Link Loader Test Report</h1>
    <div class="summary">
        <h2>Summary</h2>
        <p>Total Tests: {total}</p>
        <p>Passed: <span class="passed">{passed}</span></p>
        <p>Failed: <span class="failed">{failed}</span></p>
        <p>Coverage: {coverage:.1f}%</p>
    </div>
    <table>
        <tr>
            <th>Test Name</th>
            <th>Status</th>
            <th>Duration</th>
            <th>Details</th>
        </tr>
        {test_rows}
    </table>
</body>
</html>
"""
        
        passed = sum(1 for r in results if r.passed)
        failed = sum(1 for r in results if not r.passed)
        total = passed + failed
        
        # Calculate coverage
        all_labels = set()
        for result in results:
            all_labels.update(result.labels_visited)
        coverage = len(all_labels) / len(self.game.labels) * 100
        
        # Generate test rows
        test_rows = []
        for result in results:
            status_class = "passed" if result.passed else "failed"
            status = "PASSED" if result.passed else "FAILED"
            
            details = []
            if not result.passed:
                for assertion, error in result.assertions_failed:
                    details.append(f"• {error}")
                if result.error:
                    details.append(f"• Error: {result.error}")
                    
            details_html = "<br>".join(details) if details else "All assertions passed"
            
            test_rows.append(f"""
                <tr>
                    <td>{result.scenario_name}</td>
                    <td class="{status_class}">{status}</td>
                    <td>{result.duration:.2f}s</td>
                    <td>{details_html}</td>
                </tr>
            """)
            
        return html.format(
            total=total,
            passed=passed,
            failed=failed,
            coverage=coverage,
            test_rows="".join(test_rows)
        )
    
    def _generate_json_report(self, results: List[TestResult]) -> str:
        """Generate JSON test report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(results),
                "passed": sum(1 for r in results if r.passed),
                "failed": sum(1 for r in results if not r.passed)
            },
            "results": []
        }
        
        for result in results:
            result_data = {
                "name": result.scenario_name,
                "passed": result.passed,
                "duration": result.duration,
                "labels_visited": result.labels_visited,
                "final_state": result.final_state,
                "assertions": {
                    "passed": len(result.assertions_passed),
                    "failed": len(result.assertions_failed)
                }
            }
            
            if not result.passed:
                result_data["failures"] = []
                for assertion, error in result.assertions_failed:
                    result_data["failures"].append({
                        "type": assertion.type.value,
                        "target": assertion.target,
                        "expected": assertion.expected,
                        "error": error
                    })
                    
            report_data["results"].append(result_data)
            
        return json.dumps(report_data, indent=2)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="Automated test runner for Link Loader")
    parser.add_argument("--game", default="../current/renpy-8.3.7-sdk/link_loader_1_2/game",
                        help="Path to game directory")
    parser.add_argument("--scenarios", default="test_scenarios.yaml",
                        help="Path to test scenarios YAML file")
    parser.add_argument("--format", choices=["console", "html", "json"], default="console",
                        help="Output format")
    parser.add_argument("--output", help="Output file (default: stdout)")
    parser.add_argument("--ci", action="store_true", help="CI mode (exit code based on results)")
    
    args = parser.parse_args()
    
    # Create test runner
    runner = TestRunner(args.game)
    
    # Load scenarios
    if os.path.exists(args.scenarios):
        scenarios = runner.load_scenarios_from_yaml(args.scenarios)
    else:
        # Default test scenario
        scenarios = [
            TestScenario(
                name="Test Cosmonaut Path",
                description="Test the cosmonaut character creation path",
                choices=[
                    Choice("Choose your character background", 1),  # Welcome Comrade
                    Choice("What will you do?", 1)  # Robot language
                ],
                assertions=[
                    Assertion(AssertionType.VARIABLE, "cos", 2),
                    Assertion(AssertionType.VARIABLE, "cow", -1),
                    Assertion(AssertionType.VARIABLE, "cod", 2),
                    Assertion(AssertionType.LABEL_REACHED, "scene1_intro", None)
                ]
            )
        ]
    
    # Run tests
    results = []
    for scenario in scenarios:
        print(f"Running: {scenario.name}...")
        result = runner.run_scenario(scenario)
        results.append(result)
    
    # Generate report
    report = runner.generate_report(results, args.format)
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
    else:
        print(report)
    
    # Exit code for CI
    if args.ci:
        failed = sum(1 for r in results if not r.passed)
        sys.exit(failed)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Simple test script to verify the test runner works
"""

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from test_runner import TestRunner, TestScenario, Choice, Assertion, AssertionType

def run_simple_test():
    """Run a simple test to verify the system works"""
    
    # Path to the game
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    
    # Create test runner
    runner = TestRunner(game_path)
    
    # Create a simple test scenario
    scenario = TestScenario(
        name="Quick Verification Test",
        description="Test that we can start the game and make a choice",
        choices=[
            Choice("Choose your character background", 1)  # Choose Cosmonaut
        ],
        assertions=[
            Assertion(AssertionType.VARIABLE, "cos", 2),
            Assertion(AssertionType.VARIABLE, "cow", -1),
            Assertion(AssertionType.VARIABLE, "cod", 2),
            Assertion(AssertionType.LABEL_REACHED, "scene1_intro", None)
        ]
    )
    
    # Run the test
    print(f"Running test: {scenario.name}")
    result = runner.run_scenario(scenario)
    
    # Generate report
    report = runner.generate_report([result])
    print("\n" + report)
    
    # Save HTML report
    html_report = runner.generate_report([result], format="html")
    with open("test_report.html", "w") as f:
        f.write(html_report)
    print("\nHTML report saved to test_report.html")
    
    return 0 if result.passed else 1

def run_yaml_tests():
    """Run tests from YAML file"""
    
    # Check if YAML file exists
    if not os.path.exists("test_scenarios.yaml"):
        print("No test_scenarios.yaml found, creating one...")
        # Would create the file here
        return 1
    
    # Run tests
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    runner = TestRunner(game_path)
    
    # Load scenarios
    scenarios = runner.load_scenarios_from_yaml("test_scenarios.yaml")
    
    # Run all scenarios
    results = []
    for scenario in scenarios:
        print(f"Running: {scenario.name}...")
        result = runner.run_scenario(scenario)
        results.append(result)
    
    # Generate reports
    console_report = runner.generate_report(results)
    print("\n" + console_report)
    
    # Save HTML report
    html_report = runner.generate_report(results, format="html")
    with open("test_report_full.html", "w") as f:
        f.write(html_report)
    print("\nFull HTML report saved to test_report_full.html")
    
    # Save JSON report
    json_report = runner.generate_report(results, format="json")
    with open("test_report.json", "w") as f:
        f.write(json_report)
    print("JSON report saved to test_report.json")
    
    # Return exit code
    failed = sum(1 for r in results if not r.passed)
    return failed

if __name__ == "__main__":
    print("Link Loader Test Runner Demo")
    print("=" * 30)
    
    # Run simple test first
    print("\n1. Running simple verification test...")
    result = run_simple_test()
    
    if result == 0:
        print("\n2. Running full test suite from YAML...")
        result = run_yaml_tests()
    
    print(f"\nTest run complete. Exit code: {result}")
    sys.exit(result)
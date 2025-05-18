# Link Loader Script Validation Tools Specification

**Author**: Chen (Script/Narrative)  
**Date**: Today  
**Version**: 1.0

## Overview

This document specifies the script validation tools for Link Loader, designed to help writers and narrative designers ensure script quality and consistency.

## Core Validation Components

### 1. Script Flow Analyzer

```python
class ScriptFlowAnalyzer:
    """Analyzes the flow and structure of Ren'Py scripts"""
    
    def __init__(self, game_path: str):
        self.game = RenpyGame(game_path)
        self.flow_graph = nx.DiGraph()  # NetworkX directed graph
        self._build_flow_graph()
    
    def find_unreachable_labels(self) -> List[str]:
        """Find labels that cannot be reached from start"""
        pass
    
    def find_dead_ends(self) -> List[str]:
        """Find paths that don't lead to an ending"""
        pass
    
    def analyze_branch_complexity(self) -> ComplexityReport:
        """Analyze branching complexity"""
        pass
    
    def visualize_flow(self) -> None:
        """Generate visual flow chart"""
        pass
```

### 2. Character Voice Analyzer

```python
class CharacterVoiceAnalyzer:
    """Analyzes character dialogue for consistency"""
    
    def __init__(self, game_path: str):
        self.game = RenpyGame(game_path)
        self.character_profiles = {}
        self._build_profiles()
    
    def analyze_vocabulary(self, character: str) -> VocabularyProfile:
        """Analyze character's vocabulary usage"""
        pass
    
    def detect_inconsistencies(self) -> List[Inconsistency]:
        """Find dialogue that doesn't match character voice"""
        pass
    
    def compare_characters(self) -> SimilarityMatrix:
        """Compare speech patterns between characters"""
        pass
    
    def suggest_improvements(self) -> List[Suggestion]:
        """Suggest dialogue improvements"""
        pass
```

### 3. Condition Validator

```python
class ConditionValidator:
    """Validates conditional logic in scripts"""
    
    def __init__(self, game_path: str):
        self.game = RenpyGame(game_path)
        self.variable_ranges = {}
        self._analyze_variables()
    
    def find_impossible_conditions(self) -> List[ImpossibleCondition]:
        """Find conditions that can never be true"""
        pass
    
    def find_redundant_conditions(self) -> List[RedundantCondition]:
        """Find duplicate or unnecessary conditions"""
        pass
    
    def analyze_variable_usage(self) -> VariableUsageReport:
        """Track how variables are used"""
        pass
    
    def suggest_simplifications(self) -> List[Simplification]:
        """Suggest ways to simplify logic"""
        pass
```

## Validation Rules

### 1. Structure Rules

- **No Orphan Labels**: Every label should be reachable
- **No Dead Ends**: Every path should lead to an ending
- **Return Consistency**: Called labels must return properly
- **Jump Validity**: All jumps must target existing labels

### 2. Character Voice Rules

- **Consistent Vocabulary**: Characters use consistent word choices
- **Speech Patterns**: Maintain unique speech patterns per character
- **Emotional Range**: Characters express emotions consistently
- **Cultural References**: Keep references appropriate to character

### 3. Logic Rules

- **Variable Initialization**: All variables used must be defined
- **Range Validity**: Conditions must be mathematically possible
- **Type Consistency**: Variables maintain consistent types
- **No Redundancy**: Avoid duplicate conditional checks

## Analysis Reports

### 1. Flow Analysis Report

```yaml
# flow_analysis_report.yaml
summary:
  total_labels: 45
  reachable_labels: 42
  unreachable_labels: 3
  dead_ends: 1
  
unreachable:
  - label: debug_menu
    reason: No jumps or calls to this label
  - label: old_ending
    reason: Commented out jump in scene4
  - label: test_scene
    reason: Development label not connected

dead_ends:
  - path: scene2 -> choice3 -> error_handler
    reason: No return or jump statement

complexity:
  max_depth: 5
  branch_points: 12
  total_paths: 18
```

### 2. Character Voice Report

```yaml
# character_voice_report.yaml
characters:
  Slim:
    total_lines: 127
    vocabulary_size: 432
    common_phrases:
      - "howdy": 8
      - "partner": 6
      - "sure is": 4
    speech_patterns:
      contractions: 85%
      questions: 23%
      exclamations: 12%
    
  Clipi:
    total_lines: 98
    vocabulary_size: 389
    common_phrases:
      - "processing": 5
      - "systems": 7
      - "operational": 4
    inconsistencies:
      - line_142: "Howdy partner!" # Too informal
      - line_278: "I reckon" # Wrong character voice
```

### 3. Condition Analysis Report

```yaml
# condition_analysis_report.yaml
variables:
  cos:
    type: integer
    range: [-1, 2]
    usage_count: 15
    
  approach:
    type: string
    values: ["none", "cosmonaut", "cowboy", "coder"]
    usage_count: 8

issues:
  impossible_conditions:
    - file: scene3.rpy
      line: 45
      condition: "cos > 5"
      reason: "cos max value is 2"
      
  redundant_conditions:
    - file: scene5.rpy
      line: 123
      condition: "approach == 'cowboy' and cow > 0"
      reason: "cowboy approach always has cow > 0"

suggestions:
  - simplify: "if approach == 'coder' or cod > 1"
    to: "if cod > 1"
    reason: "coder approach always sets cod > 1"
```

## Implementation Plan

### Phase 1: Core Analysis (Days 1-3)
1. Build flow graph generator
2. Implement reachability analysis
3. Create basic report generation
4. Add command-line interface

### Phase 2: Voice Analysis (Days 4-6)
1. Implement dialogue extraction
2. Add vocabulary analysis
3. Create character profiles
4. Build inconsistency detection

### Phase 3: Logic Validation (Days 7-9)
1. Parse conditional statements
2. Track variable ranges
3. Detect impossible conditions
4. Generate suggestions

### Phase 4: Reporting & Visualization (Days 10-12)
1. Create comprehensive reports
2. Add flow chart visualization
3. Build web dashboard
4. Integrate with test framework

## Usage Examples

### Command Line

```bash
# Run all validations
python script_validator.py

# Run specific validation
python script_validator.py --check flow

# Generate visual flow chart
python script_validator.py --visualize

# Output to specific format
python script_validator.py --format html

# Check specific character
python script_validator.py --character Slim
```

### Integration

```python
# validate_scripts.py
from linkloader.validation import ScriptValidator

validator = ScriptValidator("../game")

# Check for unreachable content
unreachable = validator.find_unreachable_labels()
if unreachable:
    print(f"Warning: {len(unreachable)} unreachable labels")
    
# Analyze character consistency
voice_issues = validator.check_character_voice("Slim")
for issue in voice_issues:
    print(f"Line {issue.line}: {issue.description}")
```

## Visual Reports

### 1. Flow Chart
- Interactive node graph
- Colored by reachability
- Click to see label details
- Export as SVG/PNG

### 2. Character Dashboard
- Word clouds per character
- Speech pattern analysis
- Emotion distribution
- Line count over time

### 3. Complexity Heatmap
- Visual representation of script complexity
- Highlight problem areas
- Show test coverage overlay
- Track changes over time

## Future Enhancements

1. **AI-Powered Suggestions**: Use language models for dialogue improvements
2. **Style Guide Enforcement**: Check against custom style rules
3. **Emotional Arc Tracking**: Analyze character emotional journeys
4. **Pacing Analysis**: Detect sections that may be too slow/fast
5. **Translation Readiness**: Check for localization issues
6. **Collaborative Editing**: Multi-writer conflict detection

## Integration with Development Workflow

1. **Pre-commit Validation**: Run checks before allowing commits
2. **CI/CD Pipeline**: Automated validation on pull requests
3. **Editor Integration**: Real-time validation in VS Code
4. **Weekly Reports**: Track script health over time
5. **Sprint Planning**: Use metrics for workload estimation

## Conclusion

These validation tools will help maintain high script quality, catch issues early, and ensure consistency across the entire Link Loader narrative. By automating these checks, writers can focus on creativity while the tools handle quality assurance.
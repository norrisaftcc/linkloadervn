# Sprint Planning Session - Testing & Validation Tools

**Date**: Today  
**Attendees**: Julie (UI/Art), Chen (Script/Narrative), Bob (Engineering), AI (Facilitator)  
**Sprint Goals**: 
1. Automated Testing Framework
2. Script Validation Tools

---

## Opening Discussion

**AI**: Welcome everyone! Today we're planning our next sprint focused on testing and validation tools for Link Loader. Let's start with introductions and what each of you hopes to achieve.

**Bob (Engineering)**: Hey folks. I'm excited about this sprint. We've got the text-based player working great, and now we need to leverage it for automated testing. I want to build a test suite that can catch bugs before they hit production.

**Chen (Script/Narrative)**: Hi everyone. From my perspective, I need tools that help me validate our scripts are coherent. Things like checking that all dialogue paths are reachable, that character voices stay consistent, and that our branching narratives don't have dead ends.

**Julie (UI/Art)**: Good morning! While this sprint is mostly technical, I'm interested in how these tools can help me track which assets are actually being used in the game. I've created a lot of character expressions and backgrounds, and I want to make sure they're all accessible.

---

## User Stories

**AI**: Let's break down our goals into specific user stories. Bob, want to start with the testing framework?

**Bob**: Sure! Here are my user stories:

### Automated Testing Framework

1. **As a developer**, I want to run automated tests that play through all major game paths, so I can catch breaking changes early.
   - Acceptance: Tests cover all 3 character creation paths
   - Acceptance: Tests verify each approach (cosmonaut/cowboy/coder) works
   - Acceptance: Tests check all 3 ending choices

2. **As a developer**, I want regression tests that verify game variables are set correctly, so I can ensure game mechanics work as designed.
   - Acceptance: Test character stats (COS/COW/COD) are set properly
   - Acceptance: Test that approach and mission variables update correctly
   - Acceptance: Test conditional dialogue appears when expected

3. **As a QA tester**, I want a test report that shows which paths have been tested, so I can identify untested areas.
   - Acceptance: HTML report showing test coverage
   - Acceptance: Visual flow chart of tested paths
   - Acceptance: List of untested dialogue branches

**Chen**: Great! Here are mine for the validation tools:

### Script Validation Tools

4. **As a writer**, I want to validate that all labels in my script are reachable, so players don't hit dead ends.
   - Acceptance: Tool identifies orphaned labels
   - Acceptance: Tool shows jump/call graph
   - Acceptance: Tool warns about missing return statements

5. **As a narrative designer**, I want to check character consistency, so dialogue stays true to each character's voice.
   - Acceptance: Word frequency analysis per character
   - Acceptance: Flagging of out-of-character phrases
   - Acceptance: Statistics on line count per character

6. **As a script editor**, I want to verify all conditional branches are possible to reach, so content isn't wasted.
   - Acceptance: Variable range analysis
   - Acceptance: Impossible condition detection
   - Acceptance: Unused variable warnings

**Julie**: And here's mine:

7. **As an artist**, I want to track which assets are referenced in scripts, so I know what's being used and what's missing.
   - Acceptance: List of all image/audio references
   - Acceptance: Report of missing asset files
   - Acceptance: Usage statistics for each asset

---

## Technical Design Discussion

**Bob**: Alright, let's talk implementation. For the testing framework, I'm thinking we build on top of the `renpy_game_player.py` we just created. We can create a `TestRunner` class that:

```python
class TestRunner:
    def __init__(self, game_path):
        self.game = RenpyGame(game_path)
        self.test_results = []
    
    def run_test_path(self, choices):
        # Automatically play through with specific choices
        pass
    
    def assert_variable(self, var_name, expected_value):
        # Check game state
        pass
    
    def generate_report(self):
        # Create HTML report with coverage
        pass
```

**Chen**: For the validation tools, I need something that parses all the scripts and builds a graph of the narrative flow. Maybe:

```python
class ScriptValidator:
    def __init__(self, game_path):
        self.game = RenpyGame(game_path)
        self.flow_graph = self.build_flow_graph()
    
    def find_unreachable_labels(self):
        # Graph traversal to find orphans
        pass
    
    def analyze_character_voice(self):
        # NLP analysis of dialogue
        pass
    
    def check_conditions(self):
        # Static analysis of conditionals
        pass
```

**Julie**: For asset tracking, we could extend the existing parser to extract all asset references:

```python
class AssetTracker:
    def __init__(self, game_path):
        self.game = RenpyGame(game_path)
        self.assets = self.extract_asset_references()
    
    def find_missing_assets(self):
        # Compare references with actual files
        pass
    
    def generate_usage_report(self):
        # Show which assets are used where
        pass
```

---

## Sprint Backlog

**AI**: Based on our discussion, here's our prioritized backlog for this sprint:

### Week 1
1. **[Bob]** Create base `TestRunner` class with path execution
2. **[Bob]** Implement assertion methods for variables and state
3. **[Chen]** Build script parser for flow graph generation
4. **[Chen]** Implement unreachable label detection

### Week 2
5. **[Bob]** Add test coverage reporting
6. **[Chen]** Add character voice analysis
7. **[Julie]** Implement asset reference extraction
8. **[All]** Integration and documentation

### Stretch Goals
9. Visual flow chart generation
10. GUI for validation tools
11. CI/CD integration

---

## Dependencies and Risks

**Bob**: I'll need the current `renpy_game_player.py` to remain stable. Any major changes to it could break our tests.

**Chen**: I need sample scripts with known issues to test against. Maybe we create some purposely broken scripts?

**Julie**: I need a complete list of asset types the game supports. Do we handle video files? What about fonts?

**AI**: Good points. Let's address these:
- Bob: We'll version lock the player for testing
- Chen: We'll create a `test_scripts/` directory with known issues
- Julie: We'll document all supported asset types

---

## Definition of Done

**AI**: Let's agree on what "done" means for this sprint:

1. All code has unit tests with >80% coverage
2. Documentation includes usage examples
3. Tools are integrated into the planning/ directory
4. Can be run from command line with clear help text
5. Results are exported in both human and machine-readable formats

---

## Next Steps

**Bob**: I'll start on the TestRunner class today. Should have basic path execution working by end of week.

**Chen**: I'll begin with the script parser. Need to understand the full Ren'Py syntax we're using.

**Julie**: I'll create a spreadsheet of all current assets and their expected locations.

**AI**: Great! Let's reconvene for daily standups. I'll create the sprint board and tracking documents.

---

## Meeting Notes

- Sprint duration: 2 weeks
- Daily standups at 10 AM
- Demo to stakeholders at end of sprint
- Consider open-sourcing these tools for other Ren'Py developers
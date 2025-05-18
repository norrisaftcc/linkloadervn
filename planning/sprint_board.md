# Sprint Board - Testing & Validation Tools

**Sprint**: Testing & Validation Framework  
**Duration**: 2 weeks  
**Team**: Bob (Engineering), Chen (Script/Narrative), Julie (UI/Art)

---

## Week 1 (Current)

### To Do
- [ ] Asset reference extraction (Julie)
- [ ] Integration and documentation (All)

### In Progress
- None

### Done
- [x] Sprint planning session
- [x] Technical specifications written
- [x] Development environment setup
- [x] Create base TestRunner class with path execution (Bob)
- [x] Implement assertion methods for variables and state (Bob)
- [x] Add test coverage reporting (Bob)
- [x] Build script parser for flow graph generation (Chen)
- [x] Implement unreachable label detection (Chen)
- [x] Add character voice analysis (Chen)

### Blocked
- None

---

## Week 2 (Upcoming)

### Backlog
- [ ] Add test coverage reporting (Bob)
- [ ] Add character voice analysis (Chen)
- [ ] Quality checks implementation (Julie)
- [ ] Web dashboard for reports (All)

### Stretch Goals
- [ ] Visual flow chart generation
- [ ] GUI for validation tools
- [ ] CI/CD integration
- [ ] Performance benchmarking

---

## Daily Standup Notes

### Day 1
**Bob**: Starting on TestRunner base class. Reviewing existing renpy_game_player.py for integration points.

**Chen**: Beginning script parser implementation. Need to understand full label/jump structure.

**Julie**: Creating asset inventory spreadsheet. Documenting all current assets and their locations.

### Day 2
**Bob**: TestRunner can now execute basic paths. Working on assertion methods.

**Chen**: Flow graph generation working for simple scripts. Need to handle menu branches.

**Julie**: Found 15 unused assets and 3 missing references. Will share report.

### Day 3
**Bob**: Completed test runner with assertions and coverage reporting. 33.3% label coverage achieved.

**Chen**: Finished flow graph analyzer and character voice analysis. All labels reachable, no dead ends found. Detected some voice inconsistencies.

**Julie**: Working on asset reference extraction tool. Need file format specifications from team.

---

## Key Decisions

1. **Test Format**: Using YAML for test definitions (easier for non-programmers)
2. **Graph Library**: Using NetworkX for flow analysis
3. **Report Format**: HTML primary, with JSON/YAML export options
4. **Integration**: Will integrate with existing planning tools directory

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Parser complexity | High | Start with subset of Ren'Py features |
| Performance with large games | Medium | Add caching and incremental updates |
| CI/CD integration issues | Low | Test locally first, gradual rollout |

---

## Dependencies

- `renpy_game_player.py` must remain stable
- Need test scripts with known issues
- Asset naming convention document needed

---

## Sprint Metrics

- **Velocity**: 8 story points/week (estimated)
- **Burndown**: On track
- **Code Coverage**: Target 80%
- **Documentation**: All features must have examples

---

## Next Sprint Planning

Potential topics for next sprint:
1. Performance optimization
2. GUI tools development
3. Advanced analytics
4. Integration with Ren'Py launcher

---

## Resources

- [Test Framework Spec](test_framework_spec.md)
- [Script Validation Spec](script_validation_spec.md)
- [Asset Tracking Spec](asset_tracking_spec.md)
- [Sprint Planning Notes](sprint_planning_session.md)
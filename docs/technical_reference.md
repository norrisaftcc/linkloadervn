# Technical Reference

## Repository Structure

- `/renpy/` - Ren'Py game files and assets
  - `/renpy/current/` - Current version (link_loader_1_2)
  - `/renpy/alphas/` - Earlier alpha versions
- `/src/` - Source code and development tools
  - `/src/tools/` - Converters and tests
  - `/src/tests/` - Test files and runners
  - `/src/scripts/` - Build scripts
  - `/src/constellation/` - Constellation Engine
- `/docs/` - Documentation
- `/media/` - Media assets
- `/examples/` - Example scripts
  - `/examples/renpy/` - Sample Ren'Py scripts
- `/output/` - Generated files
  - `/output/html/` - Playable HTML files
  - `/output/twee/` - Twee format files
  - `/output/json/` - JSON intermediate files
- `/tools/` - External tools
  - `/tools/tweego/` - Tweego compiler

## Game Mechanics

### Character Stats
- Cosmonaut (COS) - Space/high-tech skills
- Cowboy (COW) - Desert/low-tech skills
- Coder (COD) - Robot communication skills

### Character Archetypes
- "Welcome Comrade" (COS +2, COW -1, COD +2)
- "Howdy Pardner" (COS -1, COW +2, COD +2)
- "Major Tom" (COS +2, COW +2, COD -1)

## Ren'Py Development

### Key Concepts
- Character definitions: `define pc = Character(...)`
- Scene/show statements for visuals
- Labels for scenes/paths
- Transforms for effects
- Audio playback
- Python functions (e.g., glitch effect)

### File Compilation
- Edit `.rpy` files
- Engine compiles to `.rpyc` on launch
- Test by running the game

### Asset Management
- Images: `/game/images/`
- Audio: `/game/audio/`
- Reference in scripts with Ren'Py commands

## Testing

```bash
# Test converter
cd src/tools
python -m pytest test_renpy_to_twee.py -v
```

## Resources
- Local docs: `/renpy/current/renpy-8.3.7-sdk/doc/`
- Online: https://www.renpy.org/doc/html/
# CLAUDE.md

LinkLoader - A Ren'Py visual novel (sci-fi/western) about a space cowboy fixing broken link loaders.

## Quick Start
```bash
# Run the game
cd renpy/current/renpy-8.3.7-sdk
./renpy.sh ../link_loader_1_2

# Convert to Twine
python src/tools/renpy_to_twee_v2.py input.rpy output.tw
./tools/tweego/tweego -o output.html input.tw
```

## Key Paths
- Game: `/renpy/current/link_loader_1_2/game/`
- Tools: `/src/tools/`
- Playable HTML: `/output/html/`

## Development
- Edit `.rpy` files directly
- Main script: `script.rpy`
- Glitch effects: `glitch.rpy`
- Assets go in `images/` and `audio/`

For detailed documentation, see `/docs/`
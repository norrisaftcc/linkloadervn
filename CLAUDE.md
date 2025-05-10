# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LinkLoader is a visual novel game built with Ren'Py. It's a sci-fi/western hybrid featuring a space cowboy protagonist (Slim) who fixes broken link loaders. The game has a LISP-inspired theme where robots speak with parentheses, and there's a copilot/assistant character named Clipi who often glitches.

The game uses a combination of:
- Ren'Py scripts for story and game logic
- Custom visual effects like glitch transformations
- Generated character assets (made with Stable Diffusion)
- Audio effects and music

## Repository Structure

The repository is organized into several key directories:

- `/alphas/` - Contains earlier alpha versions of the game
- `/current/` - Contains the current version of the game (link_loader_1_2)
- `/media/` - Contains planning notes, rules, and other media assets

The main game files are in `/current/link_loader_1_2/game/`:
- `script.rpy` - The main story script
- `glitch.rpy` - Custom glitch visual effects used by characters
- Various character image files in the `images/` directory

## Running the Game

To run the current version of the game:

1. Use the Ren'Py launcher in `/current/renpy-8.3.7-sdk/`
2. Open the `/current/link_loader_1_2/` project
3. Click "Launch Project" in the Ren'Py launcher

Alternatively, you can run it from the command line:

```bash
cd /Users/norrisa/Documents/dev/github/linkloadervn/current/renpy-8.3.7-sdk
./renpy.sh ../link_loader_1_2
```

## Game Mechanics

The game has a character with three main stats:
- Cosmonaut (COS) - Space/high-tech skills
- Cowboy (COW) - Desert/low-tech skills
- Coder (COD) - Robot communication/terminal skills

Character creation allows choosing from three archetypes:
- "Welcome Comrade" (COS +2, COW -1, COD +2)
- "Howdy Pardner" (COS -1, COW +2, COD +2)
- "Major Tom" (COS +2, COW +2, COD -1)

The game features visual novel-style dialogue, character sprites, and backgrounds with various visual effects, particularly glitch effects for certain characters.

## Developing in Ren'Py

When making changes to the game:

1. Edit the `.rpy` files in a text editor
2. The Ren'Py engine will compile these to `.rpyc` files when the game is launched
3. Test changes by running the game

Remember that Ren'Py uses Python syntax with additional specific commands for visual novels.

Key Ren'Py concepts used in this project:
- Character definitions (`define pc = Character(...)`)
- Scene and show statements for visual elements
- Labels for different scenes/paths
- Transforms for visual effects
- Audio playback commands
- Python functions for special effects (like the glitch effect)

## Asset Management

The game uses various types of assets:
- Character images (in various poses/expressions)
- Background images
- Audio files for music and sound effects

When adding new assets:
1. Place image files in the `images/` directory
2. Place audio files in the `audio/` directory
3. Reference them in the scripts using the appropriate Ren'Py commands

## Documentation

For more information about Ren'Py development:
- The Ren'Py documentation is available in `/current/renpy-8.3.7-sdk/doc/`
- Official Ren'Py documentation is also available at: https://www.renpy.org/doc/html/
# Link Loader Planning Directory

This directory contains the revised script and planning documents for the Link Loader visual novel.

## Contents

- **script.md**: The main narrative script in Markdown format, containing all dialogue, scenes, and choices in an easy-to-read format. This is the "source of truth" for the story content.

- **script.rpy**: A partially-implemented version of the script in Ren'Py format, focusing on the core structure.

- **playable_script.rpy**: A complete implementation of the script in Ren'Py format, ready to be used in the game engine.

- **improvements.md**: A summary of all improvements made to the original script.

## How to Use These Files

1. **For Story Editing**:
   - Make changes to `script.md` first to focus on narrative structure and dialogue
   - This keeps the story separate from implementation details

2. **For Game Implementation**:
   - Copy `playable_script.rpy` to the game directory and rename it to `script.rpy`
   - Adjust any asset paths or character definitions as needed
   - Test in the Ren'Py engine and refine

3. **For Future Episodes**:
   - Use the same structure as in `script.md` 
   - Follow the three-approach pattern for player choices
   - Maintain continuity with the player's final choice in Episode 1

## Game Structure

The game follows a 5-scene structure:

1. **Character Creation**: Player chooses a background that determines their stats
2. **Introduction**: Setting up the problem and introducing characters
3. **At the Link Loader**: Examining the problem and choosing an approach
4. **The Repair**: Different paths based on player's approach
5. **Confrontation**: Dealing with the antagonists
6. **Resolution**: Wrapping up the current mission and setting up future adventures

## Stats System

The game features three main stats that affect dialogue options and problem-solving approaches:
- **Cosmonaut (COS)**: Space/high-tech skills
- **Cowboy (COW)**: Desert/low-tech skills
- **Coder (COD)**: Robot communication/terminal skills
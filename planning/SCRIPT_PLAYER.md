# Script Player Documentation

This document explains how to use the Ren'Py script players for testing and development outside the Ren'Py engine.

## Overview

We now have three main tools for playing scripts outside Ren'Py:

1. **dialogue_player.py** - Plays JSON dialogue trees (conversation-focused)
2. **renpy_player.py** - Plays individual Ren'Py script files 
3. **renpy_game_player.py** - Plays complete Ren'Py games (full game directory)

## Quick Start

### Playing the Current Game

To play the current version of Link Loader in text mode:

```bash
cd /Users/norrisa/Documents/dev/github/linkloadervn/planning
python renpy_game_player.py ../current/link_loader_1_2/game
```

### Playing a Single Script File

To play just the main script file:

```bash
python renpy_player.py ../current/link_loader_1_2/game/script.rpy
```

### Playing Dialogue Trees

If you have a JSON dialogue tree:

```bash
python dialogue_player.py sample_dialogue.json
```

## Features

### renpy_game_player.py (Recommended)

The most complete player that supports:

- **Full Game Loading**: Loads all .rpy files in a game directory
- **Character Definitions**: Parses and displays character names with colors
- **Variables & Conditions**: Supports default variables and conditional statements
- **Labels & Jumps**: Handles label navigation and jumps
- **Menus & Choices**: Interactive menu selections
- **Show/Hide Commands**: Displays character emotions and positions as text
- **Music & Sound**: Shows when audio plays (no actual playback)
- **Save/Load**: Save and restore game state
- **History**: View dialogue history
- **Debug Info**: Show current variables

### renpy_player.py

A simpler player for individual script files:

- Basic character and variable support
- Simple label navigation
- Menu choices
- Python expression evaluation
- Typing animation for dialogue

### dialogue_player.py

For JSON-based dialogue trees:

- Node-based conversation flow
- Variable tracking
- Conditional choices
- Effects and scripts
- Character color formatting

## Usage Options

### Command Line Arguments

For renpy_game_player.py:

```bash
python renpy_game_player.py <game_directory> [options]

Options:
  --speed SPEED    Typing speed in seconds per character (default: 0.02)
  --no-typing      Disable typing animation
  --debug          Enable debug mode for error details
```

### In-Game Commands

While playing, you can:

- Press Enter to continue
- Press 'h' for help menu
- Access save/load functions
- View dialogue history
- Check current variables
- Quit safely

## Examples

### Play Link Loader Current Version

```bash
python renpy_game_player.py ../current/link_loader_1_2/game --speed 0.01
```

### Play Without Typing Effect

```bash
python renpy_game_player.py ../current/link_loader_1_2/game --no-typing
```

### Debug Mode

```bash
python renpy_game_player.py ../current/link_loader_1_2/game --debug
```

## Converting Between Formats

Use convert_script.py to convert between formats:

### Ren'Py to JSON

```bash
python convert_script.py --input script.rpy --output script.json --format renpy2json
```

### JSON to Ren'Py

```bash
python convert_script.py --input script.json --output script.rpy --format json2renpy
```

### JSON to Markdown

```bash
python convert_script.py --input script.json --output script.md --format json2md
```

## Limitations

The text-based players have some limitations compared to the full Ren'Py engine:

- No visual display of images or animations
- No actual audio playback
- Simplified transition effects
- Basic Python evaluation only
- Some Ren'Py-specific features may not work

## Development Workflow

1. **Write Scripts**: Create or modify .rpy files in your game directory
2. **Test Quickly**: Use renpy_game_player.py to test dialogue flow and logic
3. **Debug**: Use save/load and variable inspection to debug issues
4. **Full Test**: Run in actual Ren'Py for complete visual/audio testing

## Troubleshooting

### "Label not found" Error

Make sure you have a `label start:` in your scripts. This is the entry point.

### Character Colors Not Showing

The player maps specific hex colors to ANSI colors. Unknown colors default to white.

### Save File Issues

Save files are stored as `game_save.json` in the current directory. Delete this file to reset.

### Script Parse Errors

Use the `--debug` flag to see detailed error messages and stack traces.

## Future Improvements

Potential enhancements:

- Support for more Ren'Py statements
- Better image/audio preview
- GUI version using Tkinter or similar
- Integration with VS Code or other editors
- Automated testing framework
- Multiplayer/collaborative testing
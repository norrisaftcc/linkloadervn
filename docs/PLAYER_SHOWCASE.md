# Link Loader Text Player Showcase

## What It Does

The Link Loader Text Player lets you play Ren'Py visual novels in your terminal without graphics or sound. It's perfect for:

- **Rapid testing** of dialogue and game logic
- **Development** without constantly reloading Ren'Py
- **Accessibility** for screen readers
- **Remote testing** over SSH
- **Debugging** game flow and variables

## Visual Example

Here's what Link Loader looks like when played in text mode:

### 1. Starting the Game

```
$ cd planning
$ python play_linkloader.py

Link Loader - Text Adventure Mode
===================================

Options:
1. Play with typing effect (default)
2. Play without typing effect
3. Debug mode
4. Quit

Enter your choice (1-4): 2
```

### 2. Character Creation

```
Before we begin, who are you exactly?

What will you do?
1. Welcome Comrade (Space Expert)
2. Howdy Pardner (Desert Ranger) 
3. Major Tom (Space Castaway)

Enter your choice (1-3): 1
```

### 3. Dialogue Display

The terminal shows:
- Character names in **color**
- Stage directions in *italics*
- Scene changes
- Music/sound notifications

```
*Scene: bg desert night*
*Music: audio/music/azaFMP2_field7_Tumbleweeds.ogg*

Slim: Sure is getting cold out here on Syntax-4.

*Slim looks around, slightly frustrated*

Slim: Where is that neural network when you need it...

*Terminal appears with static display*

Terminal: Connecting to network...

*Clipi appears with a slight glitch effect*

Clipi: I'm here, Slim. Systems operational.
```

### 4. Interactive Choices

```
Cargo Bot: (Sh-query maintenance status sh-current sh-loader)

What will you do?
1. Reply in robot language: (Sh-maintenance underway sh-fixing)
2. Reply in human language: 'Shucks, I'm working on it!'

Enter your choice (1-2): 
```

### 5. Game Features

During gameplay, press 'h' for help:

```
Game Commands:
1. Continue
2. Save Game
3. Load Game
4. Show History
5. Show Variables
6. Quit

Enter your choice: 5

Current Variables:
cos: 2        # Cosmonaut skill
cow: -1       # Cowboy skill  
cod: 2        # Coder skill
approach: cosmonaut
mission: none
```

## How to Use

### Quick Start
```bash
cd planning
python play_linkloader.py
```

### Direct Command
```bash
# Play with options
python renpy_game_player.py ../renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game --no-typing

# Debug mode
python renpy_game_player.py ../renpy/current/renpy-8.3.7-sdk/link_loader_1_2/game --debug
```

### Create Your Own Demo
```bash
# Run the quick demo
./quick_demo.sh

# Or create a test script
python demo_player.py
```

## Features Demonstrated

✅ **Full Story Playback**
- All dialogue and narration
- Character interactions
- Scene descriptions

✅ **Game Mechanics**
- Character stats (COS/COW/COD)
- Conditional dialogue
- Menu choices
- Variable tracking

✅ **Development Tools**
- Save/Load states
- Debug information
- Dialogue history
- Variable inspection

✅ **Visual Elements as Text**
- Scene changes: `*Scene: bg desert night*`
- Character positions: `*Clipi appears at right*`
- Emotions: `*Slim appears (frustrated)*`
- Effects: `*Terminal shows static*`

## Why Use This?

1. **Test Faster**: No need to load full Ren'Py engine
2. **Debug Easier**: See variables and state instantly
3. **Write Anywhere**: Works in any terminal
4. **Share Scripts**: Others can test without Ren'Py installed
5. **Automate Testing**: Can be scripted for CI/CD

## Limitations

- No actual images displayed
- No sound playback
- Simplified visual effects
- Basic Python evaluation only

## Try It Now!

```bash
cd planning

# Play Link Loader
python play_linkloader.py

# Run the demo
./quick_demo.sh

# Explore features
python demo_player.py
```

The player preserves the complete narrative experience while providing powerful development tools for testing and debugging your visual novel!
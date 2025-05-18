# Link Loader Text Player - Example Session

This shows what playing Link Loader looks like in the text-based player.

## Starting the Game

```
$ python play_linkloader.py

Link Loader - Text Adventure Mode
===================================

This is a text-based version of Link Loader for testing and development.
The game will play in your terminal without graphics or sound.

Options:
1. Play with typing effect (default)
2. Play without typing effect
3. Debug mode
4. Quit

Enter your choice (1-4): 2

Starting game...
Tip: Press 'h' during the game for help
```

## Character Creation

```
Link Loader - Text Adventure Mode
========================================

*Scene: black*

Before we begin, who are you exactly?

Who are you?

What will you do?
1. Welcome Comrade (Space Expert)
2. Howdy Pardner (Desert Ranger)
3. Major Tom (Space Castaway)

Enter your choice (1-3): 1
```

## In-Game Display

```
*Scene: bg desert night*

*Music: audio/music/azaFMP2_field7_Tumbleweeds.ogg*

*Slim appears (looking at desert)*

Slim: Sure is getting cold out here on Syntax-4. The triple moons are all up - gonna be a bright night.

*Slim appears (looking up)*

Slim: The Company satellite should be directly above us now. Time to check in and see what today's malfunction is.

*Slim appears (calling out)*

Slim: Clipi! You online?

Press Enter to continue or 'h' for help...
```

## Character Colors

When running in a terminal that supports ANSI colors:

- **Slim** speaks in <span style="color: lightgreen">light green</span>
- **Terminal** speaks in <span style="color: lightblue">light blue</span>
- **Clipi** speaks in <span style="color: green">green</span>
- **???** speaks in <span style="color: red">red</span>

## Menu Choices

```
*Terminal appears (idle)*

Terminal: Link loader status: Error state. Cargo processing halted.

*Cargo Bot appears*

Cargo Bot: (Sh-query maintenance status sh-current sh-loader)

What will you do?
1. Reply in robot language: (Sh-maintenance underway sh-fixing syntax error sh-parenthesis mismatch)
2. Reply in human language: 'Shucks, I'm working on it! Give me a minute!'

Enter your choice (1-2): 1
```

## Help Menu

```
Press Enter to continue or 'h' for help... h

Game Commands:
1. Continue
2. Save Game
3. Load Game
4. Show History
5. Show Variables
6. Quit
7. Help

Enter your choice: 5

Current Variables:
cos: 2
cow: -1
cod: 2
approach: cosmonaut
mission: none

Press Enter to continue...
```

## Save System

```
Enter your choice: 2

Game saved!

Press Enter to continue...
```

## Stage Directions

The player shows stage directions for visual elements:

```
*Clipi disappears*

*Terminal shows static*

Terminal: Co-pilot interface restarting... Connecting to central database...

*Clipi appears (more stable now)*

Clipi: Systems restored. Should I prepare the transport?
```

## End of Episode

```
*The transport disappears into the desert night, three moons shining overhead*

Press Enter to continue or 'h' for help...

Game Over!
Final variables: {
  "cos": 2,
  "cow": -1,
  "cod": 2,
  "approach": "cosmonaut",
  "mission": "accept"
}
```

## Notes

- The player preserves all dialogue and story content
- Characters speak with their assigned colors (if terminal supports it)
- Visual elements (scenes, character positions) are shown as stage directions
- Music and sound effects are indicated but not played
- All game mechanics (variables, conditions, menus) work as expected
- Save/load functionality allows testing specific scenes
- Debug mode shows additional information for development
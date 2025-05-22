#!/usr/bin/env python3
"""
Test script demonstrating the Ren'Py game player
"""

import subprocess
import sys
import time

def test_simple_script():
    """Create and test a simple Ren'Py script"""
    
    # Create a simple test script
    test_script = '''
# Test Script
define pc = Character("Player", color="#00ff00")
define npc = Character("NPC", color="#ff0000")

default points = 0

label start:
    scene black
    
    "Welcome to the test game!"
    
    pc "Hello, I'm the player character."
    
    npc "Nice to meet you! Let me ask you something."
    
    menu:
        npc "Do you like visual novels?"
        
        "Yes, I love them!":
            $ points += 1
            npc "That's great! Me too."
            jump good_end
            
        "They're okay.":
            npc "Fair enough."
            jump neutral_end
            
        "Not really.":
            $ points -= 1
            npc "Oh, that's too bad."
            jump bad_end

label good_end:
    pc "This has been fun!"
    "You got the good ending! Points: [points]"
    return

label neutral_end:
    pc "Thanks for the chat."
    "You got the neutral ending. Points: [points]"
    return
    
label bad_end:
    pc "Well, bye then."
    "You got the bad ending. Points: [points]"
    return
'''
    
    # Write the test script
    with open("test_game.rpy", "w") as f:
        f.write(test_script)
    
    print("Created test_game.rpy")
    print("\nNow you can test the player with:")
    print("python renpy_player.py test_game.rpy --no-typing")
    print("\nOr for a full game directory:")
    print("python renpy_game_player.py ../current/renpy-8.3.7-sdk/link_loader_1_2/game --no-typing")

def test_link_loader_parse():
    """Test parsing the actual Link Loader script"""
    import sys
    sys.path.append('.')
    from renpy_game_player import RenpyGame
    
    try:
        # Load the actual game
        game = RenpyGame("../current/renpy-8.3.7-sdk/link_loader_1_2/game")
        
        print("Successfully loaded Link Loader!")
        print(f"\nCharacters found: {len(game.characters)}")
        for char_id, char in game.characters.items():
            print(f"  {char_id}: {char.name} (color: {char.color})")
        
        print(f"\nLabels found: {len(game.labels)}")
        for label in list(game.labels.keys())[:10]:
            print(f"  {label}")
        
        print(f"\nVariables found: {len(game.default_variables)}")
        for var, value in list(game.default_variables.items())[:10]:
            print(f"  {var} = {value}")
            
    except Exception as e:
        print(f"Error loading game: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("Ren'Py Game Player Test Suite")
    print("=" * 30)
    
    if len(sys.argv) > 1 and sys.argv[1] == "parse":
        test_link_loader_parse()
    else:
        test_simple_script()
        print("\nTo test parsing Link Loader, run:")
        print("python test_player.py parse")
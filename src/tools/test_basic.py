#!/usr/bin/env python3
"""
Basic test to verify our testing approach works
"""

import sys
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from renpy_game_player import RenpyGame

def test_game_loading():
    """Test that we can load the game"""
    
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    
    try:
        # Load the game
        game = RenpyGame(game_path)
        print(f"✓ Successfully loaded game from {game_path}")
        
        # Check characters
        print(f"\nCharacters found: {len(game.characters)}")
        for char_id, char in list(game.characters.items())[:3]:
            print(f"  - {char_id}: {char.name}")
        
        # Check labels
        print(f"\nLabels found: {len(game.labels)}")
        for label in list(game.labels.keys())[:5]:
            print(f"  - {label}")
            
        # Check variables
        print(f"\nDefault variables: {len(game.default_variables)}")
        for var, value in list(game.default_variables.items())[:5]:
            print(f"  - {var} = {value}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error loading game: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_label_structure():
    """Analyze the label structure to understand game flow"""
    
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    
    try:
        game = RenpyGame(game_path)
        
        print("\nAnalyzing game structure...")
        
        # Find all jumps and calls
        jumps = {}
        menus = {}
        
        for label, content in game.labels.items():
            jumps[label] = []
            menus[label] = []
            
            for indent, line, filename in content:
                line = line.strip()
                
                # Find jumps
                if line.startswith('jump '):
                    target = line[5:].strip()
                    jumps[label].append(target)
                
                # Find menus
                if line == 'menu:':
                    menus[label].append(True)
        
        # Report findings
        print(f"\nLabels with jumps:")
        for label, targets in jumps.items():
            if targets:
                print(f"  {label} -> {', '.join(targets)}")
        
        print(f"\nLabels with menus:")
        for label, has_menu in menus.items():
            if has_menu:
                print(f"  {label}")
        
        # Check reachability from start
        print(f"\nChecking reachability from 'start'...")
        visited = set()
        to_visit = ['start']
        
        while to_visit:
            current = to_visit.pop(0)
            if current in visited or current not in game.labels:
                continue
                
            visited.add(current)
            
            # Add jump targets
            if current in jumps:
                for target in jumps[current]:
                    if target not in visited:
                        to_visit.append(target)
        
        print(f"Reachable labels: {len(visited)}/{len(game.labels)}")
        
        unreachable = set(game.labels.keys()) - visited
        if unreachable:
            print(f"Unreachable labels: {unreachable}")
        
        return True
        
    except Exception as e:
        print(f"Error analyzing structure: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run basic tests"""
    print("Link Loader Basic Test")
    print("=" * 30)
    
    # Test 1: Game loading
    if not test_game_loading():
        return 1
    
    print("\n" + "-" * 30)
    
    # Test 2: Structure analysis
    if not test_label_structure():
        return 1
    
    print("\n✓ All basic tests passed!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
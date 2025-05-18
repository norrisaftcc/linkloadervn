#!/usr/bin/env python3
"""
Debug menu structure in Link Loader script
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))
from renpy_game_player import RenpyGame

def analyze_start_label():
    """Analyze the start label to understand menu structure"""
    
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    game = RenpyGame(game_path)
    
    if "start" not in game.labels:
        print("No start label found!")
        return
    
    print("Start label content:")
    print("=" * 40)
    
    lines = game.labels["start"]
    for i, (indent, line, filename) in enumerate(lines):
        print(f"{i:3d} [{indent:2d}] {line}")
    
    print("\n" + "=" * 40)
    
    # Find menus
    print("\nMenu structure:")
    in_menu = False
    menu_indent = 0
    
    for i, (indent, line, filename) in enumerate(lines):
        if line.strip() == "menu:":
            in_menu = True
            menu_indent = indent
            print(f"\nMenu at line {i}:")
            continue
            
        if in_menu:
            if indent <= menu_indent and line.strip() and not line.strip().startswith('"'):
                in_menu = False
                continue
                
            if line.strip().startswith('"') and line.strip().endswith('":'):
                print(f"  Choice: {line.strip()}")
            elif line.strip().startswith('jump '):
                print(f"    Action: {line.strip()}")

if __name__ == "__main__":
    analyze_start_label()
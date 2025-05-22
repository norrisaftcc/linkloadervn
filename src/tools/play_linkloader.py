#!/usr/bin/env python3
"""
Easy launcher for playing Link Loader in text mode
"""

import os
import sys
import subprocess

def main():
    # Get the path to the game
    game_path = "../current/renpy-8.3.7-sdk/link_loader_1_2/game"
    
    # Check if game exists
    if not os.path.exists(game_path):
        print("Error: Game not found at", game_path)
        print("Please run this from the planning directory")
        return 1
    
    print("Link Loader - Text Adventure Mode")
    print("=" * 35)
    print()
    print("This is a text-based version of Link Loader for testing and development.")
    print("The game will play in your terminal without graphics or sound.")
    print()
    print("Options:")
    print("1. Play with typing effect (default)")
    print("2. Play without typing effect") 
    print("3. Debug mode")
    print("4. Quit")
    print()
    
    while True:
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            args = ["python", "renpy_game_player.py", game_path]
            break
        elif choice == "2":
            args = ["python", "renpy_game_player.py", game_path, "--no-typing"]
            break
        elif choice == "3":
            args = ["python", "renpy_game_player.py", game_path, "--debug", "--no-typing"]
            break
        elif choice == "4":
            print("Goodbye!")
            return 0
        else:
            print("Invalid choice. Please try again.")
    
    print()
    print("Starting game...")
    print("Tip: Press 'h' during the game for help")
    print()
    
    # Run the game
    try:
        subprocess.run(args)
    except KeyboardInterrupt:
        print("\nGame interrupted.")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
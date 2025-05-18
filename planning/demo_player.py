#!/usr/bin/env python3
"""
Interactive Demo of the Ren'Py Game Player
Shows how the player works with a simple example
"""

import os
import sys
import time

# ANSI colors for prettier output
COLORS = {
    "bold": "\033[1m",
    "green": "\033[32m",
    "blue": "\033[34m",
    "yellow": "\033[33m",
    "reset": "\033[0m",
}

def show_demo():
    """Run an interactive demo of the player"""
    
    print(f"{COLORS['bold']}{COLORS['blue']}Link Loader Text Player Demo{COLORS['reset']}")
    print("=" * 30)
    print()
    print("This demo shows how the text-based player works.")
    print("You'll see how the game looks when played in terminal mode.")
    print()
    
    # Create a simple demo script
    demo_script = '''
define slim = Character("Slim", color="#c8ffc8")
define clipi = Character("Clipi", color="#00ff00")

default cos = 0
default cow = 0  
default cod = 0

label start:
    scene black
    
    "Welcome to the Link Loader Demo!"
    
    menu:
        "Choose your character background:"
        
        "Space Expert (COS +2)":
            $ cos = 2
            $ cow = -1
            $ cod = 2
            "You're from space, here to help!"
            jump demo_scene
            
        "Desert Ranger (COW +2)":
            $ cos = -1
            $ cow = 2
            $ cod = 2
            "You ride the range!"
            jump demo_scene

label demo_scene:
    scene bg desert night
    
    slim "Howdy! I'm Slim, the link loader troubleshooter."
    
    show clipi normal at right
    
    clipi "And I'm Clipi, your AI assistant!"
    
    slim "We fix broken link loaders on planet Syntax-4."
    
    menu:
        clipi "Want to see a demo of the game?"
        
        "Yes, show me!":
            clipi "Great! In the full game, you'll fix malfunctioning machinery..."
            slim "...deal with robot language puzzles..."
            clipi "...and uncover the mystery of the CDR rustlers!"
            jump end_demo
            
        "Maybe later":
            slim "No problem, partner. Come back anytime!"
            jump end_demo

label end_demo:
    "Thanks for trying the Link Loader text player!"
    
    "Your final stats:"
    "COS: [cos], COW: [cow], COD: [cod]"
    
    return
'''

    # Write the demo script
    with open("demo_game.rpy", "w") as f:
        f.write(demo_script)
    
    print(f"{COLORS['green']}Demo script created!{COLORS['reset']}")
    print()
    print("The player will show:")
    print("• Character dialogue with colors")
    print("• Menu choices")
    print("• Scene changes")
    print("• Variable tracking")
    print()
    
    # Show sample output
    print(f"{COLORS['bold']}Sample Output:{COLORS['reset']}")
    print()
    print(f"{COLORS['green']}{COLORS['bold']}Slim:{COLORS['reset']} Howdy! I'm Slim, the link loader troubleshooter.")
    print()
    print(f"{COLORS['green']}{COLORS['bold']}Clipi:{COLORS['reset']} And I'm Clipi, your AI assistant!")
    print()
    print("What will you do?")
    print(f"{COLORS['bold']}1.{COLORS['reset']} Yes, show me!")
    print(f"{COLORS['bold']}2.{COLORS['reset']} Maybe later")
    print()
    print(f"{COLORS['green']}Enter your choice (1-2): {COLORS['reset']}")
    print()
    
    print(f"{COLORS['yellow']}To run this demo:{COLORS['reset']}")
    print("python renpy_player.py demo_game.rpy --no-typing")
    print()
    print(f"{COLORS['yellow']}To play the full Link Loader game:{COLORS['reset']}")
    print("python play_linkloader.py")

def show_features():
    """Show the main features of the player"""
    
    print(f"\n{COLORS['bold']}{COLORS['blue']}Player Features{COLORS['reset']}")
    print("=" * 30)
    print()
    
    features = [
        ("Text-based gameplay", "Play Ren'Py games in your terminal"),
        ("Character colors", "Characters speak in their defined colors"),
        ("Menu choices", "Interactive decision points"),
        ("Save/Load", "Save your progress and resume later"),
        ("Variable tracking", "See how your choices affect the game"),
        ("Debug mode", "Inspect game state for development"),
        ("History", "Review past dialogue"),
        ("No graphics needed", "Test game logic without assets"),
    ]
    
    for feature, description in features:
        print(f"{COLORS['bold']}{feature}:{COLORS['reset']} {description}")
    
    print()

def main():
    """Main demo function"""
    print(f"{COLORS['bold']}Ren'Py Text Player Demo{COLORS['reset']}")
    print("=" * 30)
    print()
    
    while True:
        print("What would you like to see?")
        print("1. Interactive demo")
        print("2. Feature list")
        print("3. How to play Link Loader")
        print("4. Exit")
        print()
        
        choice = input("Enter your choice (1-4): ")
        
        if choice == "1":
            show_demo()
        elif choice == "2":
            show_features()
        elif choice == "3":
            print(f"\n{COLORS['bold']}{COLORS['blue']}Playing Link Loader{COLORS['reset']}")
            print("=" * 30)
            print()
            print("From the planning directory, run:")
            print()
            print(f"{COLORS['yellow']}python play_linkloader.py{COLORS['reset']}")
            print()
            print("This will give you options to:")
            print("• Play with typing effect")
            print("• Play instantly (no typing)")
            print("• Run in debug mode")
            print()
            print("The game will play in your terminal with:")
            print("• All dialogue and story")
            print("• Interactive choices")
            print("• Character stats")
            print("• Save/load support")
            print()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")
        print("\n" * 2)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Console-based conversation tree player for Link Loader

This script plays dialogue trees from JSON files in a command-line interface.
"""

import json
import os
import sys
import time
import re
import random
from typing import Dict, List, Any, Optional, Union

# ANSI color codes for pretty printing
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
    "bg_black": "\033[40m",
    "bg_red": "\033[41m",
    "bg_green": "\033[42m",
    "bg_yellow": "\033[43m",
    "bg_blue": "\033[44m",
    "bg_magenta": "\033[45m",
    "bg_cyan": "\033[46m",
    "bg_white": "\033[47m",
}

# Character color mapping
CHARACTER_COLORS = {
    "Slim": "green",
    "Clipi": "cyan",
    "Terminal": "blue",
    "Cargo Bot": "yellow",
    "???": "red"
}

# Default delay between text chunks for typing effect (in seconds)
DEFAULT_TYPING_SPEED = 0.03

class DialoguePlayer:
    """A console-based dialogue tree player"""
    
    def __init__(self, dialogue_path: str, typing_speed: float = DEFAULT_TYPING_SPEED):
        """Initialize the dialogue player with the path to a dialogue file"""
        self.dialogue_path = dialogue_path
        self.dialogue_data = self._load_dialogue()
        self.variables = self.dialogue_data.get("variables", {})
        self.current_node_id = self.dialogue_data.get("start", "")
        self.history = []
        self.typing_speed = typing_speed
        
    def _load_dialogue(self) -> Dict:
        """Load the dialogue tree from a JSON file"""
        try:
            with open(self.dialogue_path, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Error: Dialogue file '{self.dialogue_path}' not found.")
            sys.exit(1)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid JSON in dialogue file: {e}")
            sys.exit(1)
            
    def _get_current_node(self) -> Dict:
        """Get the current node from the dialogue tree"""
        nodes = self.dialogue_data.get("nodes", {})
        if self.current_node_id not in nodes:
            print(f"Error: Node '{self.current_node_id}' not found in dialogue tree.")
            sys.exit(1)
        return nodes[self.current_node_id]
    
    def _evaluate_condition(self, condition: str) -> bool:
        """Evaluate a condition based on the current variables"""
        if not condition:
            return True
            
        # Create a context with the current variables
        context = dict(self.variables)
        
        try:
            # Evaluate the condition in the context
            return eval(condition, {"__builtins__": {}}, context)
        except Exception as e:
            print(f"Error evaluating condition '{condition}': {e}")
            return False
    
    def _apply_effects(self, effects: List[Dict]) -> None:
        """Apply effects to the variables"""
        if not effects:
            return
            
        for effect in effects:
            effect_type = effect.get("type", "")
            variable = effect.get("variable", "")
            value = effect.get("value", None)
            
            if not variable and effect_type != "script":
                continue
                
            if effect_type == "set":
                self.variables[variable] = value
            elif effect_type == "inc":
                self.variables[variable] = self.variables.get(variable, 0) + value
            elif effect_type == "dec":
                self.variables[variable] = self.variables.get(variable, 0) - value
            elif effect_type == "toggle":
                self.variables[variable] = not self.variables.get(variable, False)
            elif effect_type == "push":
                if variable not in self.variables:
                    self.variables[variable] = []
                self.variables[variable].append(value)
            elif effect_type == "pop":
                if variable in self.variables and isinstance(self.variables[variable], list):
                    if self.variables[variable]:
                        self.variables[variable].pop()
            elif effect_type == "script":
                script = effect.get("script", "")
                if script:
                    try:
                        # Create a context with the current variables
                        context = dict(self.variables)
                        # Execute the script in the context
                        exec(script, {"__builtins__": {}}, context)
                        # Update the variables with the context
                        self.variables.update(context)
                    except Exception as e:
                        print(f"Error executing script: {e}")
    
    def _print_styled_text(self, text: str, speaker: Optional[str] = None, typing: bool = True) -> None:
        """Print text with styling and optional typing effect"""
        # Apply speaker colors
        if speaker:
            color = CHARACTER_COLORS.get(speaker, "white")
            prefix = f"{COLORS[color]}{COLORS['bold']}{speaker}:{COLORS['reset']} "
            print(prefix, end="")
        
        # Handle robot language formatting
        text = self._format_robot_language(text)
        
        if typing:
            self._type_text(text)
        else:
            print(text)
        
        print()  # Add a newline after the text
    
    def _format_robot_language(self, text: str) -> str:
        """Format robot language with color and style"""
        # Find text that looks like (Sh-something sh-something)
        robot_pattern = r'\(Sh-[^)]+\)'
        
        # Replace robot language with styled version
        def robot_replacer(match):
            robot_text = match.group(0)
            return f"{COLORS['yellow']}{COLORS['italic']}{robot_text}{COLORS['reset']}"
            
        return re.sub(robot_pattern, robot_replacer, text)
    
    def _type_text(self, text: str) -> None:
        """Print text with a typing animation effect"""
        for char in text:
            print(char, end="", flush=True)
            time.sleep(self.typing_speed)
    
    def _print_choices(self, choices: List[Dict]) -> List[Dict]:
        """Print the available choices and return the valid ones"""
        valid_choices = []
        
        print(f"\n{COLORS['bold']}What will you do?{COLORS['reset']}\n")
        
        choice_num = 1
        for choice in choices:
            condition = choice.get("condition", "")
            if self._evaluate_condition(condition):
                print(f"{COLORS['bold']}{choice_num}.{COLORS['reset']} {choice['text']}")
                valid_choices.append((choice_num, choice))
                choice_num += 1
        
        return valid_choices
    
    def _get_user_choice(self, valid_choices: List[Dict]) -> Dict:
        """Get user choice from input"""
        if not valid_choices:
            print("No valid choices available. Ending dialogue.")
            return None
            
        while True:
            try:
                choice = input(f"\n{COLORS['green']}Enter your choice (1-{len(valid_choices)}): {COLORS['reset']}")
                choice_num = int(choice)
                
                if 1 <= choice_num <= len(valid_choices):
                    return valid_choices[choice_num - 1][1]
                else:
                    print(f"Please enter a number between 1 and {len(valid_choices)}.")
            except ValueError:
                print("Please enter a valid number.")
    
    def play_node(self) -> None:
        """Play the current dialogue node"""
        # Get the current node
        node = self._get_current_node()
        
        # Apply onentry effects
        self._apply_effects(node.get("onentry", []))
        
        # Add to history
        self.history.append(self.current_node_id)
        
        # Clear screen for better presentation
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Print node title if available
        if "title" in node:
            print(f"{COLORS['bold']}{COLORS['underline']}{node['title']}{COLORS['reset']}\n")
        
        # Get the speaker
        speaker = node.get("speaker", self.dialogue_data.get("default_speaker", None))
        
        # Print the content
        content = node.get("content", "")
        if content:
            self._print_styled_text(content, speaker)
            
        # Wait for user to press enter if no choices
        if "choices" not in node:
            input(f"\n{COLORS['dim']}Press Enter to continue...{COLORS['reset']}")
            
            # Move to the next node
            self._apply_effects(node.get("onexit", []))
            self.current_node_id = node.get("next")
            
        else:
            # Print and process choices
            valid_choices = self._print_choices(node.get("choices", []))
            chosen = self._get_user_choice(valid_choices)
            
            if chosen:
                # Apply choice effects
                self._apply_effects(chosen.get("effects", []))
                
                # Apply onexit effects
                self._apply_effects(node.get("onexit", []))
                
                # Move to the next node
                self.current_node_id = chosen.get("next")
    
    def play(self) -> None:
        """Play the entire dialogue tree"""
        # Print the title
        title = self.dialogue_data.get("title", "Dialogue")
        author = self.dialogue_data.get("author", "")
        version = self.dialogue_data.get("version", "")
        
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print(f"{COLORS['bold']}{COLORS['bg_blue']}{COLORS['white']} {title} {COLORS['reset']}")
        if author:
            print(f"By: {author}")
        if version:
            print(f"Version: {version}")
        print()
        
        input(f"{COLORS['dim']}Press Enter to begin...{COLORS['reset']}")
        
        # Play until we reach a None node
        while self.current_node_id is not None:
            self.play_node()
            
        # Print end of dialogue
        print(f"\n{COLORS['bold']}{COLORS['blue']}End of dialogue.{COLORS['reset']}")
        print(f"Variables: {json.dumps(self.variables, indent=2)}")
    
    def reset(self) -> None:
        """Reset the dialogue to the beginning"""
        self.variables = {}
        for key, value in self.dialogue_data.get("variables", {}).items():
            self.variables[key] = value
        self.current_node_id = self.dialogue_data.get("start", "")
        self.history = []


def main():
    """Main function to run the dialogue player"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Console-based dialogue tree player")
    parser.add_argument("dialogue_file", help="Path to the dialogue JSON file")
    parser.add_argument("--speed", type=float, default=DEFAULT_TYPING_SPEED, help="Typing animation speed (seconds per character)")
    parser.add_argument("--no-typing", action="store_true", help="Disable typing animation")
    
    args = parser.parse_args()
    
    player = DialoguePlayer(args.dialogue_file, typing_speed=0 if args.no_typing else args.speed)
    player.play()


if __name__ == "__main__":
    main()
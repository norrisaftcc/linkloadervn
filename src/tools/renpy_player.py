#!/usr/bin/env python3
"""
Ren'Py Script Player

A standalone player for Ren'Py visual novel scripts that allows you to
play through games in text format without the full Ren'Py engine.

Supports:
- Character definitions
- Variables and conditions
- Labels and jumps
- Menus and choices
- Basic expressions and Python evaluation
- Show/hide commands (displayed as text)
"""

import os
import re
import sys
import json
import time
import argparse
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
from collections import defaultdict

# ANSI color codes for pretty printing
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

class RenpyCharacter:
    """Represents a Ren'Py character"""
    def __init__(self, name, color="#ffffff", **kwargs):
        self.name = name if name else "Narrator"
        self.color = color
        self.kwargs = kwargs

class RenpyScript:
    """Parses and holds a Ren'Py script structure"""
    
    def __init__(self, script_path: str):
        self.script_path = script_path
        self.characters = {}
        self.variables = {}
        self.labels = {}
        self.current_label = "start"
        self.call_stack = []
        self.menu_choices = []
        
        # Parse the script
        self._parse_script()
    
    def _parse_script(self):
        """Parse the entire Ren'Py script"""
        with open(self.script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove comments but preserve them for parsing directives
        lines = content.split('\n')
        
        # First pass: extract character definitions and default variables
        self._parse_definitions(lines)
        
        # Second pass: extract labels and their content
        self._parse_labels(lines)
    
    def _parse_definitions(self, lines: List[str]):
        """Parse character definitions and default variables"""
        for line in lines:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Character definitions
            if line.startswith('define '):
                match = re.match(r'define\s+(\w+)\s*=\s*Character\((.*)\)', line)
                if match:
                    char_id, char_args = match.groups()
                    # Parse character arguments
                    # This is simplified - real implementation would need proper Python parsing
                    name_match = re.search(r'["\']([^"\']+)["\']', char_args)
                    color_match = re.search(r'color\s*=\s*["\']([^"\']+)["\']', char_args)
                    
                    name = name_match.group(1) if name_match else None
                    color = color_match.group(1) if color_match else "#ffffff"
                    
                    self.characters[char_id] = RenpyCharacter(name, color)
            
            # Default variables
            elif line.startswith('default '):
                match = re.match(r'default\s+(\w+)\s*=\s*(.*)', line)
                if match:
                    var_id, value = match.groups()
                    # Evaluate the value
                    try:
                        self.variables[var_id] = eval(value)
                    except:
                        # If evaluation fails, store as string
                        self.variables[var_id] = value
    
    def _parse_labels(self, lines: List[str]):
        """Parse labels and their content"""
        current_label = None
        current_content = []
        indentation_level = 0
        
        for i, line in enumerate(lines):
            # Check for label definition
            if line.strip().startswith('label ') and line.strip().endswith(':'):
                # Save previous label
                if current_label:
                    self.labels[current_label] = current_content
                
                # Start new label
                label_match = re.match(r'label\s+(\w+):', line.strip())
                if label_match:
                    current_label = label_match.group(1)
                    current_content = []
                    indentation_level = 0
            
            elif current_label:
                # Store content for current label
                if line.strip():
                    # Calculate indentation
                    indent = len(line) - len(line.lstrip())
                    current_content.append((indent, line))
        
        # Save the last label
        if current_label:
            self.labels[current_label] = current_content

class RenpyPlayer:
    """Plays a parsed Ren'Py script"""
    
    def __init__(self, script: RenpyScript, typing_speed: float = 0.03):
        self.script = script
        self.typing_speed = typing_speed
        self.current_label = "start"
        self.call_stack = []
        self.variables = dict(script.variables)
        self.history = []
        self.shown_images = {}
        
    def _evaluate_expression(self, expr: str) -> Any:
        """Evaluate a Python expression in the game context"""
        try:
            # Create a safe context with variables
            context = dict(self.variables)
            return eval(expr, {"__builtins__": {}}, context)
        except:
            return expr
    
    def _execute_python(self, code: str):
        """Execute Python code in the game context"""
        try:
            # Create a context with variables
            context = dict(self.variables)
            exec(code, {"__builtins__": {}}, context)
            # Update variables with any changes
            self.variables.update(context)
        except Exception as e:
            print(f"Error executing Python: {e}")
    
    def _print_dialogue(self, speaker_id: str, text: str):
        """Print dialogue with character formatting"""
        if speaker_id in self.script.characters:
            char = self.script.characters[speaker_id]
            color_name = self._color_to_ansi(char.color)
            print(f"{COLORS[color_name]}{COLORS['bold']}{char.name}:{COLORS['reset']} {text}")
        else:
            # Narrator or undefined character
            print(text)
        
        # Add typing effect
        time.sleep(len(text) * self.typing_speed)
    
    def _color_to_ansi(self, hex_color: str) -> str:
        """Convert hex color to nearest ANSI color"""
        # Simple mapping - could be improved
        color_map = {
            "#c8ffc8": "green",
            "#c8c8ff": "blue", 
            "#00ff00": "green",
            "#ff5555": "red",
            "#aaaaaa": "white",
        }
        return color_map.get(hex_color, "white")
    
    def _parse_dialogue_line(self, line: str) -> Tuple[Optional[str], str]:
        """Parse a dialogue line to extract speaker and text"""
        # Check for character dialogue
        for char_id in self.script.characters:
            if line.strip().startswith(f'{char_id} "'):
                text_match = re.match(f'{char_id}\\s+"([^"]*)"', line.strip())
                if text_match:
                    return char_id, text_match.group(1)
        
        # Check for narrator text
        if line.strip().startswith('"') and line.strip().endswith('"'):
            return None, line.strip()[1:-1]
        
        return None, None
    
    def _process_menu(self, lines: List[Tuple[int, str]], start_idx: int) -> int:
        """Process a menu block and return the next index"""
        choices = []
        idx = start_idx + 1
        menu_indent = lines[start_idx][0]
        
        # Skip menu prompt if present
        if idx < len(lines) and lines[idx][1].strip().startswith('"'):
            prompt_match = re.match(r'\s*"([^"]*)"', lines[idx][1])
            if prompt_match:
                print(f"\n{prompt_match.group(1)}")
                idx += 1
        
        # Collect choices
        while idx < len(lines):
            indent, line = lines[idx]
            
            # Stop if we've dedented past the menu
            if indent <= menu_indent and line.strip() and not line.strip().startswith('"'):
                break
            
            # Parse choice
            choice_match = re.match(r'\s*"([^"]*)"(\s+if\s+(.+))?:', line)
            if choice_match:
                choice_text = choice_match.group(1)
                condition = choice_match.group(3)
                
                # Check condition if present
                if condition:
                    if not self._evaluate_expression(condition):
                        idx += 1
                        continue
                
                choices.append({
                    'text': choice_text,
                    'index': idx
                })
            
            idx += 1
        
        # Display choices
        print("\nChoices:")
        for i, choice in enumerate(choices):
            print(f"{i+1}. {choice['text']}")
        
        # Get player choice
        while True:
            try:
                choice_num = int(input("\nEnter your choice: "))
                if 1 <= choice_num <= len(choices):
                    chosen = choices[choice_num - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number")
        
        # Execute the chosen block
        choice_idx = chosen['index'] + 1
        choice_indent = lines[chosen['index']][0]
        
        while choice_idx < len(lines):
            indent, line = lines[choice_idx]
            
            # Stop if we've dedented past the choice
            if indent <= choice_indent and line.strip() and not line.strip().startswith('$'):
                break
            
            # Process the line
            self._process_line(line.strip())
            choice_idx += 1
        
        return idx
    
    def _process_line(self, line: str):
        """Process a single line of Ren'Py script"""
        line = line.strip()
        
        if not line or line.startswith('#'):
            return
        
        # Python code execution
        if line.startswith('$'):
            code = line[1:].strip()
            self._execute_python(code)
        
        # Show command
        elif line.startswith('show '):
            # Extract character and emotion
            parts = line[5:].split()
            if len(parts) >= 2:
                char, emotion = parts[0], parts[1]
                self.shown_images[char] = emotion
                print(f"*{char} appears ({emotion})*")
        
        # Hide command
        elif line.startswith('hide '):
            char = line[5:].strip()
            if char in self.shown_images:
                del self.shown_images[char]
                print(f"*{char} disappears*")
        
        # Scene command
        elif line.startswith('scene '):
            bg = line[6:].strip()
            self.shown_images.clear()
            print(f"\n*Scene: {bg}*\n")
        
        # Jump command
        elif line.startswith('jump '):
            label = line[5:].strip()
            self.current_label = label
        
        # Call command
        elif line.startswith('call '):
            label = line[5:].strip()
            self.call_stack.append(self.current_label)
            self.current_label = label
        
        # Return command
        elif line == 'return':
            if self.call_stack:
                self.current_label = self.call_stack.pop()
            else:
                self.current_label = None
        
        # Conditional
        elif line.startswith('if '):
            condition = line[3:].rstrip(':')
            return self._evaluate_expression(condition)
        
        # Play music/sound
        elif line.startswith('play '):
            parts = line.split()
            if len(parts) >= 3:
                media_type = parts[1]
                file_path = ' '.join(parts[2:]).strip('"')
                print(f"*Playing {media_type}: {file_path}*")
        
        # Dialogue
        else:
            speaker, text = self._parse_dialogue_line(line)
            if text:
                self._print_dialogue(speaker, text)
    
    def play_label(self, label: str):
        """Play a specific label"""
        if label not in self.script.labels:
            print(f"Error: Label '{label}' not found")
            return
        
        lines = self.script.labels[label]
        idx = 0
        
        while idx < len(lines):
            indent, line = lines[idx]
            line = line.strip()
            
            # Handle menu blocks specially
            if line.startswith('menu:'):
                idx = self._process_menu(lines, idx)
            else:
                # Process regular lines
                result = self._process_line(line)
                
                # Handle conditionals
                if line.startswith('if ') and line.endswith(':'):
                    # Skip block if condition is false
                    if not result:
                        # Find the end of this block
                        if_indent = indent
                        idx += 1
                        while idx < len(lines):
                            next_indent, next_line = lines[idx]
                            if next_indent <= if_indent and next_line.strip():
                                break
                            idx += 1
                        continue
                
                idx += 1
            
            # Check if we need to jump to another label
            if self.current_label != label:
                self.play_label(self.current_label)
                return
    
    def play(self):
        """Play the entire script starting from 'start' label"""
        print("Link Loader - Text Mode")
        print("=" * 30)
        print()
        
        self.current_label = "start"
        
        while self.current_label:
            self.play_label(self.current_label)
            
            # Check if we're done
            if self.current_label is None:
                break
        
        print("\nGame Over")
        print(f"Final variables: {json.dumps(self.variables, indent=2)}")

def main():
    parser = argparse.ArgumentParser(description="Play Ren'Py scripts in text mode")
    parser.add_argument("script", help="Path to the Ren'Py script file (usually script.rpy)")
    parser.add_argument("--speed", type=float, default=0.01, 
                        help="Typing speed for dialogue (seconds per character)")
    parser.add_argument("--no-typing", action="store_true", 
                        help="Disable typing animation")
    
    args = parser.parse_args()
    
    # Parse the script
    try:
        script = RenpyScript(args.script)
    except FileNotFoundError:
        print(f"Error: Script file '{args.script}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing script: {e}")
        sys.exit(1)
    
    # Play the script
    typing_speed = 0 if args.no_typing else args.speed
    player = RenpyPlayer(script, typing_speed)
    
    try:
        player.play()
    except KeyboardInterrupt:
        print("\n\nGame interrupted by user")
    except Exception as e:
        print(f"\nError during gameplay: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
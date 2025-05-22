#!/usr/bin/env python3
"""
Enhanced Ren'Py Game Player

A more complete standalone player for Ren'Py games that:
- Loads and plays complete game directories
- Handles multiple script files
- Supports more Ren'Py features
- Provides better error handling and game state management
"""

import os
import re
import sys
import json
import time
import glob
import argparse
from typing import Dict, List, Any, Optional, Tuple, Set
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass

# ANSI color codes
COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "dim": "\033[2m",
    "italic": "\033[3m",
    "underline": "\033[4m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",
}

# Character color mapping from the game
CHARACTER_COLORS = {
    "#c8ffc8": "green",  # Slim
    "#c8c8ff": "blue",   # Terminal
    "#00ff00": "green",  # Clipi
    "#ff5555": "red",    # ???
    "#aaaaaa": "white",  # Cargo Bot
}

@dataclass
class Character:
    """Represents a game character"""
    name: str
    color: str
    kwargs: Dict[str, Any]

@dataclass
class GameState:
    """Represents the current game state"""
    current_label: str
    variables: Dict[str, Any]
    call_stack: List[str]
    shown_images: Dict[str, str]
    history: List[str]
    music: Optional[str]
    sound: Optional[str]

class RenpyGame:
    """Represents a complete Ren'Py game"""
    
    def __init__(self, game_dir: str):
        self.game_dir = Path(game_dir)
        self.characters: Dict[str, Character] = {}
        self.default_variables: Dict[str, Any] = {}
        self.labels: Dict[str, List[Tuple[int, str, str]]] = {}  # label -> [(indent, line, filename)]
        self.images: Dict[str, str] = {}  # image name -> file path
        self.audio: Dict[str, str] = {}   # audio name -> file path
        
        # Load the game
        self._load_game()
    
    def _load_game(self):
        """Load all game resources"""
        # Find all .rpy files
        rpy_files = glob.glob(str(self.game_dir / "**/*.rpy"), recursive=True)
        
        if not rpy_files:
            raise ValueError(f"No .rpy files found in {self.game_dir}")
        
        # Parse all script files
        for rpy_file in rpy_files:
            self._parse_script_file(rpy_file)
        
        # Load images and audio
        self._load_assets()
    
    def _parse_script_file(self, filepath: str):
        """Parse a single .rpy file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_label = None
        label_content = []
        
        for i, line in enumerate(lines):
            # Remove trailing whitespace but preserve indentation
            line = line.rstrip()
            
            # Skip empty lines
            if not line.strip():
                if current_label:
                    label_content.append((len(line) - len(line.lstrip()), line, filepath))
                continue
            
            # Character definitions
            if line.strip().startswith('define '):
                self._parse_character_definition(line)
            
            # Default variables
            elif line.strip().startswith('default '):
                self._parse_default_variable(line)
            
            # Labels
            elif re.match(r'^\s*label\s+\w+\s*:', line):
                # Save previous label
                if current_label:
                    self.labels[current_label] = label_content
                
                # Start new label
                match = re.match(r'^\s*label\s+(\w+)\s*:', line)
                if match:
                    current_label = match.group(1)
                    label_content = []
            
            # Content within labels
            elif current_label:
                indent = len(line) - len(line.lstrip())
                label_content.append((indent, line, filepath))
        
        # Save last label
        if current_label:
            self.labels[current_label] = label_content
    
    def _parse_character_definition(self, line: str):
        """Parse a character definition line"""
        match = re.match(r'define\s+(\w+)\s*=\s*Character\((.*)\)', line.strip())
        if match:
            char_id, args = match.groups()
            
            # Parse arguments (simplified)
            name = None
            color = "#ffffff"
            
            # Extract name
            name_match = re.search(r'(?:_\()?["\']([^"\']+)["\'](?:\))?', args)
            if name_match:
                name = name_match.group(1)
            
            # Extract color
            color_match = re.search(r'color\s*=\s*["\']([^"\']+)["\']', args)
            if color_match:
                color = color_match.group(1)
            
            self.characters[char_id] = Character(name or char_id, color, {})
    
    def _parse_default_variable(self, line: str):
        """Parse a default variable definition"""
        match = re.match(r'default\s+(\w+)\s*=\s*(.*)', line.strip())
        if match:
            var_id, value = match.groups()
            try:
                # Safely evaluate the value
                self.default_variables[var_id] = eval(value, {"__builtins__": {}})
            except:
                self.default_variables[var_id] = value.strip()
    
    def _load_assets(self):
        """Load image and audio assets"""
        # Load images
        image_extensions = ['.png', '.jpg', '.jpeg', '.webp']
        for ext in image_extensions:
            for img_path in glob.glob(str(self.game_dir / f"**/*{ext}"), recursive=True):
                img_name = Path(img_path).stem.replace(' ', '_')
                self.images[img_name] = img_path
        
        # Load audio
        audio_extensions = ['.mp3', '.ogg', '.opus', '.wav']
        for ext in audio_extensions:
            for audio_path in glob.glob(str(self.game_dir / f"**/*{ext}"), recursive=True):
                audio_name = Path(audio_path).name
                self.audio[audio_name] = audio_path

class GamePlayer:
    """Plays a Ren'Py game in text mode"""
    
    def __init__(self, game: RenpyGame, typing_speed: float = 0.02):
        self.game = game
        self.typing_speed = typing_speed
        self.state = GameState(
            current_label="start",
            variables=dict(game.default_variables),
            call_stack=[],
            shown_images={},
            history=[],
            music=None,
            sound=None
        )
        self.save_file = "game_save.json"
    
    def save_game(self):
        """Save the current game state"""
        save_data = {
            "current_label": self.state.current_label,
            "variables": self.state.variables,
            "call_stack": self.state.call_stack,
            "shown_images": self.state.shown_images,
            "history": self.state.history[-50:],  # Keep last 50 history items
        }
        
        with open(self.save_file, 'w') as f:
            json.dump(save_data, f, indent=2)
        
        print(f"\n{COLORS['green']}Game saved!{COLORS['reset']}")
    
    def load_game(self):
        """Load a saved game state"""
        try:
            with open(self.save_file, 'r') as f:
                save_data = json.load(f)
            
            self.state.current_label = save_data["current_label"]
            self.state.variables = save_data["variables"]
            self.state.call_stack = save_data["call_stack"]
            self.state.shown_images = save_data["shown_images"]
            self.state.history = save_data["history"]
            
            print(f"\n{COLORS['green']}Game loaded!{COLORS['reset']}")
            return True
        except FileNotFoundError:
            print(f"\n{COLORS['red']}No save file found{COLORS['reset']}")
            return False
    
    def clear_screen(self):
        """Clear the screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_dialogue(self, speaker_id: Optional[str], text: str):
        """Print dialogue with formatting"""
        if speaker_id and speaker_id in self.game.characters:
            char = self.game.characters[speaker_id]
            color = CHARACTER_COLORS.get(char.color, "white")
            print(f"{COLORS[color]}{COLORS['bold']}{char.name}:{COLORS['reset']} ", end="")
        
        # Handle typing effect
        if self.typing_speed > 0:
            for char in text:
                print(char, end="", flush=True)
                time.sleep(self.typing_speed)
            print()
        else:
            print(text)
        
        # Add to history
        if speaker_id:
            self.state.history.append(f"{speaker_id}: {text}")
        else:
            self.state.history.append(text)
    
    def print_stage_direction(self, text: str):
        """Print stage directions in italics"""
        print(f"{COLORS['dim']}{COLORS['italic']}*{text}*{COLORS['reset']}")
    
    def execute_python(self, code: str):
        """Execute Python code in game context"""
        try:
            # Create safe context
            context = dict(self.state.variables)
            exec(code, {"__builtins__": {}}, context)
            self.state.variables.update(context)
        except Exception as e:
            print(f"{COLORS['red']}Error executing code: {e}{COLORS['reset']}")
    
    def evaluate_expression(self, expr: str) -> Any:
        """Evaluate a Python expression"""
        try:
            context = dict(self.state.variables)
            return eval(expr, {"__builtins__": {}}, context)
        except:
            return False
    
    def process_line(self, line: str) -> Optional[str]:
        """Process a single line and return any jump target"""
        line = line.strip()
        
        if not line or line.startswith('#'):
            return None
        
        # Python execution
        if line.startswith('$'):
            self.execute_python(line[1:].strip())
        
        # Scene change
        elif line.startswith('scene '):
            scene = line[6:].split(' with ')[0].strip()
            self.state.shown_images.clear()
            self.print_stage_direction(f"Scene: {scene}")
            print()
        
        # Show character/image
        elif line.startswith('show '):
            parts = line[5:].strip().split()
            if parts:
                char = parts[0]
                emotion = parts[1] if len(parts) > 1 else "normal"
                position = ""
                
                # Look for position
                if ' at ' in line:
                    position = line.split(' at ')[1].split()[0]
                    position = f" at {position}"
                
                self.state.shown_images[char] = emotion
                self.print_stage_direction(f"{char} appears ({emotion}){position}")
        
        # Hide character/image
        elif line.startswith('hide '):
            char = line[5:].split()[0]
            if char in self.state.shown_images:
                del self.state.shown_images[char]
                self.print_stage_direction(f"{char} disappears")
        
        # Play music/sound
        elif line.startswith('play '):
            parts = line.split('"')
            if len(parts) >= 2:
                file_name = parts[1]
                if 'music' in line:
                    self.state.music = file_name
                    self.print_stage_direction(f"Music: {file_name}")
                else:
                    self.state.sound = file_name
                    self.print_stage_direction(f"Sound: {file_name}")
        
        # Stop music/sound  
        elif line.startswith('stop '):
            if 'music' in line:
                self.state.music = None
                self.print_stage_direction("Music stops")
        
        # Jump
        elif line.startswith('jump '):
            return line[5:].strip()
        
        # Call
        elif line.startswith('call '):
            label = line[5:].strip()
            self.state.call_stack.append(self.state.current_label)
            return label
        
        # Return
        elif line == 'return':
            if self.state.call_stack:
                return self.state.call_stack.pop()
            else:
                return None
        
        # Dialogue
        else:
            # Check for character dialogue
            for char_id in self.game.characters:
                if line.startswith(f'{char_id} "') and line.endswith('"'):
                    text = line[len(char_id)+2:-1]
                    self.print_dialogue(char_id, text)
                    return None
            
            # Narrator text
            if line.startswith('"') and line.endswith('"'):
                self.print_dialogue(None, line[1:-1])
        
        return None
    
    def process_menu(self, lines: List[Tuple[int, str, str]], start_idx: int) -> Tuple[Optional[str], int]:
        """Process a menu and return jump target and next index"""
        menu_indent = lines[start_idx][0]
        idx = start_idx + 1
        
        # Check for menu prompt
        prompt = None
        if idx < len(lines) and '"' in lines[idx][1]:
            match = re.match(r'\s*"([^"]*)"', lines[idx][1])
            if match:
                prompt = match.group(1)
                idx += 1
        
        # Collect choices
        choices = []
        while idx < len(lines):
            indent, line, _ = lines[idx]
            
            # Stop at dedent
            if indent <= menu_indent and line.strip() and not line.strip().startswith('"'):
                break
            
            # Parse choice
            choice_match = re.match(r'\s*"([^"]*)"(\s+if\s+(.+))?:', line)
            if choice_match:
                text = choice_match.group(1)
                condition = choice_match.group(3)
                
                # Check condition
                if condition and not self.evaluate_expression(condition):
                    idx += 1
                    continue
                
                choices.append({
                    'text': text,
                    'index': idx,
                    'indent': indent
                })
            
            idx += 1
        
        # Display menu
        if prompt:
            print(f"\n{prompt}")
        
        print("\nWhat will you do?")
        for i, choice in enumerate(choices, 1):
            print(f"{COLORS['bold']}{i}.{COLORS['reset']} {choice['text']}")
        
        # Get player choice
        while True:
            try:
                choice_input = input(f"\n{COLORS['green']}Enter your choice (1-{len(choices)}): {COLORS['reset']}")
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    chosen = choices[choice_num - 1]
                    break
                else:
                    print(f"Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("Please enter a valid number")
        
        # Process chosen block
        choice_idx = chosen['index'] + 1
        choice_indent = chosen['indent']
        jump_target = None
        
        while choice_idx < len(lines):
            indent, line, _ = lines[choice_idx]
            
            # Stop at dedent
            if indent <= choice_indent and line.strip():
                break
            
            # Process line
            target = self.process_line(line)
            if target:
                jump_target = target
                break
            
            choice_idx += 1
        
        return jump_target, idx
    
    def play_label(self, label: str):
        """Play a specific label"""
        if label not in self.game.labels:
            print(f"{COLORS['red']}Error: Label '{label}' not found{COLORS['reset']}")
            return
        
        lines = self.game.labels[label]
        idx = 0
        
        while idx < len(lines):
            indent, line, _ = lines[idx]
            
            # Handle menus
            if line.strip() == 'menu:':
                jump_target, next_idx = self.process_menu(lines, idx)
                if jump_target:
                    self.state.current_label = jump_target
                    return
                idx = next_idx
            
            # Handle conditionals
            elif line.strip().startswith('if ') and line.strip().endswith(':'):
                condition = line.strip()[3:-1]
                if_indent = indent
                
                if self.evaluate_expression(condition):
                    # Process if block
                    idx += 1
                else:
                    # Skip to else/elif or end of block
                    idx += 1
                    while idx < len(lines):
                        next_indent, next_line, _ = lines[idx]
                        if next_indent <= if_indent:
                            if next_line.strip().startswith(('else:', 'elif ')):
                                continue
                            break
                        idx += 1
            
            # Process regular lines
            else:
                jump_target = self.process_line(line)
                if jump_target:
                    self.state.current_label = jump_target
                    return
                idx += 1
    
    def show_help(self):
        """Show help menu"""
        print(f"\n{COLORS['bold']}Game Commands:{COLORS['reset']}")
        print("1. Continue")
        print("2. Save Game")
        print("3. Load Game")
        print("4. Show History")
        print("5. Show Variables")
        print("6. Quit")
        print("7. Help")
    
    def show_history(self):
        """Show dialogue history"""
        print(f"\n{COLORS['bold']}Recent History:{COLORS['reset']}")
        for line in self.state.history[-20:]:
            print(line)
    
    def show_variables(self):
        """Show current variables"""
        print(f"\n{COLORS['bold']}Current Variables:{COLORS['reset']}")
        for var, value in self.state.variables.items():
            if not var.startswith('_'):  # Skip internal variables
                print(f"{var}: {value}")
    
    def play(self):
        """Main game loop"""
        self.clear_screen()
        print(f"{COLORS['bold']}Link Loader - Text Adventure Mode{COLORS['reset']}")
        print("="*40)
        print()
        
        # Check for save file
        if os.path.exists(self.save_file):
            print("Save file found. Load it? (y/n): ", end="")
            if input().lower() == 'y':
                self.load_game()
        
        # Main game loop
        while self.state.current_label:
            try:
                self.play_label(self.state.current_label)
                
                # End of label reached
                if self.state.current_label is None:
                    break
                
                # Show menu between labels
                print(f"\n{COLORS['dim']}Press Enter to continue or 'h' for help...{COLORS['reset']}")
                choice = input()
                
                if choice.lower() == 'h':
                    self.show_help()
                    choice = input("\nEnter your choice: ")
                    
                    if choice == '2':
                        self.save_game()
                    elif choice == '3':
                        self.load_game()
                    elif choice == '4':
                        self.show_history()
                    elif choice == '5':
                        self.show_variables()
                    elif choice == '6':
                        print("Thanks for playing!")
                        break
                    
                    input("\nPress Enter to continue...")
                
            except KeyboardInterrupt:
                print("\n\nGame interrupted. Save before quitting? (y/n): ", end="")
                if input().lower() == 'y':
                    self.save_game()
                break
            except Exception as e:
                print(f"\n{COLORS['red']}Error: {e}{COLORS['reset']}")
                import traceback
                traceback.print_exc()
                break
        
        print("\n\nGame Over!")
        print(f"Final variables: {json.dumps(self.state.variables, indent=2)}")

def main():
    parser = argparse.ArgumentParser(description="Play Ren'Py games in text mode")
    parser.add_argument("game_dir", help="Path to the game directory")
    parser.add_argument("--speed", type=float, default=0.02,
                        help="Typing speed (seconds per character)")
    parser.add_argument("--no-typing", action="store_true",
                        help="Disable typing animation")
    parser.add_argument("--debug", action="store_true",
                        help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Load the game
    try:
        game = RenpyGame(args.game_dir)
        print(f"Loaded game with {len(game.labels)} labels and {len(game.characters)} characters")
    except Exception as e:
        print(f"Error loading game: {e}")
        sys.exit(1)
    
    # Play the game
    typing_speed = 0 if args.no_typing else args.speed
    player = GamePlayer(game, typing_speed)
    
    try:
        player.play()
    except Exception as e:
        print(f"\nFatal error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
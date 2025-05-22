#!/usr/bin/env python3
"""
Direct Ren'Py to Twee converter with SugarCube syntax
"""

import re
import sys
from pathlib import Path


class RenpyToTweeConverter:
    def __init__(self):
        self.characters = {}
        self.variables = {}
        self.passages = {}
        self.current_label = None
        self.current_content = []
        
    def convert(self, script_content):
        """Main conversion method"""
        # Parse the script
        self.parse_script(script_content)
        
        # Generate Twee output
        return self.generate_twee()
    
    def parse_script(self, script_content):
        """Parse Ren'Py script into internal representation"""
        lines = script_content.strip().split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                i += 1
                continue
            
            # Character definition
            if stripped.startswith("define ") and "Character" in stripped:
                self.parse_character_definition(stripped)
            
            # Variable defaults
            elif stripped.startswith("default "):
                self.parse_default_variable(stripped)
            
            # Label
            elif stripped.startswith("label "):
                self.handle_label(stripped)
            
            # Jump
            elif stripped.startswith("jump "):
                target = stripped.split()[1]
                self.current_content.append(f"[[Continue|{target}]]")
            
            # Return
            elif stripped == "return":
                self.current_content.append("THE END")
            
            # Variable assignment
            elif stripped.startswith("$ "):
                self.parse_variable_assignment(stripped)
            
            # Menu
            elif stripped == "menu:":
                i = self.parse_menu(lines, i)
                continue
            
            # Skip audio/visual commands
            elif stripped.startswith("play ") or stripped.startswith("show ") or stripped.startswith("scene ") or stripped.startswith("hide ") or stripped.startswith("with ") or stripped.startswith("$ renpy."):
                pass  # Ignore visual/audio commands for now
            
            # Dialogue or narration
            elif '"' in stripped:
                self.parse_dialogue(stripped)
            
            # NVL clear (ignore for now)
            elif stripped == "nvl clear":
                pass
            
            i += 1
        
        # Save the last passage
        if self.current_label:
            self.save_current_passage()
    
    def parse_character_definition(self, line):
        """Parse character definitions"""
        # Try standard format first
        match = re.match(r'define\s+(\w+)\s*=\s*Character\s*\(\s*["\']([^"\']+)["\']', line)
        if match:
            char_id, char_name = match.groups()
            self.characters[char_id] = char_name
            return
        
        # Try format with _() translation function
        match = re.match(r'define\s+(\w+)\s*=\s*Character\s*\(\s*_\(["\']([^"\']+)["\']\)', line)
        if match:
            char_id, char_name = match.groups()
            self.characters[char_id] = char_name
            return
            
        # Try format with None or other complex definitions
        match = re.match(r'define\s+(\w+)\s*=\s*Character\s*\([^)]+\)', line)
        if match:
            char_id = match.group(1)
            # Set some sensible defaults for common character IDs
            if char_id == "pc":
                self.characters[char_id] = "Slim"
            elif char_id == "t":
                self.characters[char_id] = "Terminal"
            elif char_id == "narrator":
                pass  # Don't add narrator to characters dict
            else:
                self.characters[char_id] = char_id.title()  # Use capitalized ID as name
    
    def parse_default_variable(self, line):
        """Parse default variable declarations"""
        match = re.match(r'default\s+(\w+)\s*=\s*(.+)', line)
        if match:
            var_name, var_value_with_comment = match.groups()
            # Remove comments from the value
            var_value = var_value_with_comment.split('#')[0].strip()
            self.variables[var_name] = var_value
    
    def handle_label(self, line):
        """Handle label declarations"""
        # Save previous passage
        if self.current_label:
            self.save_current_passage()
        
        # Start new passage
        label = line.split()[1].rstrip(":")
        self.current_label = label
        self.current_content = []
    
    def save_current_passage(self):
        """Save the current passage content"""
        if self.current_label:
            self.passages[self.current_label] = list(self.current_content)
    
    def parse_variable_assignment(self, line):
        """Parse variable assignments"""
        assignment = line[2:].strip()  # Remove "$ "
        
        # Handle += and -= operators
        if "+=" in assignment:
            var, value = assignment.split("+=")
            var = var.strip()
            value = value.strip()
            self.current_content.append(f"<<set ${var} to ${var} + {value}>>")
        elif "-=" in assignment:
            var, value = assignment.split("-=")
            var = var.strip()
            value = value.strip()
            self.current_content.append(f"<<set ${var} to ${var} - {value}>>")
        elif "=" in assignment:
            var, value = assignment.split("=", 1)
            var = var.strip()
            value = value.strip()
            self.current_content.append(f"<<set ${var} to {value}>>")
    
    def parse_dialogue(self, line):
        """Parse dialogue lines"""
        # Check for character dialogue
        for char_id, char_name in self.characters.items():
            if line.strip().startswith(char_id + " "):
                # Extract dialogue - handle escaped quotes
                # Use a simpler approach: find first and last quotes
                first_quote = line.find('"')
                last_quote = line.rfind('"')
                if first_quote != -1 and last_quote != -1 and first_quote < last_quote:
                    dialogue = line[first_quote + 1:last_quote]
                    # Handle escaped quotes if present
                    dialogue = dialogue.replace('\\"', '"')
                    self.current_content.append(f"{char_name}: {dialogue}")
                    return
        
        # Check for undefined character dialogue
        words = line.strip().split(None, 1)
        if len(words) == 2 and words[1].startswith('"'):
            char_id = words[0]
            # Extract dialogue
            first_quote = words[1].find('"')
            last_quote = words[1].rfind('"')
            if first_quote != -1 and last_quote != -1 and first_quote < last_quote:
                dialogue = words[1][first_quote + 1:last_quote]
                dialogue = dialogue.replace('\\"', '"')
                self.current_content.append(f"{char_id}: {dialogue}")
                return
        
        # Narrator text
        first_quote = line.find('"')
        last_quote = line.rfind('"')
        if first_quote != -1 and last_quote != -1 and first_quote < last_quote:
            dialogue = line[first_quote + 1:last_quote]
            dialogue = dialogue.replace('\\"', '"')
            self.current_content.append(dialogue)
    
    def parse_menu(self, lines, start_idx):
        """Parse menu block"""
        i = start_idx + 1
        
        # Check for menu prompt
        if i < len(lines) and lines[i].strip().startswith('"') and lines[i].strip().endswith('"'):
            prompt = lines[i].strip()[1:-1]
            self.current_content.append(prompt)
            i += 1
        
        # Parse choices
        while i < len(lines):
            line = lines[i].strip()
            
            # End of menu - check for label or other non-menu content
            if line and not line.startswith('"') and not line.startswith(' ') and not line.startswith('\t'):
                # But don't break on empty lines within menu
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('"'):
                    i += 1
                    continue
                break
            
            # Choice with condition
            match = re.match(r'"([^"]+)"\s+if\s+(.+):', line)
            if match:
                choice_text, condition = match.groups()
                # Convert condition
                condition = self.convert_condition(condition)
                self.current_content.append(f"<<if {condition}>>")
                
                # Find target
                target = self.find_menu_target(lines, i)
                # Check if there are effects
                effects = self.find_menu_effects(lines, i)
                
                if effects:
                    self.current_content.append(f'<<link "{choice_text}" "{target}">>')
                    self.current_content.extend(effects)
                    self.current_content.append('<</link>>')
                else:
                    self.current_content.append(f"[[{choice_text}|{target}]]")
                
                self.current_content.append("<</if>>")
                i = self.skip_menu_block(lines, i)
                continue
            
            # Simple choice
            match = re.match(r'"([^"]+)":', line)
            if match:
                choice_text = match.group(1)
                target = self.find_menu_target(lines, i)
                effects = self.find_menu_effects(lines, i)
                
                if effects:
                    self.current_content.append(f'<<link "{choice_text}" "{target}">>')
                    self.current_content.extend(effects)
                    self.current_content.append('<</link>>')
                else:
                    self.current_content.append(f"[[{choice_text}|{target}]]")
                
                i = self.skip_menu_block(lines, i)
                continue
            
            i += 1
        
        return i - 1
    
    def find_menu_target(self, lines, choice_idx):
        """Find the jump target for a menu choice"""
        i = choice_idx + 1
        while i < len(lines) and lines[i].startswith("    "):
            if "jump " in lines[i]:
                return lines[i].strip().split()[1]
            i += 1
        return "next"
    
    def find_menu_effects(self, lines, choice_idx):
        """Find variable assignments in a menu choice"""
        effects = []
        i = choice_idx + 1
        # Track the indentation level to stay within this choice block
        choice_indent = len(lines[choice_idx]) - len(lines[choice_idx].lstrip())
        
        while i < len(lines):
            if not lines[i].strip():  # Empty line
                i += 1
                continue
            
            current_indent = len(lines[i]) - len(lines[i].lstrip())
            # If we're back to choice level or less, we've left this choice block
            if current_indent <= choice_indent:
                break
                
            stripped = lines[i].strip()
            if stripped.startswith("$ "):
                # Parse the assignment
                assignment = stripped[2:]
                if "+=" in assignment:
                    var, value = assignment.split("+=")
                    effects.append(f"<<set ${var.strip()} to ${var.strip()} + {value.strip()}>>")
                elif "-=" in assignment:
                    var, value = assignment.split("-=")
                    effects.append(f"<<set ${var.strip()} to ${var.strip()} - {value.strip()}>>")
                elif "=" in assignment:
                    var, value = assignment.split("=", 1)
                    effects.append(f"<<set ${var.strip()} to {value.strip()}>>")
            i += 1
        return effects
    
    def skip_menu_block(self, lines, choice_idx):
        """Skip to the end of a menu choice block"""
        i = choice_idx + 1
        # Skip lines that belong to this choice (more indented than the choice itself)
        choice_indent = len(lines[choice_idx]) - len(lines[choice_idx].lstrip())
        while i < len(lines):
            if not lines[i].strip():  # Empty line
                i += 1
                continue
            current_indent = len(lines[i]) - len(lines[i].lstrip())
            if current_indent <= choice_indent:
                break
            i += 1
        return i
    
    def convert_condition(self, condition):
        """Convert Ren'Py condition to SugarCube syntax"""
        # Add $ to variable names
        for var in self.variables:
            condition = re.sub(r'\b' + var + r'\b', f'${var}', condition)
        
        # Also check common variables that might not be declared
        common_vars = ['strength', 'karma', 'cos', 'cow', 'cod']
        for var in common_vars:
            if var in condition and f'${var}' not in condition:
                condition = re.sub(r'\b' + var + r'\b', f'${var}', condition)
        
        return condition
    
    def generate_twee(self):
        """Generate Twee output from parsed data"""
        output = []
        
        # Header
        output.append(":: StoryTitle")
        output.append("Link Loader Story")
        output.append("")
        
        # Story data
        output.append(":: StoryData")
        output.append("{")
        output.append('  "ifid": "D7C45122-7E3A-4B8F-9B52-7C5D4BBEB422",')
        output.append('  "format": "SugarCube",')
        output.append('  "format-version": "2.30.0",')
        output.append('  "start": "start"')
        output.append("}")
        output.append("")
        
        # StoryInit with variables
        if self.variables:
            output.append(":: StoryInit")
            for var, value in self.variables.items():
                output.append(f"<<set ${var} to {value}>>")
            output.append("")
        
        # Generate passages
        for label, content in self.passages.items():
            output.append(f":: {label}")
            output.extend(content)
            output.append("")
        
        return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python renpy_to_twee_v2.py <script.rpy> [output.tw]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.tw')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        script = f.read()
    
    converter = RenpyToTweeConverter()
    twee_content = converter.convert(script)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(twee_content)
    
    print(f"Converted {input_file} to {output_file}")


if __name__ == "__main__":
    main()
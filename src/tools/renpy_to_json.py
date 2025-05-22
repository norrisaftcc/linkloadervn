#!/usr/bin/env python3
"""
Convert Ren'Py script to JSON dialogue format
"""

import re
import json
import sys
from pathlib import Path


class RenpyToJsonConverter:
    def __init__(self):
        self.nodes = {}
        self.characters = {}
        self.variables = {}
        self.current_node_id = None
        self.node_counter = 0
        self.default_speaker = None
        self.start_label = "start"
        
    def get_node_id(self, label=None):
        """Generate a unique node ID"""
        if label:
            return label
        self.node_counter += 1
        return f"node_{self.node_counter}"
    
    def parse_character_define(self, line):
        """Parse character definitions"""
        # define pc = Character(_("Slim"), color="#c8ffc8")
        match = re.match(r'define\s+(\w+)\s*=\s*Character\s*\(\s*[_\(]*"([^"]+)"', line)
        if match:
            char_id, char_name = match.groups()
            self.characters[char_id] = char_name
            if char_id == "pc":
                self.default_speaker = char_name
    
    def parse_default_var(self, line):
        """Parse default variable declarations"""
        # default cos = 0
        match = re.match(r'default\s+(\w+)\s*=\s*(.+)', line)
        if match:
            var_name, var_value = match.groups()
            try:
                # Try to evaluate the value
                self.variables[var_name] = eval(var_value)
            except:
                self.variables[var_name] = var_value.strip()
    
    def parse_set_var(self, line):
        """Parse variable assignments"""
        # $ cos = 2
        match = re.match(r'\$\s*(\w+)\s*=\s*(.+)', line)
        if match:
            var_name, var_value = match.groups()
            return {
                "type": "set",
                "variable": var_name,
                "value": eval(var_value) if var_value.isdigit() else var_value.strip()
            }
        return None
    
    def parse_dialogue(self, line, speaker=None):
        """Parse dialogue lines"""
        # pc "Hello world"
        # "Narrator text"
        
        # Check for character dialogue
        for char_id, char_name in self.characters.items():
            if line.startswith(char_id + " "):
                quote_match = re.match(rf'{char_id}\s+"([^"]+)"', line)
                if quote_match:
                    return char_name, quote_match.group(1)
        
        # Check for narrator/unattributed dialogue
        quote_match = re.match(r'"([^"]+)"', line.strip())
        if quote_match:
            return None, quote_match.group(1)  # No speaker for narrator text
        
        # Check for robot dialogue (character name directly)
        match = re.match(r'(\w+)\s+"([^"]+)"', line)
        if match:
            char_name, dialogue = match.groups()
            # Convert character variable names to proper names
            if char_name == "cargo_bot":
                return "Cargo Bot", dialogue
            elif char_name == "rustler":
                return "???", dialogue
            elif char_name == "narrator":
                return None, dialogue  # Narrator has no speaker name
            return char_name, dialogue
            
        return None, None
    
    def parse_menu_choice(self, lines, start_idx):
        """Parse menu choices"""
        choices = []
        i = start_idx + 1
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip the menu title
            if line.startswith('"') and lines[i-1].strip() == "menu:":
                i += 1
                continue
            
            # Parse choice with condition
            match = re.match(r'"([^"]+)"\s+if\s+(.+):', line)
            if match:
                text, condition = match.groups()
                # Find what happens after this choice
                next_node = self.find_next_node(lines, i)
                choice = {
                    "text": text,
                    "condition": condition,
                    "next": next_node
                }
                
                # Check for effects in the choice block
                effects = []
                j = i + 1
                while j < len(lines) and lines[j].startswith("            "):
                    effect = self.parse_set_var(lines[j].strip())
                    if effect:
                        effects.append(effect)
                    j += 1
                
                if effects:
                    choice["effects"] = effects
                
                choices.append(choice)
            
            # Parse simple choice
            elif line.startswith('"') and line.endswith('":'):
                text = line[1:-2]
                next_node = self.find_next_node(lines, i)
                choice = {
                    "text": text,
                    "next": next_node
                }
                
                # Check for effects
                effects = []
                j = i + 1
                while j < len(lines) and lines[j].startswith("            "):
                    effect = self.parse_set_var(lines[j].strip())
                    if effect:
                        effects.append(effect)
                    j += 1
                
                if effects:
                    choice["effects"] = effects
                
                choices.append(choice)
            
            # Stop when we reach a label or dedent
            elif line.startswith("label ") or (line and not line.startswith(" ")):
                break
            
            i += 1
        
        return choices, i
    
    def find_next_node(self, lines, start_idx):
        """Find the next node after a choice or dialogue"""
        i = start_idx + 1
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Jump statement
            if line.startswith("jump "):
                return line.split()[1]
            
            # Label (new scene)
            if line.startswith("label "):
                return line.split()[1].rstrip(":")
            
            # Return statement (end)
            if line == "return":
                return None
            
            i += 1
        
        return None
    
    def convert_condition(self, condition):
        """Convert Ren'Py condition to our format"""
        # Simple conversion - this could be more sophisticated
        return condition.strip()
    
    def parse_script(self, script_content):
        """Parse the entire Ren'Py script"""
        lines = script_content.split('\n')
        i = 0
        
        current_label = None
        current_node = None
        
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            
            # Skip empty lines and comments
            if not stripped or stripped.startswith("#"):
                i += 1
                continue
            
            # Character definition
            if stripped.startswith("define ") and "Character" in stripped:
                self.parse_character_define(stripped)
            
            # Variable defaults
            elif stripped.startswith("default "):
                self.parse_default_var(stripped)
            
            # Label (new scene/node)
            elif stripped.startswith("label "):
                label_name = stripped.split()[1].rstrip(":")
                current_label = label_name
                
                # Create a new node
                node_id = self.get_node_id(label_name)
                current_node = {
                    "title": label_name.replace("_", " ").title(),
                    "content": "",
                    "next": None
                }
                
                # Check if this is the start node
                if label_name == "start":
                    current_node["tags"] = ["start"]
                
                self.nodes[node_id] = current_node
                self.current_node_id = node_id
            
            # Menu
            elif stripped == "menu:":
                if current_node:
                    choices, new_i = self.parse_menu_choice(lines, i)
                    if choices:
                        current_node["choices"] = choices
                        current_node.pop("next", None)  # Remove next if we have choices
                    i = new_i
                    continue
            
            # Jump statement
            elif stripped.startswith("jump "):
                target = stripped.split()[1]
                if current_node:
                    current_node["next"] = target
            
            # Variable assignment
            elif stripped.startswith("$ "):
                effect = self.parse_set_var(stripped)
                if effect and current_node:
                    if "onentry" not in current_node:
                        current_node["onentry"] = []
                    current_node["onentry"].append(effect)
            
            # Dialogue
            elif any(stripped.startswith(char + " ") for char in self.characters) or stripped.startswith('"'):
                speaker, dialogue = self.parse_dialogue(stripped)
                if dialogue and current_node:
                    # If we already have content, create a new node
                    if current_node["content"]:
                        # Create continuation node
                        next_node_id = self.get_node_id()
                        next_node = {
                            "title": f"Dialogue {self.node_counter}",
                            "content": dialogue,
                            "next": current_node.get("next")
                        }
                        
                        if speaker and speaker != self.default_speaker:
                            next_node["speaker"] = speaker
                        
                        # Link current to next
                        current_node["next"] = next_node_id
                        self.nodes[next_node_id] = next_node
                        current_node = next_node
                        self.current_node_id = next_node_id
                    else:
                        # First dialogue in this node
                        current_node["content"] = dialogue
                        if speaker and speaker != self.default_speaker:
                            current_node["speaker"] = speaker
            
            # Other character dialogue (like cargo_bot)
            elif re.match(r'(\w+)\s+"', stripped):
                speaker, dialogue = self.parse_dialogue(stripped)
                if dialogue and current_node:
                    # Create a new node for this dialogue
                    if current_node["content"]:
                        next_node_id = self.get_node_id()
                        next_node = {
                            "title": f"Dialogue {self.node_counter}",
                            "speaker": speaker,
                            "content": dialogue,
                            "next": current_node.get("next")
                        }
                        
                        current_node["next"] = next_node_id
                        self.nodes[next_node_id] = next_node
                        current_node = next_node
                        self.current_node_id = next_node_id
                    else:
                        current_node["content"] = dialogue
                        current_node["speaker"] = speaker
            
            i += 1
        
        return self.create_json_output()
    
    def create_json_output(self):
        """Create the final JSON structure"""
        return {
            "title": "Link Loader Episode 1",
            "author": "Converted from Ren'Py",
            "version": "1.0",
            "default_speaker": self.default_speaker or "Narrator",
            "variables": self.variables,
            "tags": ["converted", "renpy"],
            "start": self.start_label,
            "nodes": self.nodes
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python renpy_to_json.py <script.rpy> [output.json]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_suffix('.json')
    
    # Read Ren'Py script
    with open(input_file, 'r', encoding='utf-8') as f:
        script_content = f.read()
    
    # Convert to JSON
    converter = RenpyToJsonConverter()
    json_data = converter.parse_script(script_content)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)
    
    print(f"Converted {input_file} to {output_file}")
    print(f"Total nodes: {len(json_data['nodes'])}")
    print(f"Variables: {list(json_data['variables'].keys())}")


if __name__ == "__main__":
    main()
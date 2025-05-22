#!/usr/bin/env python3
"""
Direct Ren'Py to Twee converter (bypassing JSON)
"""

import re
import sys
from pathlib import Path


class RenpyToTweeConverter:
    def __init__(self):
        self.passages = []
        self.characters = {}
        self.variables = {}
        self.current_passage = None
        
    def convert_to_twee(self, script_content):
        """Convert Ren'Py script directly to Twee"""
        # Start with Twee headers
        twee = [":: StoryTitle", "Link Loader Story", "", 
                ":: StoryData", 
                '{\n  "ifid": "D7C45122-7E3A-4B8F-9B52-7C5D4BBEB422",\n  "format": "SugarCube",\n  "format-version": "2.30.0",\n  "start": "Start"\n}', 
                ""]
        
        # Add story init
        twee.append(":: StoryInit")
        twee.append("<<set $name to 'Slim'>>")
        
        # Process the script
        lines = script_content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Character definition
            if line.startswith("define ") and "Character" in line:
                match = re.match(r'define\s+(\w+)\s*=\s*Character\s*\(["\']([^"\']+)', line)
                if match:
                    char_id, char_name = match.groups()
                    self.characters[char_id] = char_name
            
            # Variable defaults
            elif line.startswith("default "):
                match = re.match(r'default\s+(\w+)\s*=\s*(.+)', line)
                if match:
                    var_name, var_value = match.groups()
                    twee.append(f"<<set ${var_name} to {var_value}>>")
            
            # Label (new passage)
            elif line.startswith("label "):
                label = line.split()[1].rstrip(":")
                passage_name = "Start" if label == "start" else label
                twee.append("")
                twee.append(f":: {passage_name}")
                self.current_passage = []
            
            # Menu
            elif line == "menu:":
                # Get menu prompt if exists
                if i + 1 < len(lines) and lines[i + 1].strip().startswith('"'):
                    prompt = lines[i + 1].strip()[1:-1]
                    self.current_passage.append(prompt)
                    i += 1
                
                # Process choices
                i += 1
                while i < len(lines) and lines[i].strip():
                    choice_line = lines[i].strip()
                    if choice_line.startswith('"') and choice_line.endswith('":'):
                        choice_text = choice_line[1:-2]
                        # Find target
                        j = i + 1
                        target = None
                        while j < len(lines) and lines[j].startswith("        "):
                            if "jump " in lines[j]:
                                target = lines[j].strip().split()[1]
                                break
                            elif "return" in lines[j].strip():
                                target = None
                                break
                            j += 1
                        
                        if target:
                            self.current_passage.append(f"[[{choice_text}|{target}]]")
                        else:
                            self.current_passage.append(f"[[{choice_text}|End]]")
                        
                        # Skip to next choice
                        i = j
                    i += 1
                i -= 1
            
            # Variable assignment
            elif line.startswith("$ "):
                var_line = line[2:].strip()
                match = re.match(r'(\w+)\s*=\s*(.+)', var_line)
                if match:
                    var, val = match.groups()
                    self.current_passage.append(f"<<set ${var} to {val}>>")
            
            # Jump
            elif line.startswith("jump "):
                target = line.split()[1]
                self.current_passage.append(f"[[Continue|{target}]]")
            
            # Return (end)
            elif line == "return":
                self.current_passage.append("THE END")
            
            # Dialogue
            elif any(line.startswith(char + " ") for char in self.characters):
                for char_id, char_name in self.characters.items():
                    if line.startswith(char_id + " "):
                        dialogue = line[len(char_id):].strip().strip('"')
                        self.current_passage.append(f"{char_name}: {dialogue}")
                        break
            
            # If we have a current passage, add content to twee
            if self.current_passage is not None and i > 0 and (
                i + 1 >= len(lines) or 
                lines[i + 1].strip().startswith("label ") or
                not lines[i + 1].strip()
            ):
                twee.extend(self.current_passage)
                self.current_passage = None
            
            i += 1
        
        # Add final End passage
        twee.extend(["", ":: End", "Thanks for playing!"])
        
        return "\n".join(twee)


def main():
    if len(sys.argv) < 2:
        print("Usage: python renpy_to_twee.py <script.rpy> [output.tw]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.tw')
    
    with open(input_file, 'r', encoding='utf-8') as f:
        script = f.read()
    
    converter = RenpyToTweeConverter()
    twee_content = converter.convert_to_twee(script)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(twee_content)
    
    print(f"Converted {input_file} to {output_file}")


if __name__ == "__main__":
    main()
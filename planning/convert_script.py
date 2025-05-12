#!/usr/bin/env python3
"""
Script Conversion Tool for Link Loader

This script converts between different script formats:
- JSON to Ren'Py
- Ren'Py to JSON
- JSON to Markdown
"""

import os
import json
import re
import argparse
import sys
from collections import defaultdict

def json_to_renpy(json_data, output_path=None):
    """Convert JSON script data to Ren'Py script format"""
    lines = []
    
    # Add header
    lines.append(f"# {json_data['title']}")
    lines.append(f"# Generated from JSON script data v{json_data['version']}")
    lines.append("")
    
    # Define characters
    lines.append("# Define the characters")
    for char_id, char in json_data.get('characters', {}).items():
        if char_id == "narrator":
            lines.append(f"define {char_id} = Character(None, kind=nvl) # {char.get('description', '')}")
        else:
            lines.append(f"define {char_id} = Character(_('{char['name']}'), color='{char['color']}') # {char.get('description', '')}")
    lines.append("")
    
    # Initialize stats
    lines.append("# Initialize variables for stats")
    for stat_id, stat in json_data.get('stats', {}).items():
        lines.append(f"default {stat_id} = {stat['default']} # {stat['name']}")
    lines.append("")
    
    # Game state variables
    if json_data.get('variables'):
        lines.append("# Game state variables")
        for var_id, var in json_data.get('variables', {}).items():
            if isinstance(var['default'], str):
                lines.append(f"default {var_id} = \"{var['default']}\" # {var['description']}")
            else:
                lines.append(f"default {var_id} = {var['default']} # {var['description']}")
        lines.append("")
    
    # Process each scene
    for scene in json_data.get('scenes', []):
        # Scene header
        lines.append(f"# {scene['title']}")
        lines.append(f"label {scene['id']}:")
        lines.append("    ")
        
        # Scene setup if available
        if scene.get('background'):
            lines.append(f"    # Set up the scene")
            lines.append(f"    scene {scene['background']}")
            lines.append(f"    with fade")
            lines.append("    ")
        
        # Music and ambient
        if scene.get('music') or scene.get('ambience'):
            lines.append(f"    # Play background music and ambient sounds")
            if scene.get('music'):
                lines.append(f"    $ renpy.music.set_volume(0.5)")
                lines.append(f"    play music \"{scene['music']}\"")
            if scene.get('ambience'):
                lines.append(f"    play audio \"{scene['ambience']}\"")
            lines.append("    ")
        
        # Process dialogue entries
        for entry in scene.get('dialogue', []):
            if entry['type'] == 'dialogue':
                char = entry['character']
                text = entry['text'].replace('"', '\\"')  # Escape quotes
                
                # Add display instruction if emotion is specified
                if entry.get('emotion'):
                    pos_str = ""
                    if entry.get('position'):
                        pos_str = f" at {entry['position']}"
                    
                    effect_str = ""
                    if entry.get('effect'):
                        effect_str = f" with {entry['effect']}"
                    
                    lines.append(f"    show {char} {entry['emotion']}{pos_str}{effect_str}")
                
                lines.append(f"    {char} \"{text}\"")
                lines.append("    ")
            
            elif entry['type'] == 'narration':
                text = entry['text'].replace('"', '\\"')
                lines.append(f"    \"{text}\"")
                lines.append("    ")
            
            elif entry['type'] == 'direction':
                lines.append(f"    # {entry['text']}")
                lines.append("    ")
            
            elif entry['type'] == 'sound':
                lines.append(f"    play audio \"{entry['file']}\"")
                lines.append("    ")
            
            elif entry['type'] == 'set':
                if isinstance(entry['value'], str):
                    lines.append(f"    $ {entry['variable']} = \"{entry['value']}\"")
                else:
                    lines.append(f"    $ {entry['variable']} = {entry['value']}")
                lines.append("    ")
            
            elif entry['type'] == 'condition':
                lines.append(f"    if {entry['condition']}:")
                
                # Add indented content
                if entry.get('text'):
                    text = entry['text'].replace('"', '\\"')
                    lines.append(f"        \"{text}\"")
                
                lines.append("    ")
            
            elif entry['type'] == 'choice':
                lines.append(f"    menu:")
                if entry.get('text'):
                    lines.append(f"        \"{entry['text']}\"")
                else:
                    lines.append(f"        \"What will you do?\"")
                lines.append("        ")
                
                for choice in entry.get('choices', []):
                    # Add condition if present
                    if choice.get('condition'):
                        lines.append(f"        \"{choice['text']}\" if {choice['condition']}:")
                    else:
                        lines.append(f"        \"{choice['text']}\":")
                    
                    # Add effects
                    if choice.get('effects'):
                        for effect in choice['effects']:
                            if effect['type'] == 'set':
                                if isinstance(effect['value'], str):
                                    lines.append(f"            $ {effect['variable']} = \"{effect['value']}\"")
                                else:
                                    lines.append(f"            $ {effect['variable']} = {effect['value']}")
                    
                    # Add jump target
                    lines.append(f"            jump {choice['target']}")
                    lines.append("            ")
                
                lines.append("    ")
            
            elif entry['type'] == 'jump':
                lines.append(f"    jump {entry['target']}")
                lines.append("    ")
        
        # Add a separator after each scene
        lines.append("")
    
    # End of script
    lines.append("    # Return to main menu")
    lines.append("    return")
    
    renpy_script = "\n".join(lines)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(renpy_script)
        print(f"Ren'Py script written to {output_path}")
    
    return renpy_script

def renpy_to_json(renpy_path, base_json_path=None, output_path=None):
    """Extract scene data from Ren'Py script and merge with base JSON if provided"""
    # Load base JSON if provided, or create template
    if base_json_path and os.path.exists(base_json_path):
        try:
            with open(base_json_path, 'r') as f:
                json_data = json.load(f)
                print(f"Loaded base JSON from {base_json_path}")
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {base_json_path}")
            return None
    else:
        # Create template
        json_data = {
            "title": "Link Loader",
            "version": "0.1",
            "characters": {},
            "stats": {},
            "variables": {},
            "scenes": []
        }
    
    try:
        with open(renpy_path, 'r') as f:
            renpy_script = f.read()
    except FileNotFoundError:
        print(f"Error: Ren'Py file not found: {renpy_path}")
        return None
    
    # Extract basic metadata
    title_match = re.search(r'^#\s+(.+)$', renpy_script, re.MULTILINE)
    if title_match:
        json_data['title'] = title_match.group(1)
    
    # Extract characters
    character_pattern = re.compile(r'define\s+(\w+)\s*=\s*Character\(\s*(?:_\()?\s*[\'"]([^\'"]+)[\'"](?:\))?\s*,\s*color=[\'"]([^\'"]+)[\'"](?:.*?#\s*(.+))?', re.MULTILINE | re.DOTALL)
    
    for match in character_pattern.finditer(renpy_script):
        char_id, name, color, description = match.groups()
        json_data['characters'][char_id] = {
            "name": name,
            "color": color,
            "description": description.strip() if description else ""
        }
    
    # Extract stats and variables
    stat_pattern = re.compile(r'default\s+(\w+)\s*=\s*([^#]+)(?:#\s*(.+))?', re.MULTILINE)
    
    for match in stat_pattern.finditer(renpy_script):
        var_id, value, description = match.groups()
        value = value.strip()
        
        # Try to parse the value
        try:
            if value.startswith('"') and value.endswith('"'):
                # String
                parsed_value = value[1:-1]
            elif value.lower() in ('true', 'false'):
                # Boolean
                parsed_value = value.lower() == 'true'
            else:
                # Number or other
                try:
                    parsed_value = int(value)
                except ValueError:
                    try:
                        parsed_value = float(value)
                    except ValueError:
                        parsed_value = value
        except:
            parsed_value = value
        
        # Decide if this is a stat or other variable
        if var_id in ('cos', 'cow', 'cod'):
            json_data['stats'][var_id] = {
                "name": description.strip() if description else var_id.capitalize(),
                "description": description.strip() if description else "",
                "default": parsed_value
            }
        else:
            json_data['variables'][var_id] = {
                "name": description.strip() if description else var_id.capitalize(),
                "description": description.strip() if description else "",
                "default": parsed_value
            }
    
    # Extract scenes and dialogue
    scenes = []
    current_scene = None
    current_dialogue = []
    
    # Split the script into lines
    lines = renpy_script.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines
        if not line:
            i += 1
            continue
        
        # Check for scene labels
        label_match = re.match(r'label\s+(\w+):', line)
        if label_match:
            # Save previous scene if exists
            if current_scene:
                current_scene['dialogue'] = current_dialogue
                scenes.append(current_scene)
            
            # Start new scene
            scene_id = label_match.group(1)
            title = scene_id.replace('_', ' ').title()
            
            # Look for a comment with the real title
            if i > 0 and lines[i-1].strip().startswith('#'):
                title = lines[i-1].strip()[1:].strip()
            
            current_scene = {
                'id': scene_id,
                'title': title,
                'dialogue': []
            }
            current_dialogue = []
            i += 1
            continue
        
        # Check for scene background
        if line.startswith('scene ') and current_scene:
            parts = line.split()
            if len(parts) > 1:
                current_scene['background'] = ' '.join(parts[1:]).replace('with fade', '').strip()
            i += 1
            continue
        
        # Check for music
        if line.startswith('play music ') and current_scene:
            parts = line.split('"')
            if len(parts) > 1:
                current_scene['music'] = parts[1]
            i += 1
            continue
        
        # Check for ambient sounds
        if line.startswith('play audio ') and current_scene:
            parts = line.split('"')
            if len(parts) > 1:
                # Don't overwrite background ambience
                if 'ambience' not in current_scene:
                    current_scene['ambience'] = parts[1]
                else:
                    # Add as a sound effect
                    current_dialogue.append({
                        'type': 'sound',
                        'file': parts[1]
                    })
            i += 1
            continue
        
        # Check for character dialogue
        if ' "' in line and not line.startswith('#') and not line.startswith('menu:') and current_scene:
            # Check for character sprite changes
            character = None
            emotion = None
            position = None
            
            # Look back for show statements
            j = i - 1
            while j >= 0 and j > i - 5:  # Look back up to 5 lines
                prev_line = lines[j].strip()
                if prev_line.startswith('show '):
                    # Parse show statement
                    show_parts = prev_line.split()
                    if len(show_parts) > 2:
                        character = show_parts[1]
                        emotion = show_parts[2]
                        
                        # Check for position
                        if ' at ' in prev_line:
                            position = prev_line.split(' at ')[1].split()[0]
                    break
                j -= 1
            
            # Parse dialogue line
            parts = line.split(' "', 1)
            speaker = parts[0].strip()
            text = parts[1].rstrip('"')
            
            # Add to dialogue
            if speaker in json_data['characters']:
                current_dialogue.append({
                    'type': 'dialogue',
                    'character': speaker,
                    'text': text,
                    'emotion': emotion,
                    'position': position
                })
            else:
                # Narration
                current_dialogue.append({
                    'type': 'narration',
                    'text': text
                })
            
            i += 1
            continue
        
        # Check for menu choices
        if line.startswith('menu:'):
            choice_entry = {
                'type': 'choice',
                'choices': []
            }
            
            # Check for menu text
            i += 1
            if i < len(lines) and '"' in lines[i]:
                choice_entry['text'] = lines[i].strip().strip('"')
                i += 1
            
            # Parse choices
            while i < len(lines):
                choice_line = lines[i].strip()
                
                # End of choices
                if not choice_line or not choice_line.startswith('"'):
                    break
                
                # Parse choice
                parts = choice_line.split('"')
                choice_text = parts[1]
                
                # Check for condition
                condition = None
                if ' if ' in choice_line:
                    condition_part = choice_line.split(' if ')[1].strip(':')
                    condition = condition_part
                
                # Create choice object
                choice = {
                    'text': choice_text,
                    'effects': [],
                    'target': None
                }
                
                if condition:
                    choice['condition'] = condition
                
                # Look for effects and jump
                i += 1
                while i < len(lines):
                    effect_line = lines[i].strip()
                    
                    # End of this choice
                    if not effect_line or not effect_line.startswith('$') and not effect_line.startswith('jump'):
                        break
                    
                    # Parse effect
                    if effect_line.startswith('$'):
                        # Variable assignment
                        var_parts = effect_line[1:].strip().split('=')
                        var_name = var_parts[0].strip()
                        var_value = var_parts[1].strip()
                        
                        # Try to parse value
                        try:
                            if var_value.startswith('"') and var_value.endswith('"'):
                                parsed_value = var_value[1:-1]
                            elif var_value.lower() in ('true', 'false'):
                                parsed_value = var_value.lower() == 'true'
                            else:
                                try:
                                    parsed_value = int(var_value)
                                except ValueError:
                                    try:
                                        parsed_value = float(var_value)
                                    except ValueError:
                                        parsed_value = var_value
                        except:
                            parsed_value = var_value
                        
                        choice['effects'].append({
                            'type': 'set',
                            'variable': var_name,
                            'value': parsed_value
                        })
                    
                    elif effect_line.startswith('jump'):
                        # Jump target
                        target = effect_line.split()[1]
                        choice['target'] = target
                    
                    i += 1
                
                # Add choice to choices list
                choice_entry['choices'].append(choice)
                
                # End of choice parsing
                continue
            
            # Add choices to dialogue
            current_dialogue.append(choice_entry)
            continue
        
        # Check for jumps
        if line.startswith('jump ') and current_scene:
            target = line.split()[1]
            current_dialogue.append({
                'type': 'jump',
                'target': target
            })
            i += 1
            continue
        
        # Check for conditionals
        if line.startswith('if ') and current_scene:
            condition = line[3:].rstrip(':')
            
            condition_entry = {
                'type': 'condition',
                'condition': condition
            }
            
            # Look for text inside condition
            i += 1
            if i < len(lines) and '"' in lines[i]:
                text_line = lines[i].strip()
                if text_line.startswith('"'):
                    condition_entry['text'] = text_line.strip('"')
            
            current_dialogue.append(condition_entry)
            continue
        
        # Check for comments (directions)
        if line.startswith('#') and current_scene:
            text = line[1:].strip()
            current_dialogue.append({
                'type': 'direction',
                'text': text
            })
            i += 1
            continue
        
        # Move to next line if nothing matched
        i += 1
    
    # Add the last scene
    if current_scene:
        current_scene['dialogue'] = current_dialogue
        scenes.append(current_scene)
    
    # Update scenes in JSON data
    json_data['scenes'] = scenes
    
    # Write to output file if specified
    if output_path:
        with open(output_path, 'w') as f:
            json.dump(json_data, f, indent=2)
        print(f"JSON data written to {output_path}")
    
    return json_data

def json_to_markdown(json_data, output_path=None):
    """Convert JSON script data to Markdown format"""
    lines = []
    
    # Add header
    lines.append(f"# {json_data['title']}")
    lines.append("")
    
    # Add game overview section
    lines.append("## Game World Overview")
    lines.append("")
    lines.append("Link Loader takes place on the desert planet Syntax-4, a remote outpost where cargo trains transport essential supplies between settlements. These trains run on \"Link Loaders\" - sophisticated machinery that connects cargo cars using LISP-inspired programming logic.")
    lines.append("")
    lines.append("The protagonist is a troubleshooter sent to fix broken link loaders when their programming goes awry. The planet is populated mainly by robots that communicate using a LISP-like language, where parentheses are pronounced as \"sh\" sounds. Human presence is rare, making the protagonist something of an oddity.")
    lines.append("")
    
    # Add characters section
    lines.append("## Characters")
    lines.append("")
    for char_id, char in json_data.get('characters', {}).items():
        if char_id != 'narrator':
            lines.append(f"- **{char['name']}** - {char.get('description', '')}")
    lines.append("")
    
    # Add stats section
    lines.append("## Stats")
    lines.append("")
    lines.append("Character has three main stats that affect dialogue options and problem-solving approaches:")
    for stat_id, stat in json_data.get('stats', {}).items():
        lines.append(f"- **{stat['name']} ({stat_id.upper()})** - {stat['description']}")
    lines.append("")
    
    # Add character creation section if defined
    start_scene = next((scene for scene in json_data.get('scenes', []) if scene['id'] == 'start'), None)
    if start_scene:
        lines.append("## Character Creation")
        lines.append("")
        lines.append("*This scene appears before the main game starts*")
        lines.append("")
        lines.append("*Background: Simple UI screen with character options*")
        lines.append("")
        
        # Find character creation dialogue
        for entry in start_scene.get('dialogue', []):
            if entry.get('type') == 'narration':
                lines.append(f"**Narrator**: \"{entry['text']}\"")
                lines.append("")
            
            if entry.get('type') == 'choice':
                lines.append("*Player selects one of three character backgrounds:*")
                lines.append("")
                
                for i, choice in enumerate(entry.get('choices', [])):
                    lines.append(f"{i+1}. **\"{choice['text']}\"**")
                    
                    # Find the stat effects
                    stat_effects = {}
                    for effect in choice.get('effects', []):
                        if effect.get('type') == 'set' and effect.get('variable') in json_data.get('stats', {}):
                            stat_effects[effect['variable']] = effect['value']
                    
                    # Add stat effects if found
                    if stat_effects:
                        stat_str = ", ".join([f"{stat.upper()} {'+' if val > 0 else ''}{val}" for stat, val in stat_effects.items()])
                        lines.append(f"   **Stats**: {stat_str}")
                    
                    # Look for the scene this jumps to
                    target_scene = next((scene for scene in json_data.get('scenes', []) if scene['id'] == choice.get('target')), None)
                    if target_scene:
                        # Find description narration
                        for target_entry in target_scene.get('dialogue', []):
                            if target_entry.get('type') == 'narration':
                                lines.append(f"   **Description**: \"{target_entry['text']}\"")
                                break
                    
                    lines.append("")
    
    # Process each scene
    for scene in json_data.get('scenes', []):
        # Skip start scene which was handled separately
        if scene['id'] == 'start':
            continue
        
        lines.append(f"## {scene['title']}")
        lines.append("")
        
        # Add background info
        if scene.get('background'):
            lines.append(f"*Background: {scene['background']}*")
        if scene.get('music'):
            lines.append(f"*Music: \"{scene['music']}\"*")
        if scene.get('ambience'):
            lines.append(f"*Ambient: \"{scene['ambience']}\"*")
        lines.append("")
        
        # Process dialogue entries
        for entry in scene.get('dialogue', []):
            if entry['type'] == 'direction':
                lines.append(f"*{entry['text']}*")
                lines.append("")
            
            elif entry['type'] == 'dialogue':
                char_id = entry['character']
                char_name = json_data.get('characters', {}).get(char_id, {}).get('name', char_id)
                
                if entry.get('emotion'):
                    lines.append(f"*{char_name} {entry.get('emotion').replace('_', ' ')}*")
                    lines.append("")
                
                lines.append(f"**{char_name}**: \"{entry['text']}\"")
                lines.append("")
            
            elif entry['type'] == 'narration':
                lines.append(f"\"{entry['text']}\"")
                lines.append("")
            
            elif entry['type'] == 'condition':
                condition_var = entry['condition'].split()[0]
                condition_name = json_data.get('stats', {}).get(condition_var, {}).get('name', condition_var.upper())
                
                lines.append(f"*CHOICE BASED ON {condition_name}:*")
                lines.append("")
                
                if entry.get('text'):
                    lines.append(f"\"{entry['text']}\"")
                    lines.append("")
            
            elif entry['type'] == 'choice':
                if entry.get('text'):
                    lines.append(f"*CHOICE: {entry['text']}*")
                else:
                    lines.append("*CHOICE:*")
                lines.append("")
                
                for choice in entry.get('choices', []):
                    # Add condition if present
                    if choice.get('condition'):
                        condition_var = choice['condition'].split()[0]
                        condition_name = json_data.get('stats', {}).get(condition_var, {}).get('name', condition_var.upper())
                        lines.append(f"{choice['text']} (if {condition_name})")
                    else:
                        lines.append(f"{choice['text']}")
                    lines.append("")
            
            elif entry['type'] == 'jump':
                target_scene = next((scene for scene in json_data.get('scenes', []) if scene['id'] == entry.get('target')), None)
                if target_scene:
                    lines.append(f"*Continue to: {target_scene['title']}*")
                    lines.append("")
    
    # End of script
    lines.append("## End of Episode")
    lines.append("")
    lines.append("*Thanks for playing Link Loader!*")
    
    markdown_text = "\n".join(lines)
    
    if output_path:
        with open(output_path, 'w') as f:
            f.write(markdown_text)
        print(f"Markdown script written to {output_path}")
    
    return markdown_text

def main():
    parser = argparse.ArgumentParser(description="Convert Link Loader scripts between formats")
    parser.add_argument("--input", required=True, help="Path to input file")
    parser.add_argument("--output", required=True, help="Path to output file")
    parser.add_argument("--format", choices=["json2renpy", "renpy2json", "json2md"], required=True, 
                        help="Conversion format: json2renpy (JSON to Ren'Py), renpy2json (Ren'Py to JSON), json2md (JSON to Markdown)")
    parser.add_argument("--base", help="Path to base JSON file for renpy2json conversion (optional)")
    
    args = parser.parse_args()
    
    if args.format == "json2renpy":
        try:
            with open(args.input, 'r') as f:
                json_data = json.load(f)
            json_to_renpy(json_data, args.output)
            print(f"Successfully converted JSON to Ren'Py script: {args.output}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    elif args.format == "renpy2json":
        result = renpy_to_json(args.input, args.base, args.output)
        if result:
            print(f"Successfully converted Ren'Py to JSON: {args.output}")
        else:
            print("Conversion failed")
            sys.exit(1)
    
    elif args.format == "json2md":
        try:
            with open(args.input, 'r') as f:
                json_data = json.load(f)
            json_to_markdown(json_data, args.output)
            print(f"Successfully converted JSON to Markdown: {args.output}")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Script Validation Tool for Link Loader

This script validates the consistency between the JSON script data 
and the Ren'Py script files, ensuring they stay in sync.
"""

import os
import json
import re
import argparse
import sys
from collections import defaultdict

# Regular expressions for parsing Ren'Py files
LABEL_PATTERN = re.compile(r'label\s+(\w+):')
DEFINE_CHARACTER_PATTERN = re.compile(r'define\s+(\w+)\s*=\s*Character\(')
JUMP_PATTERN = re.compile(r'jump\s+(\w+)')
DEFAULT_PATTERN = re.compile(r'default\s+(\w+)\s*=')
MENU_PATTERN = re.compile(r'menu:')

class ScriptValidator:
    def __init__(self, json_path, renpy_paths):
        self.json_path = json_path
        self.renpy_paths = renpy_paths
        self.json_data = None
        self.renpy_data = {
            'labels': set(),
            'characters': set(),
            'jumps': [],  # List of (source_label, target_label)
            'variables': set(),
            'menus': []   # List of label names containing menus
        }
        self.issues = []

    def load_json_data(self):
        try:
            with open(self.json_path, 'r') as f:
                self.json_data = json.load(f)
            print(f"Loaded JSON data from {self.json_path}")
            return True
        except FileNotFoundError:
            self.issues.append(f"ERROR: JSON file not found: {self.json_path}")
            return False
        except json.JSONDecodeError as e:
            self.issues.append(f"ERROR: Invalid JSON in file {self.json_path}: {e}")
            return False

    def parse_renpy_files(self):
        for path in self.renpy_paths:
            if not os.path.exists(path):
                self.issues.append(f"WARNING: Ren'Py file not found: {path}")
                continue
                
            try:
                with open(path, 'r') as f:
                    content = f.read()
                
                # Extract labels, characters, jumps, variables, and menus
                current_label = None
                
                for line in content.split('\n'):
                    line = line.strip()
                    
                    # Check for labels
                    label_match = LABEL_PATTERN.search(line)
                    if label_match:
                        current_label = label_match.group(1)
                        self.renpy_data['labels'].add(current_label)
                        continue
                    
                    # Check for character definitions
                    char_match = DEFINE_CHARACTER_PATTERN.search(line)
                    if char_match:
                        self.renpy_data['characters'].add(char_match.group(1))
                        continue
                    
                    # Check for jumps
                    jump_match = JUMP_PATTERN.search(line)
                    if jump_match and current_label:
                        target = jump_match.group(1)
                        self.renpy_data['jumps'].append((current_label, target))
                        continue
                    
                    # Check for variables
                    default_match = DEFAULT_PATTERN.search(line)
                    if default_match:
                        self.renpy_data['variables'].add(default_match.group(1))
                        continue
                    
                    # Check for menus
                    menu_match = MENU_PATTERN.search(line)
                    if menu_match and current_label:
                        self.renpy_data['menus'].append(current_label)
                        
                print(f"Parsed Ren'Py file: {path}")
                
            except Exception as e:
                self.issues.append(f"ERROR: Failed to parse Ren'Py file {path}: {e}")

    def validate(self):
        # Load and parse files
        if not self.load_json_data():
            return False
        
        self.parse_renpy_files()
        
        # Validation checks
        self._validate_scenes()
        self._validate_characters()
        self._validate_variables()
        self._validate_jumps()
        self._validate_choices()
        
        return len([i for i in self.issues if i.startswith("ERROR")]) == 0

    def _validate_scenes(self):
        # Check if all scenes in JSON have corresponding labels in Ren'Py
        json_scenes = {scene['id'] for scene in self.json_data.get('scenes', [])}
        renpy_labels = self.renpy_data['labels']
        
        for scene_id in json_scenes:
            if scene_id not in renpy_labels:
                self.issues.append(f"ERROR: Scene '{scene_id}' defined in JSON but missing in Ren'Py scripts")
        
        # Check for Ren'Py labels not in JSON
        for label in renpy_labels:
            if label != 'start' and label not in json_scenes:
                self.issues.append(f"WARNING: Label '{label}' in Ren'Py scripts but not defined in JSON")

    def _validate_characters(self):
        # Check if all characters in JSON have corresponding definitions in Ren'Py
        json_characters = set(self.json_data.get('characters', {}).keys())
        renpy_characters = self.renpy_data['characters']
        
        for char_id in json_characters:
            if char_id not in renpy_characters:
                self.issues.append(f"ERROR: Character '{char_id}' defined in JSON but missing in Ren'Py scripts")
        
        # Check for Ren'Py characters not in JSON
        for char_id in renpy_characters:
            if char_id not in json_characters:
                self.issues.append(f"WARNING: Character '{char_id}' in Ren'Py scripts but not defined in JSON")

    def _validate_variables(self):
        # Check if all variables in JSON have corresponding defaults in Ren'Py
        json_variables = set(self.json_data.get('variables', {}).keys())
        json_stats = set(self.json_data.get('stats', {}).keys())
        all_json_vars = json_variables.union(json_stats)
        renpy_variables = self.renpy_data['variables']
        
        for var_id in all_json_vars:
            if var_id not in renpy_variables:
                self.issues.append(f"ERROR: Variable '{var_id}' defined in JSON but missing in Ren'Py scripts")
        
        # Check for Ren'Py variables not in JSON
        for var_id in renpy_variables:
            if var_id not in all_json_vars:
                self.issues.append(f"WARNING: Variable '{var_id}' in Ren'Py scripts but not defined in JSON")

    def _validate_jumps(self):
        # Check if all jumps in Ren'Py scripts have valid targets
        renpy_labels = self.renpy_data['labels']
        
        for source, target in self.renpy_data['jumps']:
            if target not in renpy_labels:
                self.issues.append(f"ERROR: Jump from '{source}' to non-existent label '{target}'")
        
        # Check if all scene transitions in JSON have valid targets
        json_scenes = {scene['id']: scene for scene in self.json_data.get('scenes', [])}
        
        for scene_id, scene in json_scenes.items():
            for entry in scene.get('dialogue', []):
                if entry.get('type') == 'jump' and 'target' in entry:
                    target = entry['target']
                    if target not in json_scenes:
                        self.issues.append(f"ERROR: In JSON, jump from '{scene_id}' to non-existent scene '{target}'")

    def _validate_choices(self):
        # Check if all scenes with choices in JSON have menus in Ren'Py
        json_scenes = {scene['id']: scene for scene in self.json_data.get('scenes', [])}
        renpy_menus = set(self.renpy_data['menus'])
        
        for scene_id, scene in json_scenes.items():
            has_choice = any(entry.get('type') == 'choice' for entry in scene.get('dialogue', []))
            if has_choice and scene_id not in renpy_menus:
                self.issues.append(f"WARNING: Scene '{scene_id}' has choices in JSON but no menu in Ren'Py scripts")
        
        # Check if all scenes with menus in Ren'Py have choices in JSON
        for menu_label in renpy_menus:
            if menu_label in json_scenes:
                scene = json_scenes[menu_label]
                has_choice = any(entry.get('type') == 'choice' for entry in scene.get('dialogue', []))
                if not has_choice:
                    self.issues.append(f"WARNING: Scene '{menu_label}' has menu in Ren'Py scripts but no choices in JSON")

    def print_report(self):
        if not self.issues:
            print("\n✅ No issues found! Scripts are consistent.")
            return True
        
        # Group issues by type
        error_count = 0
        warning_count = 0
        
        print("\n📝 Validation Report:")
        print("===================")
        
        for issue in self.issues:
            if issue.startswith("ERROR"):
                error_count += 1
                print(f"❌ {issue}")
            else:
                warning_count += 1
                print(f"⚠️ {issue}")
        
        print("\n📊 Summary:")
        print(f"  - {error_count} errors")
        print(f"  - {warning_count} warnings")
        
        return error_count == 0

def main():
    parser = argparse.ArgumentParser(description="Validate Link Loader script consistency")
    parser.add_argument("--json", default="/Users/norrisa/Documents/dev/github/linkloadervn/planning/script_data.json", 
                        help="Path to JSON script data file")
    parser.add_argument("--renpy", nargs="+", default=["/Users/norrisa/Documents/dev/github/linkloadervn/planning/playable_script.rpy"],
                        help="Paths to Ren'Py script files")
    parser.add_argument("--strict", action="store_true", 
                        help="Exit with error code if any issues are found (even warnings)")
    
    args = parser.parse_args()
    
    validator = ScriptValidator(args.json, args.renpy)
    success = validator.validate()
    report_success = validator.print_report()
    
    sys.exit(0 if success and (report_success or not args.strict) else 1)

if __name__ == "__main__":
    main()
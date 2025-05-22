import streamlit as st
import json
import os
import glob
import re
from datetime import datetime

# Set page config
st.set_page_config(
    page_title="Link Loader Script Editor",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# File paths
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
SCHEMA_PATH = os.path.join(SCRIPT_DIR, "script_schema.json")
DEFAULT_SCRIPT_PATH = os.path.join(SCRIPT_DIR, "script_data.json")

# Load schema
def load_schema():
    try:
        with open(SCHEMA_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Schema file not found at {SCHEMA_PATH}")
        return None
    except json.JSONDecodeError:
        st.error(f"Invalid JSON in schema file")
        return None

# Load script data
def load_script(path=DEFAULT_SCRIPT_PATH):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        # Return a template if file doesn't exist
        return {
            "title": "Link Loader Episode 1: Cargo Conundrum",
            "version": "0.1",
            "characters": {
                "pc": {
                    "name": "Slim",
                    "color": "#c8ffc8",
                    "description": "Cowboy Cosmonaut Coder Person"
                },
                "t": {
                    "name": "Terminal",
                    "color": "#c8c8ff",
                    "description": "Interface to the world's systems"
                },
                "clipi": {
                    "name": "Clipi",
                    "color": "#00ff00",
                    "description": "AI assistant"
                },
                "cargo_bot": {
                    "name": "Cargo Bot",
                    "color": "#aaaaaa",
                    "description": "Generic cargo robot"
                },
                "rustler": {
                    "name": "???",
                    "color": "#ff5555",
                    "description": "Mystery antagonist"
                },
                "narrator": {
                    "name": "Narrator",
                    "color": "#ffffff",
                    "description": "Narrator for non-dialogue text"
                }
            },
            "stats": {
                "cos": {
                    "name": "Cosmonaut",
                    "description": "Space/high-tech skills",
                    "default": 0
                },
                "cow": {
                    "name": "Cowboy",
                    "description": "Desert/low-tech skills",
                    "default": 0
                },
                "cod": {
                    "name": "Coder",
                    "description": "Robot communication/terminal skills",
                    "default": 0
                }
            },
            "variables": {
                "approach": {
                    "name": "Problem-solving Approach",
                    "description": "Tracks which approach the player took",
                    "default": "none"
                },
                "mission": {
                    "name": "Final Mission Choice",
                    "description": "Tracks the final mission choice",
                    "default": "none"
                }
            },
            "scenes": []
        }
    except json.JSONDecodeError:
        st.error(f"Invalid JSON in script file")
        return None

# Save script data
def save_script(data, path=DEFAULT_SCRIPT_PATH):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving script: {e}")
        return False

# Create backup
def backup_script(path=DEFAULT_SCRIPT_PATH):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{path}.{timestamp}.bak"
    try:
        with open(path, "r") as src:
            with open(backup_path, "w") as dst:
                dst.write(src.read())
        return True
    except Exception as e:
        st.error(f"Error creating backup: {e}")
        return False

# Convert script to Ren'Py format
def convert_to_renpy(script_data):
    renpy_script = []
    
    # Add header
    renpy_script.append(f"# {script_data['title']}")
    renpy_script.append("# Generated from script editor")
    renpy_script.append("")
    
    # Define characters
    renpy_script.append("# Define the characters")
    for char_id, char in script_data['characters'].items():
        if char_id == "narrator":
            renpy_script.append(f"define {char_id} = Character(None, kind=nvl) # {char['description']}")
        else:
            renpy_script.append(f"define {char_id} = Character(_('{char['name']}'), color='{char['color']}') # {char['description']}")
    renpy_script.append("")
    
    # Initialize variables for stats
    renpy_script.append("# Initialize variables for stats")
    for stat_id, stat in script_data['stats'].items():
        renpy_script.append(f"default {stat_id} = {stat['default']} # {stat['name']}")
    renpy_script.append("")
    
    # Game state variables
    if 'variables' in script_data:
        renpy_script.append("# Character approach variables")
        for var_id, var in script_data['variables'].items():
            if isinstance(var['default'], str):
                renpy_script.append(f"default {var_id} = '{var['default']}' # {var['description']}")
            else:
                renpy_script.append(f"default {var_id} = {var['default']} # {var['description']}")
        renpy_script.append("")
    
    # Process each scene
    for scene in script_data['scenes']:
        # Scene header
        renpy_script.append(f"# {scene['title']}")
        renpy_script.append(f"label {scene['id']}:")
        renpy_script.append("    ")
        
        # Scene setup if available
        if 'background' in scene:
            renpy_script.append(f"    # Set up the scene")
            renpy_script.append(f"    scene {scene['background']}")
            renpy_script.append(f"    with fade")
            renpy_script.append("    ")
        
        # Music and ambient
        if 'music' in scene or 'ambience' in scene:
            renpy_script.append(f"    # Play background music and ambient sounds")
            if 'music' in scene and scene['music']:
                renpy_script.append(f"    $ renpy.music.set_volume(0.5)")
                renpy_script.append(f"    play music \"{scene['music']}\"")
            if 'ambience' in scene and scene['ambience']:
                renpy_script.append(f"    play audio \"{scene['ambience']}\"")
            renpy_script.append("    ")
        
        # Process dialogue entries
        for entry in scene['dialogue']:
            if entry['type'] == 'dialogue':
                char = entry['character']
                text = entry['text'].replace('"', '\\"')  # Escape quotes
                
                # Add display instruction if emotion is specified
                if 'emotion' in entry and entry['emotion']:
                    pos_str = ""
                    if 'position' in entry and entry['position']:
                        pos_str = f" at {entry['position']}"
                    
                    effect_str = ""
                    if 'effect' in entry and entry['effect']:
                        effect_str = f" with {entry['effect']}"
                    
                    renpy_script.append(f"    show {char} {entry['emotion']}{pos_str}{effect_str}")
                
                renpy_script.append(f"    {char} \"{text}\"")
                renpy_script.append("    ")
            
            elif entry['type'] == 'narration':
                text = entry['text'].replace('"', '\\"')
                renpy_script.append(f"    \"{text}\"")
                renpy_script.append("    ")
            
            elif entry['type'] == 'direction':
                renpy_script.append(f"    # {entry['text']}")
                renpy_script.append("    ")
            
            elif entry['type'] == 'sound':
                renpy_script.append(f"    play audio \"{entry['file']}\"")
                renpy_script.append("    ")
            
            elif entry['type'] == 'set':
                renpy_script.append(f"    $ {entry['variable']} = {entry['value']}")
                renpy_script.append("    ")
            
            elif entry['type'] == 'condition':
                renpy_script.append(f"    if {entry['condition']}:")
                
                # Add indented content
                if 'text' in entry:
                    text = entry['text'].replace('"', '\\"')
                    renpy_script.append(f"        \"{text}\"")
                
                renpy_script.append("    ")
            
            elif entry['type'] == 'choice':
                renpy_script.append(f"    menu:")
                if 'text' in entry:
                    renpy_script.append(f"        \"{entry['text']}\"")
                else:
                    renpy_script.append(f"        \"What will you do?\"")
                renpy_script.append("        ")
                
                for choice in entry['choices']:
                    # Add condition if present
                    if 'condition' in choice and choice['condition']:
                        renpy_script.append(f"        \"{choice['text']}\" if {choice['condition']}:")
                    else:
                        renpy_script.append(f"        \"{choice['text']}\":")
                    
                    # Add effects
                    if 'effects' in choice:
                        for effect in choice['effects']:
                            if effect['type'] == 'set':
                                if isinstance(effect['value'], str):
                                    renpy_script.append(f"            $ {effect['variable']} = \"{effect['value']}\"")
                                else:
                                    renpy_script.append(f"            $ {effect['variable']} = {effect['value']}")
                    
                    # Add jump target
                    renpy_script.append(f"            jump {choice['target']}")
                    renpy_script.append("            ")
                
                renpy_script.append("    ")
            
            elif entry['type'] == 'jump':
                renpy_script.append(f"    jump {entry['target']}")
                renpy_script.append("    ")
        
        # Add a separator after each scene
        renpy_script.append("")
    
    # End of script
    renpy_script.append("    # Return to main menu")
    renpy_script.append("    return")
    
    return "\n".join(renpy_script)

# Function to extract scenes from Ren'Py script
def extract_scenes_from_renpy(renpy_script):
    scenes = []
    lines = renpy_script.strip().split('\n')
    
    current_scene = None
    current_dialogue = []
    label_pattern = re.compile(r'label\s+(\w+):')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for new scene (label)
        label_match = label_pattern.match(line)
        if label_match:
            # Save previous scene if exists
            if current_scene:
                current_scene['dialogue'] = current_dialogue
                scenes.append(current_scene)
                
            # Start new scene
            scene_id = label_match.group(1)
            current_scene = {
                'id': scene_id,
                'title': scene_id.replace('_', ' ').title(),
                'dialogue': []
            }
            current_dialogue = []
            continue
            
        # Check for scene settings
        if line.startswith('scene ') and current_scene:
            parts = line.split()
            if len(parts) > 1:
                current_scene['background'] = ' '.join(parts[1:]).replace('with fade', '').strip()
                
        # Check for music
        if line.startswith('play music ') and current_scene:
            parts = line.split('"')
            if len(parts) > 1:
                current_scene['music'] = parts[1]
                
        # Check for ambient sounds
        if line.startswith('play audio ') and current_scene:
            parts = line.split('"')
            if len(parts) > 1:
                current_scene['ambience'] = parts[1]
                
        # Process dialogue and other entries
        # This is simplified - a full parser would need more complex logic
        if '"' in line and ' "' in line and current_scene:
            parts = line.split(' "')
            character = parts[0].strip()
            text = parts[1].replace('"', '')
            
            current_dialogue.append({
                'type': 'dialogue',
                'character': character,
                'text': text
            })
            
    # Add the last scene
    if current_scene:
        current_scene['dialogue'] = current_dialogue
        scenes.append(current_scene)
        
    return scenes

# UI Components
def show_character_editor(script_data):
    st.header("Characters")
    
    # Display existing characters
    for char_id, char in script_data['characters'].items():
        with st.expander(f"{char['name']} ({char_id})"):
            new_name = st.text_input("Name", char['name'], key=f"char_name_{char_id}")
            new_color = st.color_picker("Dialogue Color", char['color'], key=f"char_color_{char_id}")
            new_desc = st.text_area("Description", char['description'], key=f"char_desc_{char_id}")
            
            # Update character if changed
            if new_name != char['name'] or new_color != char['color'] or new_desc != char['description']:
                script_data['characters'][char_id]['name'] = new_name
                script_data['characters'][char_id]['color'] = new_color
                script_data['characters'][char_id]['description'] = new_desc
                st.success(f"Updated character: {new_name}")
    
    # Add new character
    with st.expander("Add New Character"):
        new_id = st.text_input("Character ID (short code used in script)", key="new_char_id")
        new_name = st.text_input("Character Name", key="new_char_name")
        new_color = st.color_picker("Dialogue Color", "#ffffff", key="new_char_color")
        new_desc = st.text_area("Description", key="new_char_desc")
        
        if st.button("Add Character") and new_id and new_name:
            if new_id in script_data['characters']:
                st.error(f"Character ID {new_id} already exists")
            else:
                script_data['characters'][new_id] = {
                    "name": new_name,
                    "color": new_color,
                    "description": new_desc
                }
                st.success(f"Added character: {new_name}")
                # Clear the inputs
                st.experimental_rerun()

def show_stats_editor(script_data):
    st.header("Character Stats")
    
    # Display existing stats
    for stat_id, stat in script_data['stats'].items():
        with st.expander(f"{stat['name']} ({stat_id})"):
            new_name = st.text_input("Name", stat['name'], key=f"stat_name_{stat_id}")
            new_desc = st.text_area("Description", stat['description'], key=f"stat_desc_{stat_id}")
            new_default = st.number_input("Default Value", value=int(stat['default']), key=f"stat_default_{stat_id}")
            
            # Update stat if changed
            if new_name != stat['name'] or new_desc != stat['description'] or new_default != stat['default']:
                script_data['stats'][stat_id]['name'] = new_name
                script_data['stats'][stat_id]['description'] = new_desc
                script_data['stats'][stat_id]['default'] = new_default
                st.success(f"Updated stat: {new_name}")
    
    # Add new stat
    with st.expander("Add New Stat"):
        new_id = st.text_input("Stat ID (short code used in script)", key="new_stat_id")
        new_name = st.text_input("Stat Name", key="new_stat_name")
        new_desc = st.text_area("Description", key="new_stat_desc")
        new_default = st.number_input("Default Value", value=0, key="new_stat_default")
        
        if st.button("Add Stat") and new_id and new_name:
            if new_id in script_data['stats']:
                st.error(f"Stat ID {new_id} already exists")
            else:
                script_data['stats'][new_id] = {
                    "name": new_name,
                    "description": new_desc,
                    "default": new_default
                }
                st.success(f"Added stat: {new_name}")
                # Clear the inputs
                st.experimental_rerun()

def show_variables_editor(script_data):
    if 'variables' not in script_data:
        script_data['variables'] = {}
        
    st.header("Game Variables")
    
    # Display existing variables
    for var_id, var in script_data['variables'].items():
        with st.expander(f"{var['name']} ({var_id})"):
            new_name = st.text_input("Name", var['name'], key=f"var_name_{var_id}")
            new_desc = st.text_area("Description", var['description'], key=f"var_desc_{var_id}")
            
            # Determine type of default value
            if isinstance(var['default'], bool):
                new_default = st.checkbox("Default Value", var['default'], key=f"var_default_{var_id}")
            elif isinstance(var['default'], int):
                new_default = st.number_input("Default Value", value=var['default'], key=f"var_default_{var_id}")
            else:
                new_default = st.text_input("Default Value", var['default'], key=f"var_default_{var_id}")
            
            # Update variable if changed
            if new_name != var['name'] or new_desc != var['description'] or new_default != var['default']:
                script_data['variables'][var_id]['name'] = new_name
                script_data['variables'][var_id]['description'] = new_desc
                script_data['variables'][var_id]['default'] = new_default
                st.success(f"Updated variable: {new_name}")
    
    # Add new variable
    with st.expander("Add New Variable"):
        new_id = st.text_input("Variable ID (short code used in script)", key="new_var_id")
        new_name = st.text_input("Variable Name", key="new_var_name")
        new_desc = st.text_area("Description", key="new_var_desc")
        
        var_type = st.selectbox("Variable Type", ["String", "Number", "Boolean"], key="new_var_type")
        
        if var_type == "String":
            new_default = st.text_input("Default Value", key="new_var_default")
        elif var_type == "Number":
            new_default = st.number_input("Default Value", value=0, key="new_var_default")
        else:  # Boolean
            new_default = st.checkbox("Default Value", key="new_var_default")
        
        if st.button("Add Variable") and new_id and new_name:
            if new_id in script_data.get('variables', {}):
                st.error(f"Variable ID {new_id} already exists")
            else:
                if 'variables' not in script_data:
                    script_data['variables'] = {}
                    
                script_data['variables'][new_id] = {
                    "name": new_name,
                    "description": new_desc,
                    "default": new_default
                }
                st.success(f"Added variable: {new_name}")
                # Clear the inputs
                st.experimental_rerun()

def show_scenes_editor(script_data):
    st.header("Scenes")
    
    # Display scene list
    if 'scenes' not in script_data or not script_data['scenes']:
        st.warning("No scenes defined yet. Create your first scene below.")
        script_data['scenes'] = []
    
    # Scene overview
    scene_ids = [scene['id'] for scene in script_data['scenes']]
    scene_titles = [scene['title'] for scene in script_data['scenes']]
    
    # Create columns for the scene list
    cols = st.columns([3, 1, 1])
    with cols[0]:
        st.subheader("Scene Title")
    with cols[1]:
        st.subheader("Scene ID")
    with cols[2]:
        st.subheader("Actions")
    
    for i, (scene_id, scene_title) in enumerate(zip(scene_ids, scene_titles)):
        cols = st.columns([3, 1, 1])
        with cols[0]:
            st.write(scene_title)
        with cols[1]:
            st.write(scene_id)
        with cols[2]:
            edit_button = st.button("Edit", key=f"edit_{scene_id}")
            if edit_button:
                st.session_state.editing_scene = i
                st.experimental_rerun()
    
    # Add new scene button
    if st.button("Add New Scene"):
        st.session_state.adding_scene = True
        st.experimental_rerun()
    
    # Edit scene form
    if hasattr(st.session_state, 'editing_scene') and st.session_state.editing_scene is not None:
        scene_index = st.session_state.editing_scene
        scene = script_data['scenes'][scene_index]
        
        st.subheader(f"Editing Scene: {scene['title']}")
        with st.form(key=f"edit_scene_form_{scene_index}"):
            scene_title = st.text_input("Scene Title", scene['title'])
            scene_id = st.text_input("Scene ID", scene['id'])
            scene_bg = st.text_input("Background", scene.get('background', ''))
            scene_music = st.text_input("Music", scene.get('music', ''))
            scene_ambience = st.text_input("Ambient Sound", scene.get('ambience', ''))
            scene_desc = st.text_area("Scene Description", scene.get('description', ''))
            
            # Dialogue editor
            st.subheader("Dialogue")
            dialogue_editor = st.text_area("Edit dialogue (JSON format)", json.dumps(scene['dialogue'], indent=2), height=400)
            
            submit = st.form_submit_button("Save Scene")
            cancel = st.form_submit_button("Cancel")
            
            if submit:
                try:
                    dialogue_data = json.loads(dialogue_editor)
                    
                    # Update scene data
                    script_data['scenes'][scene_index]['title'] = scene_title
                    script_data['scenes'][scene_index]['id'] = scene_id
                    script_data['scenes'][scene_index]['background'] = scene_bg
                    script_data['scenes'][scene_index]['music'] = scene_music
                    script_data['scenes'][scene_index]['ambience'] = scene_ambience
                    script_data['scenes'][scene_index]['description'] = scene_desc
                    script_data['scenes'][scene_index]['dialogue'] = dialogue_data
                    
                    st.success("Scene updated successfully")
                    st.session_state.editing_scene = None
                    st.experimental_rerun()
                except json.JSONDecodeError:
                    st.error("Invalid JSON format in dialogue editor")
            
            if cancel:
                st.session_state.editing_scene = None
                st.experimental_rerun()
    
    # Add new scene form
    if hasattr(st.session_state, 'adding_scene') and st.session_state.adding_scene:
        st.subheader("Add New Scene")
        with st.form(key="add_scene_form"):
            scene_title = st.text_input("Scene Title")
            scene_id = st.text_input("Scene ID")
            scene_bg = st.text_input("Background")
            scene_music = st.text_input("Music")
            scene_ambience = st.text_input("Ambient Sound")
            scene_desc = st.text_area("Scene Description")
            
            default_dialogue = [
                {
                    "type": "direction",
                    "text": "Scene begins"
                },
                {
                    "type": "dialogue",
                    "character": "pc",
                    "text": "Add your dialogue here.",
                    "emotion": "neutral"
                }
            ]
            
            dialogue_editor = st.text_area("Initial dialogue (JSON format)", json.dumps(default_dialogue, indent=2), height=300)
            
            submit = st.form_submit_button("Add Scene")
            cancel = st.form_submit_button("Cancel")
            
            if submit and scene_title and scene_id:
                try:
                    dialogue_data = json.loads(dialogue_editor)
                    
                    # Create new scene
                    new_scene = {
                        "id": scene_id,
                        "title": scene_title,
                        "background": scene_bg,
                        "music": scene_music,
                        "ambience": scene_ambience,
                        "description": scene_desc,
                        "dialogue": dialogue_data
                    }
                    
                    script_data['scenes'].append(new_scene)
                    st.success("Scene added successfully")
                    st.session_state.adding_scene = False
                    st.experimental_rerun()
                except json.JSONDecodeError:
                    st.error("Invalid JSON format in dialogue editor")
            
            if cancel:
                st.session_state.adding_scene = False
                st.experimental_rerun()

def show_export_options(script_data):
    st.header("Export Options")
    
    # Convert to Ren'Py
    if st.button("Convert to Ren'Py Script"):
        renpy_script = convert_to_renpy(script_data)
        st.session_state.renpy_export = renpy_script
        st.success("Converted script to Ren'Py format")
    
    # Display Ren'Py export if available
    if hasattr(st.session_state, 'renpy_export'):
        st.subheader("Ren'Py Script")
        st.text_area("Copy this script to your Ren'Py project", st.session_state.renpy_export, height=400)
        
        export_path = st.text_input("Save to file (provide absolute path)", "/Users/norrisa/Documents/dev/github/linkloadervn/planning/generated_script.rpy")
        if st.button("Save Ren'Py Script") and export_path:
            try:
                with open(export_path, "w") as f:
                    f.write(st.session_state.renpy_export)
                st.success(f"Saved Ren'Py script to {export_path}")
            except Exception as e:
                st.error(f"Error saving script: {e}")

def show_import_options(script_data):
    st.header("Import Options")
    
    # Import from Ren'Py
    renpy_script = st.text_area("Paste Ren'Py Script", "", height=300)
    if st.button("Extract Scenes from Ren'Py") and renpy_script:
        scenes = extract_scenes_from_renpy(renpy_script)
        if scenes:
            # Confirm before replacing
            if st.checkbox("Replace existing scenes? This will overwrite your current scenes."):
                script_data['scenes'] = scenes
                st.success(f"Extracted {len(scenes)} scenes from Ren'Py script")
                st.experimental_rerun()
        else:
            st.error("Could not extract scenes from the provided script")

def validate_script(script_data):
    st.header("Script Validation")
    
    issues = []
    
    # Check for scene IDs
    scene_ids = [scene['id'] for scene in script_data.get('scenes', [])]
    duplicate_ids = set([x for x in scene_ids if scene_ids.count(x) > 1])
    if duplicate_ids:
        issues.append(f"Duplicate scene IDs found: {', '.join(duplicate_ids)}")
    
    # Check for jump targets
    for scene in script_data.get('scenes', []):
        for entry in scene.get('dialogue', []):
            if entry.get('type') == 'jump':
                target = entry.get('target')
                if target and target not in scene_ids:
                    issues.append(f"Jump target '{target}' in scene '{scene['id']}' does not exist")
            
            if entry.get('type') == 'choice':
                for choice in entry.get('choices', []):
                    target = choice.get('target')
                    if target and target not in scene_ids:
                        issues.append(f"Choice target '{target}' in scene '{scene['id']}' does not exist")
    
    # Check for character references
    character_ids = list(script_data.get('characters', {}).keys())
    for scene in script_data.get('scenes', []):
        for entry in scene.get('dialogue', []):
            if entry.get('type') == 'dialogue':
                char_id = entry.get('character')
                if char_id and char_id not in character_ids:
                    issues.append(f"Character '{char_id}' in scene '{scene['id']}' does not exist")
    
    # Check for variable references
    variable_ids = list(script_data.get('variables', {}).keys()) + list(script_data.get('stats', {}).keys())
    for scene in script_data.get('scenes', []):
        for entry in scene.get('dialogue', []):
            if entry.get('type') == 'set':
                var_id = entry.get('variable')
                if var_id and var_id not in variable_ids:
                    issues.append(f"Variable '{var_id}' in scene '{scene['id']}' does not exist")
            
            if entry.get('type') == 'choice':
                for choice in entry.get('choices', []):
                    for effect in choice.get('effects', []):
                        if effect.get('type') == 'set':
                            var_id = effect.get('variable')
                            if var_id and var_id not in variable_ids:
                                issues.append(f"Variable '{var_id}' in choice effect in scene '{scene['id']}' does not exist")
    
    # Display validation results
    if issues:
        st.error("Validation Issues Found")
        for issue in issues:
            st.warning(issue)
    else:
        st.success("Script validation passed! No issues found.")

# Main app functionality
def main():
    st.title("Link Loader Script Editor")
    
    # First-time setup
    if 'script_data' not in st.session_state:
        st.session_state.script_data = load_script()
        st.session_state.schema = load_schema()
    
    # Sidebar menu
    with st.sidebar:
        st.header("Link Loader Script Editor")
        menu = st.radio("Menu", [
            "Script Overview", 
            "Characters", 
            "Stats", 
            "Variables", 
            "Scenes",
            "Import/Export",
            "Validation"
        ])
        
        # Save button
        if st.button("💾 Save Script"):
            # Create backup before saving
            if os.path.exists(DEFAULT_SCRIPT_PATH):
                backup_script()
            
            if save_script(st.session_state.script_data):
                st.success("Script saved successfully!")
        
        # Load button
        if st.button("🔄 Reload Script"):
            st.session_state.script_data = load_script()
            st.success("Script reloaded!")
            st.experimental_rerun()
    
    # Main content based on menu selection
    if menu == "Script Overview":
        st.header("Script Overview")
        
        # Basic script metadata
        title = st.text_input("Script Title", st.session_state.script_data['title'])
        version = st.text_input("Version", st.session_state.script_data['version'])
        
        # Update metadata if changed
        if title != st.session_state.script_data['title'] or version != st.session_state.script_data['version']:
            st.session_state.script_data['title'] = title
            st.session_state.script_data['version'] = version
        
        # Display stats
        st.subheader("Script Statistics")
        stats = {
            "Characters": len(st.session_state.script_data.get('characters', {})),
            "Scenes": len(st.session_state.script_data.get('scenes', [])),
            "Dialogue Entries": sum(len(scene.get('dialogue', [])) for scene in st.session_state.script_data.get('scenes', []))
        }
        
        for label, value in stats.items():
            st.metric(label, value)
        
    elif menu == "Characters":
        show_character_editor(st.session_state.script_data)
        
    elif menu == "Stats":
        show_stats_editor(st.session_state.script_data)
        
    elif menu == "Variables":
        show_variables_editor(st.session_state.script_data)
        
    elif menu == "Scenes":
        show_scenes_editor(st.session_state.script_data)
        
    elif menu == "Import/Export":
        col1, col2 = st.columns(2)
        
        with col1:
            show_export_options(st.session_state.script_data)
            
        with col2:
            show_import_options(st.session_state.script_data)
            
    elif menu == "Validation":
        validate_script(st.session_state.script_data)

if __name__ == "__main__":
    main()
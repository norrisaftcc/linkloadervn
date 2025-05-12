#!/usr/bin/env python3
"""
Streamlit-based dialogue tree player for Link Loader

This script plays dialogue trees from JSON files in a web interface
built with Streamlit.
"""

import streamlit as st
import json
import os
import re
import time
import random
from typing import Dict, List, Any, Optional, Union

# Initialize session state
if "dialogue_data" not in st.session_state:
    st.session_state.dialogue_data = None
if "current_node_id" not in st.session_state:
    st.session_state.current_node_id = ""
if "variables" not in st.session_state:
    st.session_state.variables = {}
if "history" not in st.session_state:
    st.session_state.history = []
if "message_history" not in st.session_state:
    st.session_state.message_history = []
if "show_debug" not in st.session_state:
    st.session_state.show_debug = False
if "auto_advance" not in st.session_state:
    st.session_state.auto_advance = False
if "typing_speed" not in st.session_state:
    st.session_state.typing_speed = 30  # ms between characters

# Character color mapping
CHARACTER_COLORS = {
    "Slim": "#c8ffc8",
    "Clipi": "#00ff00",
    "Terminal": "#c8c8ff",
    "Cargo Bot": "#aaaaaa",
    "???": "#ff5555"
}


def load_dialogue(file_path: str) -> Dict:
    """Load dialogue data from a JSON file"""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Error: Dialogue file '{file_path}' not found.")
        return {}
    except json.JSONDecodeError as e:
        st.error(f"Error: Invalid JSON in dialogue file: {e}")
        return {}


def initialize_dialogue(dialogue_data: Dict) -> None:
    """Initialize the dialogue state"""
    st.session_state.dialogue_data = dialogue_data
    st.session_state.current_node_id = dialogue_data.get("start", "")
    st.session_state.variables = dialogue_data.get("variables", {}).copy()
    st.session_state.history = []
    st.session_state.message_history = []


def reset_dialogue() -> None:
    """Reset the dialogue to the beginning"""
    if st.session_state.dialogue_data:
        initialize_dialogue(st.session_state.dialogue_data)
        

def evaluate_condition(condition: str) -> bool:
    """Evaluate a condition based on the current variables"""
    if not condition:
        return True
        
    # Create a context with the current variables
    context = dict(st.session_state.variables)
    
    try:
        # Evaluate the condition in the context
        return eval(condition, {"__builtins__": {}}, context)
    except Exception as e:
        st.error(f"Error evaluating condition '{condition}': {e}")
        return False


def apply_effects(effects: List[Dict]) -> None:
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
            st.session_state.variables[variable] = value
        elif effect_type == "inc":
            st.session_state.variables[variable] = st.session_state.variables.get(variable, 0) + value
        elif effect_type == "dec":
            st.session_state.variables[variable] = st.session_state.variables.get(variable, 0) - value
        elif effect_type == "toggle":
            st.session_state.variables[variable] = not st.session_state.variables.get(variable, False)
        elif effect_type == "push":
            if variable not in st.session_state.variables:
                st.session_state.variables[variable] = []
            st.session_state.variables[variable].append(value)
        elif effect_type == "pop":
            if variable in st.session_state.variables and isinstance(st.session_state.variables[variable], list):
                if st.session_state.variables[variable]:
                    st.session_state.variables[variable].pop()
        elif effect_type == "script":
            script = effect.get("script", "")
            if script:
                try:
                    # Create a context with the current variables
                    context = dict(st.session_state.variables)
                    # Execute the script in the context
                    exec(script, {"__builtins__": {}}, context)
                    # Update the variables with the context
                    st.session_state.variables.update(context)
                except Exception as e:
                    st.error(f"Error executing script: {e}")


def format_robot_language(text: str) -> str:
    """Format robot language with CSS styling"""
    # Find text that looks like (Sh-something sh-something)
    robot_pattern = r'\(Sh-[^)]+\)'
    
    # Replace robot language with styled version
    def robot_replacer(match):
        robot_text = match.group(0)
        return f"<span style='color: #FFCC00; font-style: italic;'>{robot_text}</span>"
        
    return re.sub(robot_pattern, robot_replacer, text)


def get_current_node() -> Optional[Dict]:
    """Get the current dialogue node"""
    if not st.session_state.dialogue_data or not st.session_state.current_node_id:
        return None
        
    nodes = st.session_state.dialogue_data.get("nodes", {})
    if st.session_state.current_node_id not in nodes:
        st.error(f"Error: Node '{st.session_state.current_node_id}' not found in dialogue tree.")
        return None
        
    return nodes[st.session_state.current_node_id]


def advance_to_node(node_id: str) -> None:
    """Advance to a new node"""
    st.session_state.current_node_id = node_id
    
    # If the node is None, we've reached the end
    if node_id is None:
        return
        
    # Process the new node
    node = get_current_node()
    if not node:
        return
        
    # Apply onentry effects
    apply_effects(node.get("onentry", []))
    
    # Add to history
    st.session_state.history.append(node_id)
    
    # Get the speaker
    speaker = node.get("speaker", st.session_state.dialogue_data.get("default_speaker", None))
    
    # Get content
    content = node.get("content", "")
    if content:
        # Add to message history
        st.session_state.message_history.append({
            "speaker": speaker,
            "content": content,
            "emotion": node.get("emotion", ""),
            "position": node.get("position", ""),
            "node_id": node_id
        })
        
    # Auto-advance if no choices and auto-advance is enabled
    if st.session_state.auto_advance and "choices" not in node:
        next_node = node.get("next")
        if next_node:
            # Apply onexit effects
            apply_effects(node.get("onexit", []))
            advance_to_node(next_node)


def process_choice(choice: Dict) -> None:
    """Process a user choice"""
    # Apply choice effects
    apply_effects(choice.get("effects", []))
    
    # Apply onexit effects for the current node
    node = get_current_node()
    if node:
        apply_effects(node.get("onexit", []))
    
    # Move to the next node
    advance_to_node(choice.get("next"))


def render_message(message: Dict) -> None:
    """Render a dialogue message with styling"""
    speaker = message.get("speaker")
    content = message.get("content", "")
    
    # Apply styling based on speaker
    if speaker:
        color = CHARACTER_COLORS.get(speaker, "#ffffff")
        with st.container(border=True):
            st.markdown(f"<div style='color: {color}; font-weight: bold;'>{speaker}</div>", unsafe_allow_html=True)
            st.markdown(f"<div>{format_robot_language(content)}</div>", unsafe_allow_html=True)
    else:
        st.markdown(format_robot_language(content), unsafe_allow_html=True)


def render_choices(choices: List[Dict]) -> None:
    """Render the available choices as buttons"""
    # Filter choices based on conditions
    valid_choices = []
    for choice in choices:
        condition = choice.get("condition", "")
        if evaluate_condition(condition):
            valid_choices.append(choice)
    
    # Display choices as buttons
    if valid_choices:
        st.write("What will you do?")
        for choice in valid_choices:
            if st.button(choice["text"], key=f"choice_{choice['text']}"):
                process_choice(choice)
                st.rerun()
    else:
        st.warning("No valid choices available.")


def display_dialogue_player() -> None:
    """Display the main dialogue player interface"""
    # Get the current node
    node = get_current_node()
    if not node:
        return
    
    # Display title if available
    if "title" in node:
        st.subheader(node["title"])
    
    # Display message history
    for msg in st.session_state.message_history:
        render_message(msg)
    
    # Display choices if any
    if "choices" in node:
        render_choices(node.get("choices", []))
    else:
        # Display continue button for nodes without choices
        next_node = node.get("next")
        if next_node:
            if st.button("Continue", key="continue_button"):
                # Apply onexit effects
                apply_effects(node.get("onexit", []))
                advance_to_node(next_node)
                st.rerun()
        else:
            st.success("End of dialogue")


def display_dialogue_info() -> None:
    """Display information about the current dialogue"""
    if not st.session_state.dialogue_data:
        return
        
    with st.expander("Dialogue Information"):
        # Basic info
        st.write(f"**Title:** {st.session_state.dialogue_data.get('title', 'Untitled')}")
        if "author" in st.session_state.dialogue_data:
            st.write(f"**Author:** {st.session_state.dialogue_data['author']}")
        if "version" in st.session_state.dialogue_data:
            st.write(f"**Version:** {st.session_state.dialogue_data['version']}")
            
        # Tags
        if "tags" in st.session_state.dialogue_data:
            st.write(f"**Tags:** {', '.join(st.session_state.dialogue_data['tags'])}")
            
        # Node count
        node_count = len(st.session_state.dialogue_data.get("nodes", {}))
        st.write(f"**Nodes:** {node_count}")
        
        # Current node
        st.write(f"**Current Node:** {st.session_state.current_node_id}")
        
        # History
        st.write(f"**History Length:** {len(st.session_state.history)}")


def display_variables() -> None:
    """Display the current variable values"""
    if not st.session_state.variables:
        return
        
    with st.expander("Variables"):
        # Convert variables to a more readable format
        var_data = []
        for var, value in st.session_state.variables.items():
            var_data.append({"Variable": var, "Value": str(value), "Type": type(value).__name__})
            
        # Display as a table
        st.dataframe(var_data)


def display_controls() -> None:
    """Display player controls"""
    with st.expander("Controls"):
        # Reset button
        if st.button("Reset Dialogue", key="reset_button"):
            reset_dialogue()
            st.rerun()
            
        # Auto-advance toggle
        auto_advance = st.checkbox("Auto-advance through non-choice nodes", value=st.session_state.auto_advance, key="auto_advance_checkbox")
        if auto_advance != st.session_state.auto_advance:
            st.session_state.auto_advance = auto_advance
            st.rerun()
            
        # Debug toggle
        show_debug = st.checkbox("Show debug information", value=st.session_state.show_debug, key="debug_checkbox")
        if show_debug != st.session_state.show_debug:
            st.session_state.show_debug = show_debug
            st.rerun()
            
        # Typing speed
        typing_speed = st.slider("Typing animation speed (ms)", min_value=0, max_value=100, value=st.session_state.typing_speed, key="typing_speed_slider")
        if typing_speed != st.session_state.typing_speed:
            st.session_state.typing_speed = typing_speed
            st.rerun()


def main():
    """Main function to run the Streamlit app"""
    st.set_page_config(
        page_title="Link Loader Dialogue Player",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Add custom CSS for styling
    st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        border-radius: 5px;
    }
    .robot-text {
        color: #FFCC00;
        font-style: italic;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Title and description
    st.title("Link Loader Dialogue Player")
    st.markdown("Play dialogue trees from JSON files")
    
    # Sidebar
    with st.sidebar:
        st.header("Load Dialogue")
        
        # File uploader
        uploaded_file = st.file_uploader("Upload dialogue JSON file", type=["json"])
        
        # Or select from samples
        st.write("Or choose a sample dialogue:")
        sample_path = "/Users/norrisa/Documents/dev/github/linkloadervn/planning/sample_dialogue.json"
        if os.path.exists(sample_path):
            if st.button("Sample: Cargo Bot Conversation"):
                dialogue_data = load_dialogue(sample_path)
                initialize_dialogue(dialogue_data)
                st.rerun()
        
        # Display controls
        st.header("Player Controls")
        display_controls()
        
        # Show dialogue info if debug is enabled
        if st.session_state.show_debug:
            st.header("Dialogue Info")
            display_dialogue_info()
            
            # Show variables
            st.header("Variables")
            display_variables()
    
    # Main content
    if uploaded_file is not None:
        # Load dialogue from uploaded file
        try:
            dialogue_data = json.load(uploaded_file)
            initialize_dialogue(dialogue_data)
        except json.JSONDecodeError as e:
            st.error(f"Error: Invalid JSON in uploaded file: {e}")
    
    # Display dialogue player if data is loaded
    if st.session_state.dialogue_data:
        # Create columns for layout
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Display dialogue player
            display_dialogue_player()
        
        with col2:
            # Display node info if debug is enabled
            if st.session_state.show_debug:
                st.subheader("Current Node")
                node = get_current_node()
                if node:
                    st.json(node)
    else:
        # Show instructions if no dialogue is loaded
        st.info("Upload a dialogue file or select a sample to begin.")
        st.markdown("""
        ## About the Dialogue Format
        
        The dialogue player uses a JSON format inspired by Twine:
        
        - Each dialogue has nodes with content and choices
        - Nodes can have effects on variables
        - Conditions control which choices are available
        - Variables track state throughout the dialogue
        
        For more information, see the [dialogue schema](https://github.com/yourusername/linkloadervn/planning/dialogue_schema.json).
        """)


if __name__ == "__main__":
    main()
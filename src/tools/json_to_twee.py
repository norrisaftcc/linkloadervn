#!/usr/bin/env python3
"""
Convert JSON dialogue format to Twee format for Twine
"""

import json
import sys
from pathlib import Path


def convert_condition(condition):
    """Convert our condition syntax to SugarCube's syntax"""
    # Replace variable names with SugarCube's $ prefix
    condition = condition.replace("cod", "$cod")
    condition = condition.replace("cow", "$cow")
    condition = condition.replace("cos", "$cos")
    condition = condition.replace("terminal_fixed", "$terminal_fixed")
    condition = condition.replace("knows_about_rustlers", "$knows_about_rustlers")
    condition = condition.replace("spoken_robot_language", "$spoken_robot_language")
    condition = condition.replace("robot_trust", "$robot_trust")
    condition = condition.replace("parts_collected", "$parts_collected")
    
    # SugarCube uses standard operators, not word operators
    # Just return the condition with $ prefixes
    return condition


def format_effects(effects):
    """Convert effects to SugarCube macros"""
    output = []
    for effect in effects:
        if effect["type"] == "set":
            output.append(f'<<set ${effect["variable"]} to {json.dumps(effect["value"])}>>')
        elif effect["type"] == "inc":
            output.append(f'<<set ${effect["variable"]} to ${effect["variable"]} + {effect["value"]}>>')
    return "\n".join(output)


def format_character_display(node):
    """Format character sprite/image display"""
    output = []
    
    # Add character image if speaker exists
    if "speaker" in node and node["speaker"] and node["speaker"] != "Slim":
        speaker = node["speaker"].lower().replace(" ", "_")
        emotion = node.get("emotion", "neutral")
        position = node.get("position", "center")
        
        # CSS class for positioning
        output.append(f'<div class="character {position}">')
        output.append(f'<img src="images/{speaker}_{emotion}.png" alt="{node["speaker"]}">')
        output.append('</div>')
    
    return "\n".join(output)


def json_to_twee(json_data):
    """Convert JSON dialogue to Twee format"""
    twee_output = []
    
    # Twee header
    twee_output.append(":: StoryTitle")
    twee_output.append(json_data.get("title", "Untitled Story"))
    twee_output.append("")
    
    # Story data
    twee_output.append(":: StoryData")
    story_data = {
        "ifid": "D7C45122-7E3A-4B8F-9B52-7C5D4BBEB422",  # Valid UUID
        "format": "SugarCube",
        "format-version": "2.30.0",
        "start": json_data.get("start", "intro")
    }
    twee_output.append(json.dumps(story_data, indent=2))
    twee_output.append("")
    
    # CSS Stylesheet
    twee_output.append(":: Stylesheet [stylesheet]")
    twee_output.append("""
/* Character positioning */
.character {
    position: absolute;
    bottom: 10%;
    transition: all 0.3s ease;
}

.character.left { left: 10%; }
.character.center { left: 50%; transform: translateX(-50%); }
.character.right { right: 10%; }

.character img {
    max-height: 400px;
    width: auto;
}

/* Dialogue styling */
.dialogue {
    background: rgba(0, 0, 0, 0.8);
    padding: 20px;
    margin: 20px;
    border: 2px solid #00ff00;
    font-family: monospace;
    color: #00ff00;
}

/* Glitch effect for certain characters */
.glitch {
    animation: glitch 2s infinite;
}

@keyframes glitch {
    0%, 100% { transform: translate(0); }
    20% { transform: translate(-2px, 2px); }
    40% { transform: translate(-2px, -2px); }
    60% { transform: translate(2px, 2px); }
    80% { transform: translate(2px, -2px); }
}
""")
    twee_output.append("")
    
    # StoryInit - Initialize variables
    twee_output.append(":: StoryInit")
    # Set the player name to Slim (no name prompt)
    twee_output.append("<<set $name to \"Slim\">>")
    if "variables" in json_data:
        for var, value in json_data["variables"].items():
            twee_output.append(f"<<set ${var} to {json.dumps(value)}>>")
    
    # Convert nodes to passages
    for node_id, node in json_data["nodes"].items():
        # Passage header with tags
        tags = node.get("tags", [])
        if tags:
            twee_output.append(f":: {node_id} [{' '.join(tags)}]")
        else:
            twee_output.append(f":: {node_id}")
        
        # Character display
        char_display = format_character_display(node)
        if char_display:
            twee_output.append(char_display)
        
        # Entry effects
        if "onentry" in node:
            effects = format_effects(node["onentry"])
            if effects:
                twee_output.append(effects)
        
        # Dialogue content
        twee_output.append('<div class="dialogue">')
        
        # Speaker name
        speaker = node.get("speaker")
        if speaker:
            twee_output.append(f"**{speaker}:**")
        
        # Content with potential glitch effect
        content = node["content"]
        if speaker and speaker.lower() in ["clipi", "cargo bot"]:
            twee_output.append(f'<span class="glitch">{content}</span>')
        else:
            twee_output.append(content)
        
        twee_output.append('</div>')
        
        # Choices or next
        if "choices" in node:
            twee_output.append("")
            for choice in node["choices"]:
                # Handle conditional choices
                if "condition" in choice:
                    condition = convert_condition(choice["condition"])
                    twee_output.append(f"<<if {condition}>>")
                
                # Add effects if present
                if "effects" in choice:
                    effects = format_effects(choice["effects"])
                    # Use <<link>> macro for choices with effects
                    twee_output.append(f"<<link \"{choice['text']}\" \"{choice['next']}\">>{effects}<</link>>")
                else:
                    # Simple link
                    twee_output.append(f"[[{choice['text']}|{choice['next']}]]")
                
                if "condition" in choice:
                    twee_output.append("<</if>>")
                
                twee_output.append("")
        
        elif "next" in node and node["next"]:
            twee_output.append("")
            twee_output.append(f"[[Continue|{node['next']}]]")
        
        twee_output.append("")
    
    return "\n".join(twee_output)


def main():
    if len(sys.argv) < 2:
        print("Usage: python json_to_twee.py <input.json> [output.tw]")
        sys.exit(1)
    
    input_file = Path(sys.argv[1])
    
    if len(sys.argv) >= 3:
        output_file = Path(sys.argv[2])
    else:
        output_file = input_file.with_suffix('.tw')
    
    # Read JSON
    with open(input_file, 'r') as f:
        json_data = json.load(f)
    
    # Convert to Twee
    twee_content = json_to_twee(json_data)
    
    # Write output
    with open(output_file, 'w') as f:
        f.write(twee_content)
    
    print(f"Converted {input_file} to {output_file}")
    print(f"You can import this file into Twine 2 or use it with Tweego")


if __name__ == "__main__":
    main()
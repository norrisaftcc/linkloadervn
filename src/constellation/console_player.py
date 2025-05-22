#!/usr/bin/env python3
"""
Console-based Constellation Engine Player
Simple text-only version for testing story logic
"""

import json
import sys
import os
from pathlib import Path

class ConsolePlayer:
    def __init__(self, story_file):
        self.story_file = story_file
        self.story_data = None
        self.current_scene = None
        self.game_state = {
            'variables': {},
            'history': []
        }
        
    def load_story(self):
        """Load and validate the story JSON"""
        try:
            with open(self.story_file, 'r') as f:
                self.story_data = json.load(f)
            
            print(f"✅ Loaded: {self.story_data.get('title', 'Untitled')}")
            print(f"📄 Version: {self.story_data.get('version', 'Unknown')}")
            print(f"👤 Author: {self.story_data.get('metadata', {}).get('author', 'Unknown')}")
            print(f"📝 Description: {self.story_data.get('metadata', {}).get('description', 'No description')}")
            print(f"🎬 Scenes: {len(self.story_data.get('scenes', {}))}")
            print(f"🎭 Characters: {len(self.story_data.get('characters', {}))}")
            print()
            
            # Validate required fields
            if 'scenes' not in self.story_data:
                raise ValueError("Story must have 'scenes' field")
            
            start_scene = self.story_data.get('startScene')
            if not start_scene:
                raise ValueError("Story must have 'startScene' field")
                
            if start_scene not in self.story_data['scenes']:
                raise ValueError(f"Start scene '{start_scene}' not found in scenes")
                
            print(f"🎯 Starting scene: {start_scene}")
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: Could not find story file: {self.story_file}")
            return False
        except json.JSONDecodeError as e:
            print(f"❌ Error: Invalid JSON in {self.story_file}: {e}")
            return False
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def display_scene(self, scene_id):
        """Display a scene and handle choices"""
        if scene_id not in self.story_data['scenes']:
            print(f"❌ Error: Scene '{scene_id}' not found!")
            return False
            
        scene = self.story_data['scenes'][scene_id]
        self.current_scene = scene_id
        
        print("=" * 60)
        print(f"📍 SCENE: {scene_id}")
        print("=" * 60)
        
        # Display background/music info if present
        if 'background' in scene:
            print(f"🖼️  Background: {scene['background']}")
        if 'music' in scene:
            print(f"🎵 Music: {scene['music']}")
        if 'effects' in scene:
            print(f"✨ Effects: {', '.join(scene['effects'])}")
        if any(k in scene for k in ['background', 'music', 'effects']):
            print()
        
        # Display narrative text
        if 'text' in scene:
            print(f"📜 {scene['text']}")
            print()
        
        # Display dialogue
        if 'dialogue' in scene:
            for line in scene['dialogue']:
                speaker = line.get('speaker', 'Unknown')
                text = line.get('text', '')
                
                # Get character info
                char_info = self.story_data.get('characters', {}).get(speaker, {})
                char_name = char_info.get('name', speaker)
                char_color = char_info.get('color', '')
                
                if speaker == 'narrator':
                    print(f"📖 {text}")
                else:
                    print(f"💬 {char_name}: {text}")
            print()
        
        # Handle choices
        if 'choices' in scene and scene['choices']:
            print("🔀 Your choices:")
            for i, choice in enumerate(scene['choices'], 1):
                choice_text = choice.get('text', 'No text')
                print(f"  {i}. {choice_text}")
            
            print()
            return self.handle_choice(scene['choices'])
        
        # Handle ending
        if 'ending' in scene:
            print(f"🏁 THE END ({scene['ending']})")
            return False
            
        # If no choices and no ending, something's wrong
        print("⚠️  Scene has no choices or ending - story may be incomplete")
        return False
    
    def handle_choice(self, choices):
        """Handle player choice input"""
        while True:
            try:
                choice_input = input("Enter your choice (number): ").strip()
                
                if choice_input.lower() in ['quit', 'exit', 'q']:
                    return False
                
                choice_num = int(choice_input)
                if 1 <= choice_num <= len(choices):
                    choice = choices[choice_num - 1]
                    next_scene = choice.get('next')
                    
                    if not next_scene:
                        print("❌ Error: Choice has no 'next' scene specified!")
                        continue
                    
                    # Add to history
                    self.game_state['history'].append({
                        'scene': self.current_scene,
                        'choice': choice_num - 1,
                        'choice_text': choice.get('text', '')
                    })
                    
                    print(f"➡️  Going to scene: {next_scene}")
                    print()
                    
                    return next_scene
                else:
                    print(f"❌ Please enter a number between 1 and {len(choices)}")
                    
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                return False
    
    def play(self):
        """Main game loop"""
        if not self.load_story():
            return
        
        print("🎮 Starting game... (type 'quit' to exit)")
        print()
        
        current_scene = self.story_data['startScene']
        
        while current_scene:
            next_scene = self.display_scene(current_scene)
            if not next_scene:
                break
            current_scene = next_scene
        
        print()
        print("📊 Game Session Summary:")
        print(f"🎯 Scenes visited: {len(self.game_state['history']) + 1}")
        print(f"🔀 Choices made: {len(self.game_state['history'])}")
        
        if self.game_state['history']:
            print("\n📜 Choice history:")
            for i, entry in enumerate(self.game_state['history'], 1):
                print(f"  {i}. {entry['scene']}: \"{entry['choice_text']}\"")

def main():
    if len(sys.argv) != 2:
        print("Usage: python console_player.py <story_file.json>")
        print()
        print("Example:")
        print("  python console_player.py examples/neon_taxidermy_intro.json")
        return
    
    story_file = sys.argv[1]
    if not os.path.exists(story_file):
        print(f"❌ Story file not found: {story_file}")
        return
    
    player = ConsolePlayer(story_file)
    player.play()

if __name__ == "__main__":
    main()
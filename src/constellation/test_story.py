#!/usr/bin/env python3
"""
Automated Story Tester - Tests scene transitions without user input
"""

import json
import sys

def test_story_transitions(story_file):
    """Test all possible scene transitions"""
    
    with open(story_file, 'r') as f:
        story = json.load(f)
    
    print(f"🧪 Testing story: {story.get('title')}")
    print(f"🎬 Total scenes: {len(story.get('scenes', {}))}")
    print()
    
    scenes = story.get('scenes', {})
    start_scene = story.get('startScene')
    
    # Track all scenes and their connectivity
    scene_graph = {}
    issues = []
    
    for scene_id, scene_data in scenes.items():
        scene_graph[scene_id] = {
            'has_dialogue': 'dialogue' in scene_data,
            'has_choices': 'choices' in scene_data and len(scene_data['choices']) > 0,
            'has_ending': 'ending' in scene_data,
            'next_scenes': []
        }
        
        # Check choices
        if 'choices' in scene_data:
            for i, choice in enumerate(scene_data['choices']):
                if 'next' not in choice:
                    issues.append(f"❌ Scene '{scene_id}' choice {i+1} missing 'next' field")
                elif choice['next'] not in scenes:
                    issues.append(f"❌ Scene '{scene_id}' choice {i+1} points to non-existent scene '{choice['next']}'")
                else:
                    scene_graph[scene_id]['next_scenes'].append(choice['next'])
    
    # Test first scene specifically
    print(f"🎯 Testing start scene: {start_scene}")
    if start_scene not in scenes:
        issues.append(f"❌ Start scene '{start_scene}' not found!")
        return issues
    
    start_scene_data = scenes[start_scene]
    print(f"  📖 Has dialogue: {scene_graph[start_scene]['has_dialogue']}")
    print(f"  🔀 Has choices: {scene_graph[start_scene]['has_choices']}")
    print(f"  🏁 Has ending: {scene_graph[start_scene]['has_ending']}")
    
    if scene_graph[start_scene]['has_choices']:
        print(f"  ➡️  Next scenes: {scene_graph[start_scene]['next_scenes']}")
        
        # Test each choice from start scene
        for next_scene in scene_graph[start_scene]['next_scenes']:
            print(f"    🔍 Testing path to '{next_scene}'...")
            if next_scene in scene_graph:
                next_data = scene_graph[next_scene]
                print(f"      ✅ Scene exists, has dialogue: {next_data['has_dialogue']}, choices: {next_data['has_choices']}")
            else:
                print(f"      ❌ Scene '{next_scene}' not found!")
    
    print()
    print("🔗 Scene Connectivity Analysis:")
    reachable = set()
    
    def find_reachable(scene_id, visited=None):
        if visited is None:
            visited = set()
        if scene_id in visited:
            return
        visited.add(scene_id)
        reachable.add(scene_id)
        
        if scene_id in scene_graph:
            for next_scene in scene_graph[scene_id]['next_scenes']:
                find_reachable(next_scene, visited)
    
    find_reachable(start_scene)
    
    unreachable = set(scenes.keys()) - reachable
    if unreachable:
        print(f"⚠️  Unreachable scenes: {list(unreachable)}")
    else:
        print("✅ All scenes are reachable from start")
    
    print()
    print("📊 Scene Analysis:")
    for scene_id, data in scene_graph.items():
        status = "✅" if scene_id in reachable else "⚠️"
        ending_info = " (ENDING)" if data['has_ending'] else ""
        choices_info = f" -> {data['next_scenes']}" if data['next_scenes'] else ""
        print(f"  {status} {scene_id}{ending_info}{choices_info}")
    
    print()
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"  {issue}")
    else:
        print("✅ No structural issues found!")
    
    return issues

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_story.py <story_file.json>")
        sys.exit(1)
    
    issues = test_story_transitions(sys.argv[1])
    sys.exit(len(issues))
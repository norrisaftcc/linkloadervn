#!/usr/bin/env python3
"""
Script Flow Analyzer for Link Loader
Builds a flow graph of the script structure and detects issues

Author: Chen (Script/Narrative)
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional, Any
from dataclasses import dataclass
from collections import defaultdict
import re

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))
from renpy_game_player import RenpyGame

@dataclass
class FlowNode:
    """Represents a node in the script flow graph"""
    label: str
    filename: str
    line_number: int
    jumps_to: List[str]
    called_by: List[str]
    menu_choices: List[Dict[str, str]]
    conditions: List[str]
    dialogue_count: int
    character_dialogue: Dict[str, int]

class ScriptFlowAnalyzer:
    """Analyzes the flow and structure of Ren'Py scripts"""
    
    def __init__(self, game_path: str):
        self.game = RenpyGame(game_path)
        self.flow_nodes: Dict[str, FlowNode] = {}
        self.orphan_jumps: Set[str] = set()
        self._build_flow_graph()
        
    def _build_flow_graph(self):
        """Build the flow graph from the game scripts"""
        # Create nodes for each label
        for label, content in self.game.labels.items():
            if not content:
                continue
                
            # Get filename and line number from first line
            _, _, filename = content[0]
            
            node = FlowNode(
                label=label,
                filename=filename,
                line_number=0,  # Could extract from content
                jumps_to=[],
                called_by=[],
                menu_choices=[],
                conditions=[],
                dialogue_count=0,
                character_dialogue={}
            )
            
            self.flow_nodes[label] = node
            self._analyze_label_content(label, content)
    
    def _analyze_label_content(self, label: str, content: List[Tuple[int, str, str]]):
        """Analyze the content of a label"""
        node = self.flow_nodes[label]
        in_menu = False
        current_menu_text = ""
        
        for indent, line, filename in content:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Track jumps
            if line.startswith('jump '):
                target = line[5:].strip()
                node.jumps_to.append(target)
                
                # Check if target exists
                if target not in self.game.labels:
                    self.orphan_jumps.add(target)
            
            # Track calls
            elif line.startswith('call '):
                target = line[5:].strip().split()[0]
                node.jumps_to.append(target)
                
                # Add reverse reference
                if target in self.flow_nodes:
                    self.flow_nodes[target].called_by.append(label)
            
            # Track menus
            elif line == 'menu:':
                in_menu = True
                
            elif in_menu:
                # Check for menu prompt
                if line.startswith('"') and line.endswith('"') and not line.endswith('":'):
                    current_menu_text = line[1:-1]
                
                # Check for choices
                elif line.startswith('"') and line.endswith('":'):
                    choice_text = line[1:-2]
                    
                    # Look ahead for jump in this choice
                    choice_data = {
                        'text': choice_text,
                        'menu_text': current_menu_text,
                        'target': None
                    }
                    
                    # Simple lookahead for jump
                    for j in range(1, 10):
                        if indent + j < len(content):
                            _, next_line, _ = content[indent + j]
                            if next_line.strip().startswith('jump '):
                                choice_data['target'] = next_line.strip()[5:].strip()
                                break
                    
                    node.menu_choices.append(choice_data)
                
                # End of menu
                elif indent <= 0:
                    in_menu = False
            
            # Track conditions
            elif line.startswith('if ') and line.endswith(':'):
                condition = line[3:-1].strip()
                node.conditions.append(condition)
            
            # Track dialogue
            elif '"' in line and not line.startswith('$'):
                # Check for character dialogue
                for char_id in self.game.characters:
                    if line.startswith(f'{char_id} "'):
                        node.dialogue_count += 1
                        if char_id not in node.character_dialogue:
                            node.character_dialogue[char_id] = 0
                        node.character_dialogue[char_id] += 1
                        break
                else:
                    # Narrator or other dialogue
                    if line.startswith('"') and line.endswith('"'):
                        node.dialogue_count += 1
                        if 'narrator' not in node.character_dialogue:
                            node.character_dialogue['narrator'] = 0
                        node.character_dialogue['narrator'] += 1
    
    def find_unreachable_labels(self) -> List[str]:
        """Find labels that cannot be reached from start"""
        if 'start' not in self.flow_nodes:
            return list(self.flow_nodes.keys())
        
        visited = set()
        to_visit = ['start']
        
        while to_visit:
            current = to_visit.pop(0)
            if current in visited:
                continue
                
            visited.add(current)
            
            if current in self.flow_nodes:
                node = self.flow_nodes[current]
                
                # Add all jump/call targets
                for target in node.jumps_to:
                    if target not in visited and target in self.flow_nodes:
                        to_visit.append(target)
                
                # Add menu choice targets
                for choice in node.menu_choices:
                    if choice['target'] and choice['target'] not in visited:
                        if choice['target'] in self.flow_nodes:
                            to_visit.append(choice['target'])
        
        # Find unreachable labels
        all_labels = set(self.flow_nodes.keys())
        unreachable = all_labels - visited
        
        return sorted(list(unreachable))
    
    def find_dead_ends(self) -> List[str]:
        """Find labels that don't lead anywhere (no jumps, calls, or returns)"""
        dead_ends = []
        
        for label, node in self.flow_nodes.items():
            # Check if this label has any exits
            has_exit = (
                len(node.jumps_to) > 0 or
                any(choice['target'] for choice in node.menu_choices) or
                label.endswith('_return')  # Common pattern for return labels
            )
            
            if not has_exit:
                # Check if the content has a return statement
                if label in self.game.labels:
                    has_return = any(
                        line.strip() == 'return'
                        for _, line, _ in self.game.labels[label]
                    )
                    if not has_return:
                        dead_ends.append(label)
        
        return sorted(dead_ends)
    
    def analyze_branch_complexity(self) -> Dict[str, Any]:
        """Analyze the branching complexity of the script"""
        complexity_data = {
            'total_labels': len(self.flow_nodes),
            'total_branches': 0,
            'max_branches_per_label': 0,
            'most_complex_label': None,
            'average_branches': 0,
            'menu_count': 0,
            'choice_count': 0
        }
        
        branch_counts = []
        
        for label, node in self.flow_nodes.items():
            # Count branches from this label
            branches = len(node.jumps_to)
            
            # Add menu choices
            for choice in node.menu_choices:
                if choice['target']:
                    branches += 1
                    complexity_data['choice_count'] += 1
            
            if node.menu_choices:
                complexity_data['menu_count'] += 1
            
            branch_counts.append(branches)
            
            if branches > complexity_data['max_branches_per_label']:
                complexity_data['max_branches_per_label'] = branches
                complexity_data['most_complex_label'] = label
        
        complexity_data['total_branches'] = sum(branch_counts)
        complexity_data['average_branches'] = (
            sum(branch_counts) / len(branch_counts) if branch_counts else 0
        )
        
        return complexity_data
    
    def generate_flow_graph_data(self) -> Dict[str, Any]:
        """Generate data for visualization (e.g., with Graphviz or D3.js)"""
        nodes = []
        edges = []
        
        for label, node in self.flow_nodes.items():
            # Node data
            nodes.append({
                'id': label,
                'label': label,
                'dialogue_count': node.dialogue_count,
                'has_menu': len(node.menu_choices) > 0,
                'filename': node.filename
            })
            
            # Regular jumps/calls
            for target in node.jumps_to:
                edges.append({
                    'source': label,
                    'target': target,
                    'type': 'jump'
                })
            
            # Menu choices
            for i, choice in enumerate(node.menu_choices):
                if choice['target']:
                    edges.append({
                        'source': label,
                        'target': choice['target'],
                        'type': 'menu',
                        'label': choice['text'][:30] + '...' if len(choice['text']) > 30 else choice['text']
                    })
        
        return {
            'nodes': nodes,
            'edges': edges
        }
    
    def generate_report(self) -> str:
        """Generate a comprehensive flow analysis report"""
        lines = ["Script Flow Analysis Report", "=" * 40, ""]
        
        # Overview
        lines.append("## Overview")
        lines.append(f"Total labels: {len(self.flow_nodes)}")
        lines.append(f"Total jumps: {sum(len(n.jumps_to) for n in self.flow_nodes.values())}")
        lines.append(f"Total menus: {sum(1 for n in self.flow_nodes.values() if n.menu_choices)}")
        lines.append("")
        
        # Unreachable labels
        unreachable = self.find_unreachable_labels()
        lines.append("## Unreachable Labels")
        if unreachable:
            lines.append(f"Found {len(unreachable)} unreachable labels:")
            for label in unreachable:
                lines.append(f"  - {label}")
        else:
            lines.append("All labels are reachable ✓")
        lines.append("")
        
        # Dead ends
        dead_ends = self.find_dead_ends()
        lines.append("## Dead Ends")
        if dead_ends:
            lines.append(f"Found {len(dead_ends)} dead-end labels:")
            for label in dead_ends:
                lines.append(f"  - {label}")
        else:
            lines.append("No dead ends found ✓")
        lines.append("")
        
        # Orphan jumps
        lines.append("## Missing Jump Targets")
        if self.orphan_jumps:
            lines.append(f"Found {len(self.orphan_jumps)} jumps to non-existent labels:")
            for target in sorted(self.orphan_jumps):
                lines.append(f"  - {target}")
        else:
            lines.append("All jump targets exist ✓")
        lines.append("")
        
        # Complexity analysis
        complexity = self.analyze_branch_complexity()
        lines.append("## Complexity Analysis")
        lines.append(f"Total branches: {complexity['total_branches']}")
        lines.append(f"Average branches per label: {complexity['average_branches']:.2f}")
        lines.append(f"Most complex label: {complexity['most_complex_label']} ({complexity['max_branches_per_label']} branches)")
        lines.append(f"Total menus: {complexity['menu_count']}")
        lines.append(f"Total choices: {complexity['choice_count']}")
        lines.append("")
        
        # Character dialogue distribution
        lines.append("## Character Dialogue Distribution")
        total_dialogue = sum(n.dialogue_count for n in self.flow_nodes.values())
        character_totals = defaultdict(int)
        
        for node in self.flow_nodes.values():
            for char, count in node.character_dialogue.items():
                character_totals[char] += count
        
        for char, count in sorted(character_totals.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total_dialogue * 100) if total_dialogue > 0 else 0
            char_name = self.game.characters[char].name if char in self.game.characters else char
            lines.append(f"  {char_name}: {count} lines ({percentage:.1f}%)")
        
        return "\n".join(lines)
    
    def export_to_json(self, output_path: str):
        """Export the analysis to JSON format"""
        data = {
            'overview': {
                'total_labels': len(self.flow_nodes),
                'total_characters': len(self.game.characters),
                'total_variables': len(self.game.default_variables)
            },
            'unreachable_labels': self.find_unreachable_labels(),
            'dead_ends': self.find_dead_ends(),
            'orphan_jumps': sorted(list(self.orphan_jumps)),
            'flow_graph': self.generate_flow_graph_data(),
            'complexity': self.analyze_branch_complexity()
        }
        
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Analysis exported to {output_path}")

def main():
    """Run the flow analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Analyze Link Loader script flow")
    parser.add_argument("--game", default="../current/renpy-8.3.7-sdk/link_loader_1_2/game",
                        help="Path to game directory")
    parser.add_argument("--export", help="Export analysis to JSON file")
    parser.add_argument("--format", choices=["console", "json"], default="console",
                        help="Output format")
    
    args = parser.parse_args()
    
    # Create analyzer
    print("Analyzing script flow...")
    analyzer = ScriptFlowAnalyzer(args.game)
    
    # Generate report
    if args.format == "console":
        report = analyzer.generate_report()
        print("\n" + report)
    
    # Export if requested
    if args.export:
        analyzer.export_to_json(args.export)
    
    # Generate visualization data
    graph_data = analyzer.generate_flow_graph_data()
    
    # Save visualization data
    with open("flow_graph.json", "w") as f:
        json.dump(graph_data, f, indent=2)
    print("\nFlow graph data saved to flow_graph.json")

if __name__ == "__main__":
    main()
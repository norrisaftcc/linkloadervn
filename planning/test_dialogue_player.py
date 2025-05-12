#!/usr/bin/env python3
"""
Unit tests for the dialogue player
"""

import unittest
import tempfile
import json
import os
import io
import sys
from unittest.mock import patch, MagicMock
from dialogue_player import DialoguePlayer


class TestDialoguePlayer(unittest.TestCase):
    """Tests for the DialoguePlayer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create a simple test dialogue
        self.test_dialogue = {
            "title": "Test Dialogue",
            "author": "Test Author",
            "version": "1.0",
            "default_speaker": "Tester",
            "variables": {
                "test_var": 0,
                "flag": False
            },
            "start": "start_node",
            "nodes": {
                "start_node": {
                    "title": "Start Node",
                    "content": "This is the start of the dialogue.",
                    "next": "choice_node"
                },
                "choice_node": {
                    "title": "Choice Node",
                    "content": "Please make a choice.",
                    "choices": [
                        {
                            "text": "Option 1",
                            "next": "option1_node",
                            "effects": [
                                {
                                    "type": "set",
                                    "variable": "test_var",
                                    "value": 1
                                }
                            ]
                        },
                        {
                            "text": "Option 2",
                            "next": "option2_node",
                            "effects": [
                                {
                                    "type": "set",
                                    "variable": "test_var",
                                    "value": 2
                                }
                            ]
                        },
                        {
                            "text": "Conditional Option",
                            "condition": "flag == True",
                            "next": "end_node"
                        }
                    ]
                },
                "option1_node": {
                    "title": "Option 1 Node",
                    "content": "You selected option 1.",
                    "next": "end_node"
                },
                "option2_node": {
                    "title": "Option 2 Node",
                    "content": "You selected option 2.",
                    "next": "end_node"
                },
                "end_node": {
                    "title": "End Node",
                    "content": "This is the end of the dialogue.",
                    "next": None
                }
            }
        }
        
        # Create a temporary file with the test dialogue
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump(self.test_dialogue, self.temp_file)
        self.temp_file.close()
        
        # Create a player with typing disabled for tests
        self.player = DialoguePlayer(self.temp_file.name, typing_speed=0)
        
    def tearDown(self):
        """Tear down test fixtures"""
        os.unlink(self.temp_file.name)
    
    def test_load_dialogue(self):
        """Test loading a dialogue file"""
        self.assertEqual(self.player.dialogue_data["title"], "Test Dialogue")
        self.assertEqual(self.player.current_node_id, "start_node")
        self.assertEqual(self.player.variables["test_var"], 0)
        
    def test_get_current_node(self):
        """Test getting the current node"""
        node = self.player._get_current_node()
        self.assertEqual(node["title"], "Start Node")
        self.assertEqual(node["content"], "This is the start of the dialogue.")
        
    def test_evaluate_condition_true(self):
        """Test evaluating a true condition"""
        self.player.variables["flag"] = True
        self.assertTrue(self.player._evaluate_condition("flag == True"))
        
    def test_evaluate_condition_false(self):
        """Test evaluating a false condition"""
        self.player.variables["flag"] = False
        self.assertFalse(self.player._evaluate_condition("flag == True"))
        
    def test_apply_effects(self):
        """Test applying effects to variables"""
        effects = [
            {"type": "set", "variable": "test_var", "value": 42},
            {"type": "inc", "variable": "counter", "value": 1},
            {"type": "toggle", "variable": "flag"}
        ]
        
        self.player.variables = {"test_var": 0, "counter": 0, "flag": False}
        self.player._apply_effects(effects)
        
        self.assertEqual(self.player.variables["test_var"], 42)
        self.assertEqual(self.player.variables["counter"], 1)
        self.assertEqual(self.player.variables["flag"], True)
        
    def test_apply_effects_complex(self):
        """Test applying more complex effects"""
        effects = [
            {"type": "push", "variable": "stack", "value": "item1"},
            {"type": "push", "variable": "stack", "value": "item2"},
            {"type": "pop", "variable": "stack"}
        ]
        
        self.player.variables = {}
        self.player._apply_effects(effects)
        
        self.assertEqual(self.player.variables["stack"], ["item1"])
        
    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_node_with_next(self, mock_stdout, mock_input):
        """Test playing a node with a next attribute"""
        self.player.current_node_id = "start_node"
        self.player.play_node()
        
        # Check that we've moved to the next node
        self.assertEqual(self.player.current_node_id, "choice_node")
        
        # Check that content was printed (ignoring ANSI color codes)
        output = mock_stdout.getvalue()
        self.assertIn("This is the start of the dialogue.", output)
        
    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_play_node_with_choices(self, mock_stdout, mock_input):
        """Test playing a node with choices"""
        self.player.current_node_id = "choice_node"
        self.player.play_node()
        
        # Check that we've moved to the selected node
        self.assertEqual(self.player.current_node_id, "option1_node")
        
        # Check that the effect was applied
        self.assertEqual(self.player.variables["test_var"], 1)
        
        # Check that choices were printed
        output = mock_stdout.getvalue()
        self.assertIn("Please make a choice.", output)
        self.assertIn("Option 1", output)
        self.assertIn("Option 2", output)
        
    @patch('builtins.input', return_value='1')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_conditional_choices(self, mock_stdout, mock_input):
        """Test that conditional choices are properly filtered"""
        self.player.current_node_id = "choice_node"
        
        # First with flag = False (should not show conditional option)
        self.player.variables["flag"] = False
        node = self.player._get_current_node()
        choices = node.get("choices", [])
        valid_choices = self.player._print_choices(choices)
        
        # Should only have 2 options (Option 1 and Option 2)
        self.assertEqual(len(valid_choices), 2)
        
        # Now with flag = True (should show conditional option)
        self.player.variables["flag"] = True
        valid_choices = self.player._print_choices(choices)
        
        # Should have all 3 options
        self.assertEqual(len(valid_choices), 3)
        
    def test_reset(self):
        """Test resetting the dialogue"""
        # Save original values
        original_node_id = self.player.current_node_id

        # Change some values
        self.player.current_node_id = "end_node"
        self.player.history = ["start_node", "choice_node", "option1_node", "end_node"]

        # Reset
        self.player.reset()

        # Verify reset values
        self.assertEqual(self.player.current_node_id, original_node_id)
        self.assertEqual(self.player.history, [])
        
    @patch('builtins.input', return_value='')
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_format_robot_language(self, mock_stdout, mock_input):
        """Test robot language formatting"""
        robot_text = "This contains (Sh-robot sh-language)"
        formatted = self.player._format_robot_language(robot_text)
        
        # The formatted text should be longer due to ANSI codes
        self.assertGreater(len(formatted), len(robot_text))
        
    def test_play_dialogue_flow(self):
        """Test dialogue flow without running the full play method"""
        # Manual node traversal
        self.assertEqual(self.player.current_node_id, "start_node")

        # Move to next node
        self.player.current_node_id = "choice_node"
        node = self.player._get_current_node()
        self.assertEqual(node["title"], "Choice Node")

        # Move to option 1
        self.player.current_node_id = "option1_node"
        self.player.variables["test_var"] = 1  # Simulate effect
        node = self.player._get_current_node()
        self.assertEqual(node["title"], "Option 1 Node")

        # Move to end node
        self.player.current_node_id = "end_node"
        node = self.player._get_current_node()
        self.assertEqual(node["title"], "End Node")

        # End of dialogue
        self.assertEqual(node["next"], None)


if __name__ == '__main__':
    unittest.main()
#!/usr/bin/env python3
"""
Tests for Ren'Py to Twee converter
"""

import unittest
from pathlib import Path
import tempfile
import os


class TestRenpyToTwee(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        # Clean up temp files
        for file in Path(self.temp_dir).glob("*"):
            file.unlink()
        os.rmdir(self.temp_dir)
    
    def convert_script(self, renpy_script):
        """Helper to convert a Ren'Py script string to Twee"""
        # Import will be from the actual converter once we implement it
        # For now, this is a placeholder
        from renpy_to_twee_v2 import RenpyToTweeConverter
        converter = RenpyToTweeConverter()
        return converter.convert(renpy_script)
    
    def test_basic_dialogue(self):
        """Test simple character dialogue"""
        renpy = '''
define s = Character("Slim")

label start:
    s "Hello world!"
    s "This is a test."
    return
'''
        expected_twee = ''':: start
Slim: Hello world!

Slim: This is a test.

THE END'''
        
        result = self.convert_script(renpy)
        self.assertIn("Slim: Hello world!", result)
        self.assertIn("Slim: This is a test.", result)
    
    def test_menu_with_choices(self):
        """Test menu conversion"""
        renpy = '''
define s = Character("Slim")

label start:
    s "What should I do?"
    
    menu:
        "Go left":
            jump left_path
        "Go right":
            jump right_path
            
label left_path:
    s "Going left!"
    return
    
label right_path:
    s "Going right!"
    return
'''
        result = self.convert_script(renpy)
        self.assertIn("[[Go left|left_path]]", result)
        self.assertIn("[[Go right|right_path]]", result)
    
    def test_variables_and_conditions(self):
        """Test variable handling"""
        renpy = '''
define s = Character("Slim")
default strength = 0

label start:
    $ strength = 5
    
    s "My strength is now higher."
    
    menu:
        "Test strength" if strength > 3:
            jump strong_path
        "Be careful":
            jump weak_path
'''
        result = self.convert_script(renpy)
        self.assertIn("<<set $strength to 5>>", result)
        self.assertIn("<<if $strength > 3>>", result)
    
    def test_jump_and_labels(self):
        """Test label and jump handling"""
        renpy = '''
label start:
    "Beginning of story"
    jump middle
    
label middle:
    "Middle of story"
    jump end
    
label end:
    "The end"
    return
'''
        result = self.convert_script(renpy)
        self.assertIn(":: start", result)
        self.assertIn(":: middle", result)
        self.assertIn(":: end", result)
        self.assertIn("[[Continue|middle]]", result)
        self.assertIn("[[Continue|end]]", result)
    
    def test_character_with_no_definition(self):
        """Test handling of undefined characters"""
        renpy = '''
label start:
    "This is narration."
    unknown_char "Who am I?"
    return
'''
        result = self.convert_script(renpy)
        self.assertIn("This is narration.", result)
        self.assertIn("unknown_char: Who am I?", result)
    
    def test_complex_menu_with_effects(self):
        """Test menu with variable changes"""
        renpy = '''
define s = Character("Slim")
default karma = 0

label start:
    menu:
        "Help someone":
            $ karma += 1
            s "That was nice of me."
            jump good_end
            
        "Be selfish":
            $ karma -= 1
            s "I look out for myself."
            jump bad_end
'''
        result = self.convert_script(renpy)
        # Should create a choice with effects
        self.assertIn("Help someone", result)
        self.assertIn("<<set $karma to $karma + 1>>", result)
    
    def test_narrator_text(self):
        """Test narrator/unattributed text"""
        renpy = '''
label start:
    "It was a dark and stormy night."
    "The wind howled through the trees."
    return
'''
        result = self.convert_script(renpy)
        self.assertIn("It was a dark and stormy night.", result)
        self.assertIn("The wind howled through the trees.", result)
    
    def test_special_characters_in_dialogue(self):
        """Test handling of special characters"""
        renpy = '''
define s = Character("Slim")

label start:
    s "What's up? I'm ready!"
    s "This has \"quotes\" in it."
    return
'''
        result = self.convert_script(renpy)
        self.assertIn("What's up? I'm ready!", result)
        self.assertIn('This has "quotes" in it.', result)
    
    def test_empty_script(self):
        """Test empty/minimal script"""
        renpy = '''
label start:
    return
'''
        result = self.convert_script(renpy)
        self.assertIn(":: start", result)
        self.assertIn("THE END", result)
    
    def test_nvl_mode(self):
        """Test NVL mode handling (should convert to regular text)"""
        renpy = '''
define n = Character(None, kind=nvl)

label start:
    n "This is NVL mode text."
    n "It should convert to regular text."
    nvl clear
    return
'''
        result = self.convert_script(renpy)
        self.assertIn("This is NVL mode text.", result)
        self.assertIn("It should convert to regular text.", result)


if __name__ == "__main__":
    unittest.main()
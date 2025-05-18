#!/bin/bash
# Quick demo of the Link Loader text player

echo "Link Loader Text Player - Quick Demo"
echo "===================================="
echo
echo "This script will create a simple demo game and run it."
echo

# Create a simple demo script
cat > quick_demo.rpy << 'EOF'
# Quick Demo Script
define slim = Character("Slim", color="#c8ffc8")
define clipi = Character("Clipi", color="#00ff00")

default points = 0

label start:
    scene black
    
    "Welcome to Link Loader - Text Mode Demo!"
    
    slim "Howdy, partner! I'm Slim."
    
    show clipi normal at right
    
    clipi "And I'm Clipi, your AI assistant!"
    
    menu:
        "What brings you to Syntax-4?"
        
        "Looking for adventure":
            $ points += 1
            slim "Well, you've come to the right place!"
            clipi "Plenty of broken link loaders to fix."
            
        "Just passing through":
            slim "Fair enough. This desert planet ain't for everyone."
            clipi "But the work pays well!"
    
    slim "Want to see what we do?"
    
    show terminal idle
    
    "A terminal appears, showing corrupted LISP code..."
    
    "(load (car (cdr (cons))))"
    
    clipi "That's a syntax error! Missing data in the innermost function."
    
    menu:
        "How would you fix it?"
        
        "Add the missing data":
            $ points += 1
            slim "Good thinking! That's the direct approach."
            
        "Rewrite the whole thing":
            slim "Sometimes starting fresh is the best solution."
    
    "Your adventure points: [points]"
    
    slim "Thanks for trying the demo!"
    
    return
EOF

echo "Demo script created: quick_demo.rpy"
echo
echo "Running the demo..."
echo "===================="
echo

# Run the demo with the simple player
python renpy_player.py quick_demo.rpy --no-typing

echo
echo "===================="
echo "Demo complete!"
echo
echo "To play the full Link Loader game in text mode, run:"
echo "  python play_linkloader.py"
echo
echo "To play this demo again with typing effect:"
echo "  python renpy_player.py quick_demo.rpy"
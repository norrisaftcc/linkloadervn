
# Test Script
define pc = Character("Player", color="#00ff00")
define npc = Character("NPC", color="#ff0000")

default points = 0

label start:
    scene black
    
    "Welcome to the test game!"
    
    pc "Hello, I'm the player character."
    
    npc "Nice to meet you! Let me ask you something."
    
    menu:
        npc "Do you like visual novels?"
        
        "Yes, I love them!":
            $ points += 1
            npc "That's great! Me too."
            jump good_end
            
        "They're okay.":
            npc "Fair enough."
            jump neutral_end
            
        "Not really.":
            $ points -= 1
            npc "Oh, that's too bad."
            jump bad_end

label good_end:
    pc "This has been fun!"
    "You got the good ending! Points: [points]"
    return

label neutral_end:
    pc "Thanks for the chat."
    "You got the neutral ending. Points: [points]"
    return
    
label bad_end:
    pc "Well, bye then."
    "You got the bad ending. Points: [points]"
    return

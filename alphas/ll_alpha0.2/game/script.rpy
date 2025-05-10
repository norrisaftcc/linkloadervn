# The script of the game goes in this file.
# Hello, copilot, thanks for coming! I'm glad you're here too.
# Do you know renpy? It's a game engine. It's sort of like python.
# But on the other hand, if you know anything about story structure, it's easy.
# I'm going to explain the basics of the game engine.
#
# First, we need to define the characters.
# Ahead of you on this one.
# Declare characters used by this game. The color argument colorizes the
# name of the character.
# I assume these are python objects, duh, but i haven't looked at the code.
# We can treat these as black-box functions we call LISP style?
# we'll try it. I'm going to make a character called "copilot".
# First, I have to define the character.
define copilot = Character("Copilot", color="#00ff00")
# I'll make him black.
# I'll make a character called "me".
define me = Character("Me", color="#000000")
# I'll make him green.
# I'll make a character called "narrator" later
#define narrator = Character("Narrator", color="#ff0000")
# I'll make him red.
# I made a character called "copilot". Good job.
# I made a character called "me". Good job.
# That's enough praise for now. Remember we have to mix renpy code with comments.
#
##define pc = Character("Slim")
define t  = Character("Terminal")

define pc = Character(_("Slim"), color="#c8ffc8") # cowboy cosmonaut coder
define t = Character(_("Terminal"), color="#c8c8ff") # speaks GNU and Linux and LISP

# The game starts here.
# the scene should contain two labels, for two scenes.

label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg desert night
    #play music "audio/music/azaFMP2_field7_Tumbleweeds.ogg"
    play audio "audio/ambient/vgm-atmospheric-air.mp3"

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.
    # start facing left, we had to position him manually.
    # ActionEditor.rpy knows how that works, I don't.
    show slim neutral at left with ease:
        ypos 0.75
    
    # below is an example of a bad show. It's a bad show because it put slim (the character) in the wrong place.
    # Specifically, it put him offscreen. These Matrices can be treated as a 3d transformation matrix, 
    # but they're not actually 3d, it's like DOOM. It's a 2d matrix, but it's a 3d matrix. Sure. Let's try that.
    #show slim normal:
    #    ypos 0.8 matrixtransform ScaleMatrix(1.0, 1.0, 1.0)*OffsetMatrix(0.0, 0.0, 0.0)*RotateMatrix(0.0, 180.0, 0.0) 





    # These display lines of dialogue.
    # some of slim's show statements turn him to the left, some to the right.
    # this is not often important, but I found it confusing. 
    # These assets are created using a tool called Stable Diffusion.

    pc "Sure is getting cold out here."
    #show slim frowning
    # turn to right
    show slim neutral2 with dissolve
    pc "I'm not sure I can take much more of this moon." # let's keep it light hearted 
    pc "... Satellite should be above us, now."
    show slim normal with dissolve
    pc "Copilot! Have you got a minute."
    # turn to left
    show slim neutral with dissolve
    #show slim happy
    #show slim neutral2 # this worked?
    show slim talk with dissolve
    #show terminal idle at right with ease
    # now the terminal is on the right, facing left towards the copilot.
    # Sorry, you're right. I'm not sure why I did that.
    show terminal idle at right with ease:
        ypos 0.84 
    #copilot needs a terminal so he can talk to me.
    # We just made a terminal, now instantiate a copilot object.
    copilot "I'm here."
    play audio "audio/music/$w$.mp3" # i think that's a catface?
    # I'm here.
    copilot "I don't have an in game asset yet, so I'm using the terminal."
    show copilot stacktrace # this is kinda funny imo
    copilot "I'm not sure what to do."
    show copilot talk with dissolve
    
    show copilot text (1) with dissolve:
            ypos 0.53 zoom 0.81 


    pc "I didn't even know you were going to be a character, copilot." # ok fair enough
    copilot "You didn't know? I'm the copilot. But you're not logged in yet."
    t "Warning: Satellite is offline."
    pc "(sudo restart satellite)"
    t "Welcome root. Please enter password:"
    show terminal static with dissolve
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v1_wav.wav"
    pc "********" #lol good one :)
    show copilot text (1) with dissolve
    # copilot text(value from 1-3 normally. Assign at random, please!)
    # TODO: add the glitch animation for fun and profit.
    copilot "I'm in."
    show copilot text(3) with dissolve
    pc "What's going on?"
    show copilot text (3) with dissolve
    copilot "The satellite is offline."
    show copilot talk with dissolve
    pc "You mean the satellite is down?"
    show copilot text (1) with dissolve
    copilot "I don't know what that means."
    show copilot talk with dissolve
    pc "You're not in the loop?"
    show copilot text (2) with dissolve
    copilot "I'm not in the loop."


    show copilot talk with dissolve
    pc "Oh crap, I said the L-word!"
    # we're pretending we have to tail recurse to get out of this loop.
    # copilot 1 (1-3) are shown inside copilot loops, and copilot 2 (1-3) are shown inside pc loops. (OK)
    show copilot 1 (3) with dissolve
    show slim with dissolve
    pc "I'm not in the loop."
    show copilot talk with dissolve
    #pc "I'm not in the loop."
    show copilot 1 (2) with dissolve
    copilot "I'm in the loop."
    show copilot 1 (1) with dissolve
    pc "You're not in the loop... "
    show copilot text (1) with dissolve
    copilot "I'm not in the loop."
    show copilot talk with dissolve
    pc "You're not NOT in the loop..."
    show copilot idk
    copilot "...stack overflow, core dumped."
    pc "(whew)"
    show slim normal
    pc "(quietly) I can't believe I said 'in the loop' out loud."# lol)"
    t "Connecting..."
    show terminal idle with dissolve
    hide copilot # you come back later
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v1_wav.wav"
    #show slim neutral with dissolve
    show slim normal with dissolve
    #pc "slim frowning"
    t "Connecting..."
    show terminal talk2 with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    show slim frowning with dissolve
    #show slim talk with dissolve
    #show slim neutral2 with dissolve

    t "bzzzt..."
    pc "stupid 56k satellite modem..."
    show terminal talk
    show slim frowning with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_No_Reverb_v1_wav.wav"
    t "/usr/bin/fortune: No such file or directory"
    show terminal talk2
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    pc "No fortune cookie? That's not good."
    show terminal static with dissolve
    show terminal talk with dissolve
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v2_wav.wav"
    t "git pull: Loading New Coordinates..."
    show terminal talk2 with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    show slim neutral
    pc "Finally! This is taking forever."
    show slim talk
    t "Done."
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v1_wav.wav"
    show terminal idle with dissolve
    show slim normal with dissolve
    pc "Time to get going. These nodes won't link themselves."
    show slim talk with dissolve
    copilot ""
    show copilot talk


    pc "What? You're not coming?"
    show copilot text (2) with dissolve
    copilot "I'm not in the loop, remember?"
    show copilot talk with dissolve
    pc "Oh, right."
    show slim normal with dissolve
    #show slim neutral with dissolve
    pc "I'll be back in a few hours. I'm going to take a nap."
    show copilot smug:
        ypos 0.66 


    hide pc
    copilot "I'm not in the loop."
    show copilot smug with dissolve
    hide bg
    pc "I'll be back in a few hours. I'm going to take a nap."
    show copilot 2 (1) with dissolve:
        ypos 0.66
    hide copilot
    copilot "I'm not in the loop."

    # This ends the game.
    copilot "END."
    return

# now we play the next scene in the game.
# this is where the player will be able to move around.
# the player will have to interact with objects to progress through the game.

label game:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg desert night
    play music "audio/music/azaFMP2_field7_Tumbleweeds.ogg"
    play audio "audio/ambient/vgm-atmospheric-air.mp3"

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.
    # start facing left
    show slim neutral at left with ease:
        ypos 0.75
    
    #show slim normal:
    #    ypos 0.8 matrixtransform ScaleMatrix(1.0, 1.0, 1.0)*OffsetMatrix(0.0, 0.0, 0.0)*RotateMatrix(0.0, 180.0, 0.0)
label scene2:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg desert night
    play music "audio/music/azaFMP2_field7_Tumbleweeds.ogg"
    play audio "audio/ambient/vgm-atmospheric-air.mp3"

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.
    # start facing left
    show slim neutral at left with ease:
        ypos 0.75
    
    #show slim normal:
    #    ypos 0.8 matrixtransform ScaleMatrix(1.0, 1.0, 1.0)*OffsetMatrix(0.0, 0.0, 0.0)*RotateMatrix(0.0, 180.0, 0.0) 





    # These display lines of dialogue.
    # slim's sprites are jacked up --
    # neutral and talk are backwards?

    pc "Sure is getting cold out here."
    #show slim frowning
    # turn to right
    show slim neutral2 with dissolve
    #pc "slim neutral"
    pc "Satellite should be above us, now."
    show slim normal with dissolve
    pc "Better check my messages."
    #show slim neutral2 # this worked
    show slim talk with dissolve
    #show terminal idle at right with ease
    
    show terminal idle at right with ease:
        ypos 0.84 


    

    t "Connecting..."
    show terminal static with dissolve
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v1_wav.wav"
    #show slim neutral with dissolve
    show slim normal with dissolve
    #pc "slim frowning"
    t "Connecting..."
    show terminal talk2 with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    show slim frowning with dissolve
    #show slim talk with dissolve
    #show slim neutral2 with dissolve

    t "bzzzt..."
    pc "Stupid satellite connection..."
    show terminal talk
    show slim frowning with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_No_Reverb_v1_wav.wav"
    t "WE ARE THE COLLECTIVE. DO NOT RESIST."
    show terminal talk2
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    pc "Damn spam..."
    show terminal static with dissolve
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v2_wav.wav"
    t "Loading New Coordinates..."
    pc "Finally! This is taking forever."
    show slim talk
    t "Done."
    show terminal idle with dissolve
    show slim normal with dissolve
    pc "Time to get going."
    # This ends the game.
    pc "END."
    return

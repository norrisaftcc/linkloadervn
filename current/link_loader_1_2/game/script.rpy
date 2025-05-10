# The script of the game goes in this file.
# I'm going to explain the basics of the game engine.
#
# First, we need to define the characters.

# Declare characters used by this game. The color argument colorizes the
# name of the character.
# I assume these are python objects, duh, but i haven't looked at the code.
# We can treat these as black-box functions we call LISP style?
# we'll try it. I'm going to make a character called "clipi".
# First, I have to define the character.
define clipi = Character("clipi", color="#00ff00")
# I'll make him black.
# I'll make a character called "me".
# define me = Character("Me", color="#000000")
# I'll make him green.
# I'll make a character called "narrator" later
#define narrator = Character("Narrator", color="#ff0000")
# I'll make him red.
# I made a character called "clipi". Good job.
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

    #scene bg desert night
    
    show bg desert night:
            zoom 0.31 

    $ renpy.music.set_volume(0.5)
    play music "audio/music/azaFMP2_field7_Tumbleweeds.ogg"
    play audio "audio/ambient/vgm-atmospheric-air.mp3"

    # This shows a character sprite. A placeholder is used, but you can
    # replace it by adding a file named "eileen happy.png" to the images
    # directory.
    # start facing left, we had to position him manually.
    # ActionEditor.rpy knows how that works, I don't.
    pc "(hello world)" # i'll alow it
    show slim neutral at left with easeinleft:
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
    pc "Clipi! Have you got a minute?"
    # turn to left

    show slim neutral with dissolve
    pc "...just where is that dad-gum neural network?"
    #show slim happy
    #show slim neutral2 # this worked?
    show slim talk 
    
    show slim talk with dissolve
    #show terminal idle at right with ease
    # now the terminal is on the right, facing left towards the clipi.
    # Sorry, you're right. I'm not sure why I did that.
    show terminal idle at right with easeinright:
        ypos 0.84 
    #clipi needs a terminal so he can talk to me.
    # We just made a terminal, now instantiate a clipi object.
    
    #show clipi text (1):
    #    pos (1009, 0.31) zoom 0.31  
    
    show clipi text (1) with dissolve:
            pos (950, 0.24) zoom 0.38  




    clipi "I'm here."
    #play audio "audio/music/$w$.mp3" # i think that's a catface?
    # I'm here.
    #clipi "I don't have an in game asset yet, so I'm using the terminal."
    # show clipi stacktrace # this is kinda funny imo
    #show clipi text (1) with dissolve:
    #        ypos 0.53 zoom 0.81 
    
    show clipi text (1):
        pos (925, 0.22) zoom 0.44 


    #clipi "I'm not sure what to do..."
    image clipi glitched:
        At("clipi", glitch)
        pause 0.2
        At("clipi", chromatic_offset)
        pause 0.2
        At("clipi", glitch)
        pause 0.2
        At("clipi", chromatic_offset)
        pause 0.1
        At("clipi", glitch)
        pause 0.3
        At("clipi", chromatic_offset)

    image clipi glitched2:
        At("clipi", glitch)
        pause 0.1
        At("clipi", chromatic_offset)
        pause 0.1
        At("clipi", glitch)
        pause 0.3
        At("clipi", chromatic_offset)
        pause 0.1
        At("clipi", glitch)
        pause 0.2
        At("clipi", chromatic_offset)
        pause 0.3
        At("clipi", glitch)
        pause 0.1
        At("clipi", chromatic_offset)

    show clipi text with dissolve:
        pos (910, 0.26) zoom 0.41 
    show clipi glitched:
        pos (9100, 0.26) zoom 0.41 
    show clipi talk with dissolve:
        pos (910, 0.26) zoom 0.41 
    
    
    show clipi glitched2:
            pos (910, 0.26) zoom 0.38





    pc "I didn't even know you were going to be a character, clipi." # ok fair enough
    clipi "You didn't know? I'm the co-pilot. But you're not logged in yet."
    t "Warning: Satellite is offline."
    pc "(sudo restart satellite)"
    t "Welcome root. Please enter password:"
    show terminal static with dissolve
    pc "********" #lol good one :)
    show clipi text (1) with dissolve
    show clipi glitched
    # clipi text(value from 1-3 normally. Assign at random, please!)
    # TODO: add the glitch animation for fun and profit.
    clipi "I'm in."
    show clipi text(2) with dissolve
    pc "What's going on?"
    show clipi text (2) with dissolve
    clipi "The satellite is offline."
    show clipi talk with dissolve
    pc "You mean the satellite is down?"
    show clipi text (1) with dissolve
    clipi "I don't know what that means."
    show clipi talk with dissolve
    pc "You're not in the loop?"
    show clipi text (2) with dissolve
    clipi "I'm not in the loop.)"
    show clipi glitched2
    show clipi talk with dissolve
    pc "Oh crap, I used the L-word."
    # we're pretending we have to tail recurse to get out of this loop.
    # clipi 1 (1-3) are shown inside clipi loops, and clipi 2 (1-3) are shown inside pc loops. (OK)
    show clipi 1 (3) with dissolve
    show slim with dissolve
    pc "I'm not in the loop?"
    show clipi 1 (2) with dissolve
    clipi "I'm not in the loop.))"
    show clipi talk with dissolve
    show slim frowning with dissolve
    pc "oops... YOU'RE not in the loop."
    show clipi 1 (2) with dissolve
    clipi "I'm not in the loop.)))"
    show clipi 1 (1) with dissolve
    show slim talk with dissolve
    show clipi talk with dissolve
    pc "You're not in the ()@!# loop!"
        
    show clipi glitched2:
            pos (910, 0.28) zoom 0.38
    clipi "...stack overflow, core dumped."
    pc "I'll give you a second."
    show slim normal
    pc "(quietly) I can't believe I said 'in the loop' out loud."# lol)"
    t "Connecting..."
    show terminal idle with dissolve
    hide clipi with dissolve
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
    pc "The Company really thought 56k was enough bandwidth, huh..."
    show terminal talk
    show slim frowning with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_No_Reverb_v1_wav.wav"
    t "/usr/bin/fortune: No such file or directory"
    show terminal talk2
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    pc "Not even a lousy fortune cookie?"
    show terminal static with dissolve
    show terminal talk with dissolve
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v2_wav.wav"
    t "git pull: Loading New Coordinates..."
    show terminal talk2 with dissolve
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    pc "Finally! This is taking forever."
    show slim talk
    t "Done."
    show terminal idle with dissolve
    show slim normal with dissolve
    pc "Time to get going. These nodes won't link themselves."
    show slim talk with dissolve
    clipi ""
    show clipi talk with dissolve
    pc "What? You're not coming?"
    show clipi text (2) with dissolve
    clipi "I'm not in the loop."
    show clipi talk with dissolve
    pc "Oh, right."
    show slim normal with dissolve
    #show slim neutral with dissolve
    pc "I'll be back in a few hours. I'm going to take a nap."
    show clipi text (1) with dissolve
    clipi "I'm not in the loop."
    show clipi smug with dissolve
    pc "I'll be back in a few hours. I'm going to take a nap."
    show clipi text (1) with dissolve
    show clipi talk with dissolve
    pc "I'll be back in a few hours. I'm going to take a nap."
    show clipi text (1) with dissolve
    # This ends the game.
    clipi "(sudo shutdown)"
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

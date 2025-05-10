# The script of the game goes in this file.

# Declare characters used by this game. The color argument colorizes the
# name of the character.

##define pc = Character("Slim")
define t  = Character("Terminal")

define pc = Character(_("Slim"), color="#c8ffc8")
define t = Character(_("Terminal"), color="#c8c8ff")

# The game starts here.

label start:

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
    pc "Finally!"
    t "Done."
    show terminal idle with dissolve
    show slim normal with dissolve
    pc "Time to get going."
    # This ends the game.
    pc "END."
    return

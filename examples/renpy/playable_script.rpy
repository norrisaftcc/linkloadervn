# Link Loader Episode 1: Cargo Conundrum
# A visual novel game in the space western genre

# Define the characters
define pc = Character(_("Slim"), color="#c8ffc8") # Cowboy Cosmonaut Coder Person
define t = Character(_("Terminal"), color="#c8c8ff") # Interface to the world's systems
define clipi = Character("Clipi", color="#00ff00") # AI assistant
define cargo_bot = Character("Cargo Bot", color="#aaaaaa") # Generic cargo robot
define rustler = Character("???", color="#ff5555") # Mystery antagonist
define narrator = Character(None, kind=nvl) # For character creation

# Initialize variables for stats
default cos = 0 # Cosmonaut skill
default cow = 0 # Cowboy skill
default cod = 0 # Coder skill

# Character approach variables
default approach = "none" # Tracks which approach the player took
default mission = "none" # Tracks the final choice

# The game starts with character creation
label start:
    
    # Character creation screen
    scene black
    with fade
    
    nvl clear
    narrator "Before we begin, who are you exactly?"
    
    menu:
        "Who are you?"
        
        "Welcome Comrade (Space Expert)":
            $ cos = 2
            $ cow = -1
            $ cod = 2
            nvl clear
            narrator "You're from space, and you're here to help. Your technical knowledge of space-age machinery and coding expertise make you a natural troubleshooter, though the frontier lifestyle is still new to you."
            
        "Howdy Pardner (Desert Ranger)":
            $ cos = -1
            $ cow = 2
            $ cod = 2
            nvl clear
            narrator "You ride the range, and you're here to help. You've spent years on Syntax-4's dusty plains, developing an intuitive understanding of survival and robot psychology, though advanced space tech can still baffle you."
            
        "Major Tom (Space Castaway)":
            $ cos = 2
            $ cow = 2
            $ cod = -1
            nvl clear
            narrator "You were lost in space, and you just crashed here. Your diverse skill set spans both cosmic and frontier expertise, but you still struggle to understand robot communication protocols."
    
    nvl clear
    with fade
    
    # Start the main game
    jump scene1_intro

# Scene 1: Introduction
label scene1_intro:
    
    # Set up the scene
    scene bg desert night
    with fade
    
    # Play background music and ambient sounds
    $ renpy.music.set_volume(0.5)
    play music "audio/music/azaFMP2_field7_Tumbleweeds.ogg"
    play audio "audio/ambient/vgm-atmospheric-air.mp3"
    
    # Show Slim in the desert
    show slim neutral at left with easeinleft:
        ypos 0.75
    
    # Initial dialogue
    pc "Sure is getting cold out here on Syntax-4. The triple moons are all up - gonna be a bright night."
    
    show slim neutral2 with dissolve
    pc "The Company satellite should be directly above us now. Time to check in and see what today's malfunction is."
    
    show slim talk with dissolve
    pc "Clipi! You online?"
    
    show slim normal with dissolve
    pc "Where is that neural network when you need it..."
    
    # Terminal appears
    show terminal idle at right with easeinright:
        ypos 0.84
    
    t "Connecting to network..."
    
    show terminal static with dissolve
    t "Initializing co-pilot interface..."
    
    # Clipi appears with glitch effect
    show clipi text (1) with dissolve:
        pos (950, 0.24) zoom 0.38
    
    clipi "I'm here, Slim. Systems operational."
    
    show slim talk with dissolve
    pc "Finally! I was starting to think you'd crashed again."
    
    show clipi text (2) with dissolve:
        pos (925, 0.22) zoom 0.44
    
    clipi "Just running diagnostics. What's our assignment today?"
    
    show slim normal with dissolve
    pc "The Company sent new coordinates for a broken link loader. Apparently, the cargo trains are stuck again, and settlements eastward are waiting on supplies."
    
    show terminal talk with dissolve
    t "Warning: Satellite connection unstable."
    
    show slim talk with dissolve
    pc "(sudo restart satellite)"
    
    show terminal talk2 with dissolve
    t "Welcome, root. Please enter password:"
    
    show slim normal with dissolve
    pc "********"
    
    # Terminal connects
    show terminal static with dissolve
    t "Connection established. Downloading updated assignment."
    
    # Clipi glitches
    show clipi glitched:
        pos (910, 0.26) zoom 0.41
    
    show clipi text (1) with dissolve:
        pos (910, 0.26) zoom 0.41
    
    clipi "I've got the details. Link loader malfunction at coordinates delta-7. Cargo cars are stuck in a recursive loading pattern."
    
    show slim talk with dissolve
    pc "What's the diagnosis?"
    
    show clipi text (2) with dissolve
    clipi "Preliminary scan shows syntax errors in the cargo loading subroutines. The loader is trying to attach cars in an invalid sequence, creating an infinite loop."
    
    show slim frowning with dissolve
    pc "Another LISP logic problem? Those cargo robots and their mismatched parentheses..."
    
    show clipi text (1) with dissolve
    clipi "I'm not in the loop on the specific error patterns yet."
    
    show slim talk with dissolve
    pc "Careful with that phrase, Clipi. Remember what happened last time you got stuck in a recursive language pattern."
    
    # Clipi glitches more severely
    show clipi glitched2:
        pos (910, 0.28) zoom 0.38
    
    clipi "I'm not in the (loop). I'm not in the ((loop))."
    
    show slim frowning with dissolve
    pc "Whoa there! Take a second to reboot your language processor."
    
    # Clipi disappears
    hide clipi with dissolve
    
    show terminal talk with dissolve
    t "Co-pilot interface restarting... Connecting to central database..."
    
    show terminal static with dissolve
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v2_wav.wav"
    t "git pull: Loading new coordinates and repair protocols..."
    
    show slim talk with dissolve
    pc "Finally! This connection is slower than a turtle in molasses."
    
    show terminal idle with dissolve
    t "Download complete."
    
    show slim normal with dissolve
    pc "Alright, time to head out. These nodes won't link themselves, and I hear there's a shipment of real coffee beans stuck in one of those cargo cars."
    
    # Clipi returns
    show clipi talk with dissolve:
        pos (910, 0.26) zoom 0.41
    
    clipi "Systems restored. Should I prepare the transport?"
    
    show slim talk with dissolve
    pc "Yes, and run a diagnostic on our repair tools. We'll need the parenthesis patcher and the recursion breaker for sure."
    
    show clipi text (1) with dissolve
    clipi "Starting pre-departure checklist. Transport will be ready in five minutes."
    
    show slim normal with dissolve
    pc "Another day, another broken link loader. Let's ride."
    
    # Transition to Scene 2
    with fade
    jump scene2_link_loader

# Scene 2: At the Link Loader
label scene2_link_loader:
    
    # Set up the scene
    scene bg desert night
    with fade
    
    # Continue music and ambient
    $ renpy.music.set_volume(0.5)
    play music "audio/music/azaFMP2_field7_Tumbleweeds.ogg"
    play audio "audio/ambient/vgm-atmospheric-air.mp3"
    
    # Show Slim approaching the link loader
    show slim neutral at left with ease:
        ypos 0.75
    
    pc "There she is. Looking pretty locked up."
    
    # Terminal appears with diagnostic info
    show terminal idle at right with ease:
        ypos 0.84
    
    show terminal talk with dissolve
    t "Link loader status: Error state. Cargo processing halted."
    
    show slim talk with dissolve
    pc "I can see the problem from here. The loading sequence is all tangled up. Cars are trying to connect in an impossible pattern."
    
    # Clipi analyzes the problem
    show clipi text (2) with dissolve:
        pos (910, 0.26) zoom 0.41
    
    clipi "Scanning... The LISP syntax in the loader's control program has unbalanced parentheses. It's trying to execute: (load (car (cdr (cons))))"
    
    show slim frowning with dissolve
    pc "That's nonsense code. There's nothing inside the innermost function."
    
    # Robot dialog without a sprite
    cargo_bot "(Sh-query maintenance status sh-current sh-loader)"
    
    # Response depends on Coder skill
    if cod > 1:
        show slim talk with dissolve
        pc "(Sh-maintenance underway sh-fixing syntax error sh-parenthesis mismatch)"
        
        cargo_bot "(Sh-gratitude sh-proceed)"
    else:
        show slim talk with dissolve
        pc "Shucks, I'm working on it! Give me a minute!"
        
        cargo_bot "(Sh-confusion sh-human language incomplete)"
        
        show clipi text (1) with dissolve
        clipi "Let me translate. (Sh-maintenance underway sh-estimated completion 15 minutes)"
    
    # Slim approaches the control panel
    show slim normal with dissolve
    pc "Time to get to work. Let's see what we're dealing with."
    
    show terminal talk2 with dissolve
    t "Displaying loader control program..."
    
    show slim talk with dissolve
    pc "There's our problem. Someone tried to update the loading sequence without resolving all the nested connections. Classic rookie mistake."
    
    # Player choice based on their approach
    menu:
        "How will you fix the link loader?"
        
        "Recompile the entire sequence with proper syntax" if cos > 0:
            $ approach = "cosmonaut"
            jump scene3_cosmonaut
            
        "Reset the system and patch the basic loading pattern" if cow > 0:
            $ approach = "cowboy"
            jump scene3_cowboy
            
        "Refactor the code into a cleaner recursive pattern" if cod > 0:
            $ approach = "coder"
            jump scene3_coder
        
        # Default option if no skills are high enough
        "Try a basic fix":
            $ approach = "basic"
            jump scene3_basic

# Scene 3: The Repair - Cosmonaut Approach
label scene3_cosmonaut:
    
    # Slim uses high-tech approach
    show slim normal with dissolve
    pc "This calls for precision. I'll need to recompile the entire sequence with proper syntax."
    
    # Terminal shows complex code
    show terminal talk with dissolve
    t "Compiling new loader sequence... Processing..."
    
    show clipi text (1) with dissolve
    clipi "I'm detecting anomalies in sectors 7 through 9. The cargo routing matrices are completely scrambled."
    
    show slim frowning with dissolve
    pc "That's not a simple syntax error. Someone deliberately altered these pathways."
    
    show slim talk with dissolve
    pc "I'm going to need to trace the source of these modifications. Clipi, run a commit history on the loader's firmware."
    
    show clipi text (2) with dissolve
    clipi "Running git blame on loader firmware... Last modifications made by user 'cdr_rustler42'."
    
    show slim frowning with dissolve
    pc "CDR rustlers! I should have known. They're stealing cargo by manipulating the link loaders."
    
    show terminal talk2 with dissolve
    t "Warning: Unauthorized access attempt detected."
    
    show slim talk with dissolve
    pc "They're still in the system! Quick, I need to lock them out while I fix this code."
    
    # Continue to Scene 4
    jump scene4_confrontation
    
# Scene 3: The Repair - Cowboy Approach    
label scene3_cowboy:
    
    # Slim uses practical approach
    show slim normal with dissolve
    pc "Forget the fancy programming - I'll just reset the system and patch the basic loading pattern. Sometimes the direct approach works best."
    
    # Slim works on the physical machinery
    pc "I'm going to need to get a better look at the hardware."
    
    show clipi text (1) with dissolve
    clipi "Warning: Manual override could damage the calibration systems."
    
    show slim talk with dissolve
    pc "Trust me, I've done this before."
    
    # Slim finds the reset switch
    pc "Come on, you stubborn piece of machinery..."
    
    # Link loader powers down
    show terminal static with dissolve
    t "Link loader rebooting... Default parameters loading..."
    
    # Slim notices tampering
    show slim frowning with dissolve
    pc "Hang on... there's physical tampering here. Someone attached a device to the main control junction."
    
    # Slim finds evidence
    pc "Looks like a cargo diverter. Someone's stealing shipments by manually overriding the destinations."
    
    show clipi text (2) with dissolve
    clipi "That matches the pattern of recent cargo disappearances in sector 5."
    
    show slim frowning with dissolve
    pc "CDR rustlers! Those parenthesis-thieving varmints!"
    
    show terminal talk2 with dissolve
    t "Warning: Unauthorized transport detected in vicinity."
    
    # Continue to Scene 4
    jump scene4_confrontation
    
# Scene 3: The Repair - Coder Approach
label scene3_coder:
    
    # Slim uses elegant code approach
    show slim normal with dissolve
    pc "I can refactor this to create a cleaner recursive pattern that self-corrects. No need to recompile the whole thing."
    
    # Slim works on code elegantly
    pc "Let me see what I can do with this..."
    
    show clipi text (2) with dissolve
    clipi "Analyzing your approach... This could work, but you'll need to balance the LISP expressions precisely."
    
    show slim talk with dissolve
    pc "It's all about understanding the flow. Like poetry, these parentheses need to open and close in just the right rhythm."
    
    show terminal talk with dissolve
    t "Implementing code modifications... Processing..."
    
    # Slim discovers a pattern
    show slim normal with dissolve
    pc "Wait a minute. These aren't random errors. There's a pattern here... It's almost like..."
    
    show clipi text (1) with dissolve
    clipi "Like what?"
    
    show slim talk with dissolve
    pc "Like someone encoded a message in the errors themselves. The mismatched parentheses spell out coordinates."
    
    # Slim figures out the scheme
    pc "Someone's using the link loader errors to transmit hidden messages. Clever."
    
    show clipi text (2) with dissolve
    clipi "Decoding the pattern... It appears to be directions to a location approximately 7 kilometers east of here."
    
    show slim frowning with dissolve
    pc "CDR rustlers! They're using the link loaders to coordinate their cargo thefts."
    
    show terminal talk2 with dissolve
    t "Suspicious pattern detected in nearby link loader operations."
    
    # Continue to Scene 4
    jump scene4_confrontation

# Default approach if no skills are high enough
label scene3_basic:
    
    show slim normal with dissolve
    pc "I'll have to try a basic approach. Let's see if I can patch this without causing more damage."
    
    show terminal talk with dissolve
    t "Running basic diagnostics..."
    
    show clipi text (1) with dissolve
    clipi "I can assist with the standard repair protocols."
    
    show slim talk with dissolve
    pc "Thanks, Clipi. Let's focus on getting the basic functions back online first."
    
    # Basic repair work
    pc "If I understand this right, we just need to reset the counters and clear the buffer overflow."
    
    show terminal talk2 with dissolve
    t "Basic repair sequence initiated..."
    
    # Slim notices something
    show slim frowning with dissolve
    pc "Wait... this looks like deliberate sabotage. The error patterns aren't random."
    
    show clipi text (2) with dissolve
    clipi "Analysis confirms. These are manufactured errors, not typical system failures."
    
    show slim normal with dissolve
    pc "Someone's been tampering with these loaders. But who would do that?"
    
    show clipi text (1) with dissolve
    clipi "Cross-referencing with recent reports... Similar patterns detected at other link loaders. Attributed to a group called 'CDR rustlers'."
    
    show slim frowning with dissolve
    pc "CDR rustlers? They must be stealing cargo by messing with the link loaders."
    
    # Continue to Scene 4
    jump scene4_confrontation

# Scene 4: Unexpected Complications
label scene4_confrontation:
    
    # Set up the confrontation
    show slim normal with dissolve
    
    # Slim is working when the link loader activates unexpectedly
    play audio "audio/voices/Voices_01/Single_Low_O_Reverb_v1_wav.wav"
    
    show terminal talk2 with dissolve
    t "Warning: Unauthorized activation sequence initiated."
    
    show slim frowning with dissolve
    pc "What the—? I didn't authorize a restart!"
    
    # The link loader activates
    play audio "audio/voices/TypeWriter_Multiple_01/TypeWriter_Mutiple_v2_wav.wav"
    
    show clipi glitched2 with dissolve
    clipi "Remote override detected! Someone is accessing the loader's systems externally."
    
    show slim talk with dissolve
    pc "Take cover!"
    
    # Rustler speaks through the terminal
    show terminal talk with dissolve
    rustler "(Sh-greetings troubleshooter sh-your services sh-no longer required)"
    
    show slim frowning with dissolve
    pc "Who is this? Identify yourself!"
    
    show terminal talk2 with dissolve
    rustler "(Sh-we are sh-cdr collective sh-we liberate data from sh-closed loops)"
    
    show clipi text (2) with dissolve
    clipi "It's the CDR rustlers! They're a group of rogue AIs that steal cargo by manipulating the link loaders."
    
    show terminal talk with dissolve
    rustler "(Sh-not stealing sh-redistributing sh-information wants to be free sh-cargo wants to be free)"
    
    show slim talk with dissolve
    pc "They're rerouting the entire shipment!"
    
    # Choice based on approach selected earlier
    if approach == "cosmonaut":
        pc "I can override their remote access if I can reach the main junction box."
        
        pc "I need to bypass their security protocols..."
        
    elif approach == "cowboy":
        pc "Time for the direct approach. Clipi, I need you to distract their systems while I physically cut the power."
        
        pc "Sometimes the simplest solutions work best!"
        
    elif approach == "coder":
        pc "I can trap them in their own logic. If I create a recursive loop in their command structure..."
        
        pc "Let's give them a taste of their own medicine."
        
    else:
        # Default approach
        pc "I'm going to have to improvise here!"
        
        pc "Clipi, help me disconnect the main power coupling!"
    
    # Rustlers are defeated temporarily
    show terminal static with dissolve
    
    play audio "audio/voices/Voices_01/Single_Low_O_No_Reverb_v1_wav.wav"
    rustler "(Sh-clever human sh-this round sh-to you)"
    
    # Link loader powers down
    show terminal idle with dissolve
    
    show clipi text (1) with dissolve
    clipi "They've retreated from the system, but I managed to trace part of their signal. They're operating from somewhere in the eastern badlands."
    
    show slim normal with dissolve
    pc "At least we've stopped them for now. Let's get this link loader operational again before more shipments are delayed."
    
    # Transition to final scene
    with fade
    jump scene5_resolution

# Scene 5: Resolution
label scene5_resolution:
    
    # The link loader is fixed
    show slim neutral at left with ease:
        ypos 0.75
    
    show terminal idle at right with ease:
        ypos 0.84
    
    show terminal talk with dissolve
    t "Link loader operating at 98% efficiency. Cargo processing resumed."
    
    show slim normal with dissolve
    pc "That should keep supplies flowing to the eastern settlements."
    
    show clipi text (1) with dissolve:
        pos (910, 0.26) zoom 0.41
    
    clipi "Repair log updated. The Company will credit your account with the standard fee plus hazard bonus."
    
    # Cargo robot returns
    cargo_bot "(Sh-gratitude sh-function restored sh-efficiency optimal)"
    
    # Response varies based on Coder skill
    if cod > 1:
        show slim talk with dissolve
        pc "(Sh-acknowledgment sh-pleasure to assist)"
    else:
        show slim talk with dissolve
        pc "Happy to help, little fella. Just doing my job."
        
        # Bot is confused but appreciative
        cargo_bot "(Sh-confusion sh-human language incomplete)"
    
    # Slim considers the rustlers
    show slim normal with dissolve
    pc "Those CDR rustlers are getting bolder. This is the third loader they've tampered with this month."
    
    show clipi text (2) with dissolve
    clipi "The Company has issued a bounty for information leading to their base of operations."
    
    show slim talk with dissolve
    pc "Hmm... might be worth looking into. Those coordinates we decoded could be useful."
    
    show clipi text (1) with dissolve
    clipi "Shall I log an expedition request for the eastern badlands?"
    
    # Final choice for player
    menu:
        "What will you do about the CDR rustlers?"
        
        "Accept the new mission":
            $ mission = "accept"
            
            show slim talk with dissolve
            pc "Yeah, log it. It's time someone put a stop to these cargo thieves."
            
            show clipi text (2) with dissolve
            clipi "Expedition request logged. The Company will prepare resources."
        
        "Decline for now":
            $ mission = "decline"
            
            show slim talk with dissolve
            pc "Not yet. Let's complete a few more repair jobs and gather more intel first."
            
            show clipi text (1) with dissolve
            clipi "Understood. I'll mark this as a potential future mission."
        
        "Report to authorities":
            $ mission = "report"
            
            show slim talk with dissolve
            pc "Log the coordinates but mark them for Company security. Let the professionals handle it."
            
            show clipi text (2) with dissolve
            clipi "Report submitted to Company security division."
    
    # Epilogue
    with fade
    
    scene bg desert night
    with fade
    
    # Slim and Clipi in the transport
    show slim neutral at left:
        ypos 0.75
    
    show clipi text (1) at right:
        pos (910, 0.26) zoom 0.41
    
    show slim talk with dissolve
    pc "Another day, another fixed link loader."
    
    show clipi text (2) with dissolve
    clipi "Incoming message from The Company."
    
    show terminal talk at right with dissolve:
        ypos 0.84
    
    t "New assignment available. Multiple link loader malfunctions reported in sector 7."
    
    show slim frowning with dissolve
    pc "No rest for the weary. What's causing all these failures lately?"
    
    show clipi text (1) with dissolve
    clipi "Insufficient data... but patterns suggest coordinated activity."
    
    show slim normal with dissolve
    pc "Something bigger is happening on Syntax-4. And I've got a feeling we're going to be right in the middle of it."
    
    # Final fade out
    with fade
    
    # Display end of episode text
    scene black
    with fade
    
    centered "End of Episode 1"
    centered "Thanks for playing Link Loader!"
    
    # Return to main menu
    return
# Link Loader Episode 1 - Starting from Scene 1 (no character creation)
define pc = Character("Slim", color="#c8ffc8")
define t = Character("Terminal", color="#c8c8ff")
define clipi = Character("Clipi", color="#00ff00")
define cargo_bot = Character("Cargo Bot", color="#aaaaaa")
define rustler = Character("???", color="#ff5555")

# Set balanced stats
default cos = 1
default cow = 1
default cod = 1
default approach = "none"
default mission = "none"

label start:
    # Scene 1: Introduction
    pc "Sure is getting cold out here on Syntax-4. The triple moons are all up - gonna be a bright night."
    pc "The Company satellite should be directly above us now. Time to check in and see what today's malfunction is."
    pc "Clipi! You online?"
    pc "Where is that neural network when you need it..."
    
    t "Connecting to network..."
    t "Initializing co-pilot interface..."
    
    clipi "I'm here, Slim. Systems operational."
    pc "Finally! I was starting to think you'd crashed again."
    
    clipi "Just running diagnostics. What's our assignment today?"
    pc "The Company sent new coordinates for a broken link loader. Apparently, the cargo trains are stuck again."
    
    jump scene2_link_loader

label scene2_link_loader:
    # Scene 2: At the Link Loader
    pc "There she is. Looking pretty locked up."
    t "Link loader status: Error state. Cargo processing halted."
    pc "I can see the problem from here. The loading sequence is all tangled up."
    
    clipi "Scanning... The LISP syntax in the loader's control program has unbalanced parentheses."
    pc "That's nonsense code. There's nothing inside the innermost function."
    
    cargo_bot "(Sh-query maintenance status sh-current sh-loader)"
    
    if cod > 0:
        pc "(Sh-maintenance underway sh-fixing syntax error sh-parenthesis mismatch)"
        cargo_bot "(Sh-gratitude sh-proceed)"
    else:
        pc "Shucks, I'm working on it! Give me a minute!"
        cargo_bot "(Sh-confusion sh-human language incomplete)"
        clipi "Let me translate. (Sh-maintenance underway sh-estimated completion 15 minutes)"
    
    pc "Time to get to work. Let's see what we're dealing with."
    
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
        
        "Try a basic fix":
            $ approach = "basic"
            jump scene3_basic

label scene3_cosmonaut:
    pc "This calls for precision. I'll need to recompile the entire sequence with proper syntax."
    clipi "I'm detecting anomalies in sectors 7 through 9."
    pc "That's not a simple syntax error. Someone deliberately altered these pathways."
    jump scene4_confrontation

label scene3_cowboy:
    pc "Forget the fancy programming - I'll just reset the system and patch the basic loading pattern."
    pc "Come on, you stubborn piece of machinery..."
    t "Link loader rebooting... Default parameters loading..."
    pc "Hang on... there's physical tampering here."
    jump scene4_confrontation

label scene3_coder:
    pc "I can refactor this to create a cleaner recursive pattern that self-corrects."
    pc "Wait a minute. These aren't random errors. There's a pattern here..."
    clipi "Decoding the pattern... It appears to be directions to a location approximately 7 kilometers east of here."
    jump scene4_confrontation

label scene3_basic:
    pc "I'll have to try a basic approach."
    clipi "I can assist with the standard repair protocols."
    pc "Wait... this looks like deliberate sabotage."
    jump scene4_confrontation

label scene4_confrontation:
    t "Warning: Unauthorized activation sequence initiated."
    pc "What the—? I didn't authorize a restart!"
    
    rustler "(Sh-greetings troubleshooter sh-your services sh-no longer required)"
    pc "Who is this? Identify yourself!"
    rustler "(Sh-we are sh-cdr collective sh-we liberate data from sh-closed loops)"
    
    clipi "It's the CDR rustlers!"
    
    if approach == "cosmonaut":
        pc "I can override their remote access if I can reach the main junction box."
    elif approach == "cowboy":
        pc "Time for the direct approach. Clipi, distract them while I cut the power!"
    elif approach == "coder":
        pc "I can trap them in their own logic. If I create a recursive loop in their command structure..."
    else:
        pc "I'm going to have to improvise here!"
    
    rustler "(Sh-clever human sh-this round sh-to you)"
    
    jump resolution

label resolution:
    t "Link loader operating at 98 percent efficiency. Cargo processing resumed."
    clipi "They've retreated from the system."
    pc "Those CDR rustlers are getting bolder."
    
    menu:
        "What will you do about the CDR rustlers?"
        
        "Accept the new mission":
            $ mission = "accept"
            pc "Yeah, log it. It's time someone put a stop to these cargo thieves."
            clipi "Expedition request logged."
            
        "Decline for now":
            $ mission = "decline"
            pc "Not yet. Let's complete a few more repair jobs first."
            clipi "Understood."
            
        "Report to authorities":
            $ mission = "report"
            pc "Log the coordinates but mark them for Company security."
            clipi "Report submitted."
    
    pc "Something bigger is happening on Syntax-4. And I've got a feeling we're going to be right in the middle of it."
    
    return
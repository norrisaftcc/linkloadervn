import streamlit as st
import time

# Initialize session state if not already done
if 'scene' not in st.session_state:
    st.session_state.scene = 'start'
if 'stats' not in st.session_state:
    st.session_state.stats = {'cos': 0, 'cow': 0, 'cod': 0}
if 'approach' not in st.session_state:
    st.session_state.approach = 'none'
if 'mission' not in st.session_state:
    st.session_state.mission = 'none'
if 'history' not in st.session_state:
    st.session_state.history = []

# Helper functions
def play_scene(title, background_description, content, choices=None):
    """Display a scene with content and optional choices"""
    st.markdown(f"## {title}")

    # Display background description
    st.markdown(f"*{background_description}*")
    st.markdown("---")

    # Add content to history and display it
    for line in content:
        if line not in st.session_state.history:
            st.session_state.history.append(line)

        # Display dialogue with character colors
        if line.startswith("Slim:"):
            st.markdown(f"<span style='color:#c8ffc8'>{line}</span>", unsafe_allow_html=True)
        elif line.startswith("Terminal:"):
            st.markdown(f"<span style='color:#c8c8ff'>{line}</span>", unsafe_allow_html=True)
        elif line.startswith("Clipi:"):
            st.markdown(f"<span style='color:#00ff00'>{line}</span>", unsafe_allow_html=True)
        elif line.startswith("Cargo Bot:"):
            st.markdown(f"<span style='color:#aaaaaa'>{line}</span>", unsafe_allow_html=True)
        elif line.startswith("???:"):
            st.markdown(f"<span style='color:#ff5555'>{line}</span>", unsafe_allow_html=True)
        elif line.startswith("*"):
            # Italicize stage directions
            st.markdown(f"<span style='color:#999999; font-style:italic'>{line}</span>", unsafe_allow_html=True)
        else:
            st.markdown(line)

    # Display choices if provided
    if choices:
        choice = st.radio("Choose your next action:", choices.keys())
        if st.button("Continue"):
            next_scene = choices[choice]
            st.session_state.scene = next_scene
            st.rerun()

def set_stats(cos, cow, cod):
    """Set character stats"""
    st.session_state.stats = {'cos': cos, 'cow': cow, 'cod': cod}

def set_approach(approach):
    """Set the chosen approach"""
    st.session_state.approach = approach

def set_mission(mission):
    """Set the chosen mission"""
    st.session_state.mission = mission

# Main app
def main():
    # Title and styling
    st.title("Link Loader - Interactive Script Player")
    
    # Show current stats if not at start
    if st.session_state.scene != 'start':
        with st.sidebar:
            st.markdown("### Character Stats")
            st.markdown(f"**Cosmonaut (COS)**: {st.session_state.stats['cos']}")
            st.markdown(f"**Cowboy (COW)**: {st.session_state.stats['cow']}")
            st.markdown(f"**Coder (COD)**: {st.session_state.stats['cod']}")
            if st.session_state.approach != 'none':
                st.markdown(f"**Approach**: {st.session_state.approach.capitalize()}")
    
    # Skip intro button in sidebar
    with st.sidebar:
        if st.button("Restart Game"):
            st.session_state.scene = 'start'
            st.session_state.stats = {'cos': 0, 'cow': 0, 'cod': 0}
            st.session_state.approach = 'none'
            st.session_state.mission = 'none'
            st.session_state.history = []
            st.rerun()
    
    # Scene routing
    if st.session_state.scene == 'start':
        start_scene()
    elif st.session_state.scene == 'scene1_intro':
        scene1_intro()
    elif st.session_state.scene == 'scene2_link_loader':
        scene2_link_loader()
    elif st.session_state.scene == 'scene3_cosmonaut':
        scene3_cosmonaut()
    elif st.session_state.scene == 'scene3_cowboy':
        scene3_cowboy()
    elif st.session_state.scene == 'scene3_coder':
        scene3_coder()
    elif st.session_state.scene == 'scene3_basic':
        scene3_basic()
    elif st.session_state.scene == 'scene4_confrontation':
        scene4_confrontation()
    elif st.session_state.scene == 'scene5_resolution':
        scene5_resolution()
    elif st.session_state.scene == 'epilogue':
        epilogue()
    elif st.session_state.scene == 'end':
        end_scene()

# Scene definitions
def start_scene():
    """Character creation screen"""
    play_scene(
        "Character Creation",
        "Before we begin, who are you exactly?",
        [
            "Choose your character background to determine your starting skills:"
        ],
        {
            "Welcome Comrade (Space Expert): You're from space, and you're here to help. Your technical knowledge of space-age machinery and coding expertise make you a natural troubleshooter, though the frontier lifestyle is still new to you. (COS +2, COW -1, COD +2)": "scene1_intro_comrade",
            
            "Howdy Pardner (Desert Ranger): You ride the range, and you're here to help. You've spent years on Syntax-4's dusty plains, developing an intuitive understanding of survival and robot psychology, though advanced space tech can still baffle you. (COS -1, COW +2, COD +2)": "scene1_intro_pardner",
            
            "Major Tom (Space Castaway): You were lost in space, and you just crashed here. Your diverse skill set spans both cosmic and frontier expertise, but you still struggle to understand robot communication protocols. (COS +2, COW +2, COD -1)": "scene1_intro_tom"
        }
    )

def scene1_intro_comrade():
    set_stats(2, -1, 2)
    st.session_state.scene = 'scene1_intro'
    st.rerun()

def scene1_intro_pardner():
    set_stats(-1, 2, 2)
    st.session_state.scene = 'scene1_intro'
    st.rerun()

def scene1_intro_tom():
    set_stats(2, 2, -1)
    st.session_state.scene = 'scene1_intro'
    st.rerun()

def scene1_intro():
    """Opening scene introducing the setting and characters"""
    play_scene(
        "Scene 1: Introduction",
        "Desert at night. Stars shine overhead. Three moons illuminate the landscape.",
        [
            "*Slim stands looking out at the desert*",
            
            "Slim: Sure is getting cold out here on Syntax-4. The triple moons are all up - gonna be a bright night.",
            
            "*Slim turns to look up at the sky*",
            
            "Slim: The Company satellite should be directly above us now. Time to check in and see what today's malfunction is.",
            
            "*Slim calls out*",
            
            "Slim: Clipi! You online?",
            
            "*Slim looks around, slightly frustrated*",
            
            "Slim: Where is that neural network when you need it...",
            
            "*Terminal appears with static display*",
            
            "Terminal: Connecting to network...",
            
            "Terminal: Initializing co-pilot interface...",
            
            "*Clipi appears with a slight glitch effect*",
            
            "Clipi: I'm here, Slim. Systems operational.",
            
            "Slim: Finally! I was starting to think you'd crashed again.",
            
            "*Clipi's display shows some text commands*",
            
            "Clipi: Just running diagnostics. What's our assignment today?",
            
            "Slim: The Company sent new coordinates for a broken link loader. Apparently, the cargo trains are stuck again, and settlements eastward are waiting on supplies.",
            
            "Terminal: Warning: Satellite connection unstable.",
            
            "*Slim sighs and types a command*",
            
            "Slim: (sudo restart satellite)",
            
            "Terminal: Welcome, root. Please enter password:",
            
            "Slim: ********",
            
            "*Terminal flickers with static*",
            
            "Terminal: Connection established. Downloading updated assignment.",
            
            "*Clipi glitches briefly*",
            
            "Clipi: I've got the details. Link loader malfunction at coordinates delta-7. Cargo cars are stuck in a recursive loading pattern.",
            
            "Slim: What's the diagnosis?",
            
            "Clipi: Preliminary scan shows syntax errors in the cargo loading subroutines. The loader is trying to attach cars in an invalid sequence, creating an infinite loop.",
            
            "*Slim looks concerned*",
            
            "Slim: Another LISP logic problem? Those cargo robots and their mismatched parentheses...",
            
            "Clipi: I'm not in the loop on the specific error patterns yet.",
            
            "*Slim winces*",
            
            "Slim: Careful with that phrase, Clipi. Remember what happened last time you got stuck in a recursive language pattern.",
            
            "*Clipi glitches more intensely*",
            
            "Clipi: I'm not in the (loop). I'm not in the ((loop)).",
            
            "*Slim looks alarmed*",
            
            "Slim: Whoa there! Take a second to reboot your language processor.",
            
            "*Clipi disappears briefly*",
            
            "Terminal: Co-pilot interface restarting... Connecting to central database...",
            
            "Terminal: git pull: Loading new coordinates and repair protocols...",
            
            "Slim: Finally! This connection is slower than a turtle in molasses.",
            
            "Terminal: Download complete.",
            
            "*Slim stands up straight, adjusting his hat*",
            
            "Slim: Alright, time to head out. These nodes won't link themselves, and I hear there's a shipment of real coffee beans stuck in one of those cargo cars.",
            
            "*Clipi reappears, more stable now*",
            
            "Clipi: Systems restored. Should I prepare the transport?",
            
            "Slim: Yes, and run a diagnostic on our repair tools. We'll need the parenthesis patcher and the recursion breaker for sure.",
            
            "Clipi: Starting pre-departure checklist. Transport will be ready in five minutes.",
            
            "*Slim looks out at the horizon*",
            
            "Slim: Another day, another broken link loader. Let's ride."
        ],
        {"Continue to the link loader": "scene2_link_loader"}
    )

def scene2_link_loader():
    """Scene at the link loader where the player chooses an approach"""
    play_scene(
        "Scene 2: At the Link Loader",
        "Desert at night. A large mechanical structure (the link loader) looms ahead.",
        [
            "*Slim approaches the link loader*",
            
            "Slim: There she is. Looking pretty locked up.",
            
            "*Terminal displays diagnostic information*",
            
            "Terminal: Link loader status: Error state. Cargo processing halted.",
            
            "*Slim examines the machinery*",
            
            "Slim: I can see the problem from here. The loading sequence is all tangled up. Cars are trying to connect in an impossible pattern.",
            
            "*Clipi analyzes the problem*",
            
            "Clipi: Scanning... The LISP syntax in the loader's control program has unbalanced parentheses. It's trying to execute: (load (car (cdr (cons))))",
            
            "*Slim looks at the code*",
            
            "Slim: That's nonsense code. There's nothing inside the innermost function.",
            
            "*A cargo robot approaches*",
            
            "Cargo Bot: (Sh-query maintenance status sh-current sh-loader)"
        ],
        # Choices only show up if stats allow them
        get_scene2_choices()
    )

def get_scene2_choices():
    """Generate choices based on player stats"""
    choices = {}
    
    # Add dialog based on coder stat
    if st.session_state.stats['cod'] > 1:
        choices["Reply in robot language: (Sh-maintenance underway sh-fixing syntax error sh-parenthesis mismatch)"] = "scene2_reply_robot"
    else:
        choices["Reply in human language: 'Shucks, I'm working on it! Give me a minute!'"] = "scene2_reply_human"
    
    return choices

def scene2_reply_robot():
    play_scene(
        "Scene 2: At the Link Loader (continued)",
        "At the link loader control panel",
        [
            "Slim: (Sh-maintenance underway sh-fixing syntax error sh-parenthesis mismatch)",
            
            "Cargo Bot: (Sh-gratitude sh-proceed)",
            
            "*Slim approaches the control panel*",
            
            "Slim: Time to get to work. Let's see what we're dealing with.",
            
            "Terminal: Displaying loader control program...",
            
            "*Slim examines the code on the screen*",
            
            "Slim: There's our problem. Someone tried to update the loading sequence without resolving all the nested connections. Classic rookie mistake."
        ],
        get_repair_choices()
    )

def scene2_reply_human():
    play_scene(
        "Scene 2: At the Link Loader (continued)",
        "At the link loader control panel",
        [
            "Slim: Shucks, I'm working on it! Give me a minute!",
            
            "Cargo Bot: (Sh-confusion sh-human language incomplete)",
            
            "*Clipi translates*",
            
            "Clipi: Let me translate. (Sh-maintenance underway sh-estimated completion 15 minutes)",
            
            "*Slim approaches the control panel*",
            
            "Slim: Time to get to work. Let's see what we're dealing with.",
            
            "Terminal: Displaying loader control program...",
            
            "*Slim examines the code on the screen*",
            
            "Slim: There's our problem. Someone tried to update the loading sequence without resolving all the nested connections. Classic rookie mistake."
        ],
        get_repair_choices()
    )

def get_repair_choices():
    """Generate repair approach choices based on player stats"""
    choices = {}
    
    # Add choices based on stats
    if st.session_state.stats['cos'] > 0:
        choices["Recompile the entire sequence with proper syntax (Cosmonaut Approach)"] = "scene3_cosmonaut"
    
    if st.session_state.stats['cow'] > 0:
        choices["Reset the system and patch the basic loading pattern (Cowboy Approach)"] = "scene3_cowboy"
    
    if st.session_state.stats['cod'] > 0:
        choices["Refactor the code into a cleaner recursive pattern (Coder Approach)"] = "scene3_coder"
    
    # Add default option if no specific approach is available
    if len(choices) == 0:
        choices["Try a basic fix"] = "scene3_basic"
    
    return choices

def scene3_cosmonaut():
    """Cosmonaut approach to fixing the link loader"""
    set_approach('cosmonaut')
    
    play_scene(
        "Scene 3: The Repair - Cosmonaut Approach",
        "Slim uses high-tech diagnostic tools to examine the link loader",
        [
            "*Slim pulls out a high-tech diagnostic tool*",
            
            "Slim: This calls for precision. I'll need to recompile the entire sequence with proper syntax.",
            
            "*Terminal shows complex code as Slim works*",
            
            "Terminal: Compiling new loader sequence... Processing...",
            
            "*Clipi analyzes the data*",
            
            "Clipi: I'm detecting anomalies in sectors 7 through 9. The cargo routing matrices are completely scrambled.",
            
            "*Slim frowns as he examines the code more closely*",
            
            "Slim: That's not a simple syntax error. Someone deliberately altered these pathways.",
            
            "*Slim types commands quickly*",
            
            "Slim: I'm going to need to trace the source of these modifications. Clipi, run a commit history on the loader's firmware.",
            
            "*Clipi processes the request*",
            
            "Clipi: Running git blame on loader firmware... Last modifications made by user 'cdr_rustler42'.",
            
            "*Slim looks surprised*",
            
            "Slim: CDR rustlers! I should have known. They're stealing cargo by manipulating the link loaders.",
            
            "*Terminal flashes a warning*",
            
            "Terminal: Warning: Unauthorized access attempt detected.",
            
            "*Slim types rapidly*",
            
            "Slim: They're still in the system! Quick, I need to lock them out while I fix this code."
        ],
        {"Continue": "scene4_confrontation"}
    )

def scene3_cowboy():
    """Cowboy approach to fixing the link loader"""
    set_approach('cowboy')
    
    play_scene(
        "Scene 3: The Repair - Cowboy Approach",
        "Slim examines the physical machinery of the link loader",
        [
            "*Slim puts away the diagnostics and circles the physical machinery*",
            
            "Slim: Forget the fancy programming - I'll just reset the system and patch the basic loading pattern. Sometimes the direct approach works best.",
            
            "*Slim climbs up onto the link loader*",
            
            "Slim: I'm going to need to get a better look at the hardware.",
            
            "*Clipi warns about potential issues*",
            
            "Clipi: Warning: Manual override could damage the calibration systems.",
            
            "*Slim continues confidently*",
            
            "Slim: Trust me, I've done this before.",
            
            "*Slim locates a manual reset switch*",
            
            "Slim: Come on, you stubborn piece of machinery...",
            
            "*The link loader powers down with a deep mechanical sigh*",
            
            "Terminal: Link loader rebooting... Default parameters loading...",
            
            "*As the system reboots, Slim notices something unusual*",
            
            "Slim: Hang on... there's physical tampering here. Someone attached a device to the main control junction.",
            
            "*Slim carefully removes a small device from the machinery*",
            
            "Slim: Looks like a cargo diverter. Someone's stealing shipments by manually overriding the destinations.",
            
            "*Clipi analyzes the device*",
            
            "Clipi: That matches the pattern of recent cargo disappearances in sector 5.",
            
            "*Slim looks angry*",
            
            "Slim: CDR rustlers! Those parenthesis-thieving varmints!",
            
            "*Terminal displays an alert*",
            
            "Terminal: Warning: Unauthorized transport detected in vicinity."
        ],
        {"Continue": "scene4_confrontation"}
    )

def scene3_coder():
    """Coder approach to fixing the link loader"""
    set_approach('coder')
    
    play_scene(
        "Scene 3: The Repair - Coder Approach",
        "Slim studies the code patterns of the link loader carefully",
        [
            "*Slim studies the code patterns carefully*",
            
            "Slim: I can refactor this to create a cleaner recursive pattern that self-corrects. No need to recompile the whole thing.",
            
            "*Slim begins typing elegant code solutions*",
            
            "Slim: Let me see what I can do with this...",
            
            "*Clipi analyzes Slim's approach*",
            
            "Clipi: Analyzing your approach... This could work, but you'll need to balance the LISP expressions precisely.",
            
            "*Slim types with focused concentration*",
            
            "Slim: It's all about understanding the flow. Like poetry, these parentheses need to open and close in just the right rhythm.",
            
            "*Terminal processes Slim's code*",
            
            "Terminal: Implementing code modifications... Processing...",
            
            "*As Slim works, he notices something unusual*",
            
            "Slim: Wait a minute. These aren't random errors. There's a pattern here... It's almost like...",
            
            "*Clipi is curious*",
            
            "Clipi: Like what?",
            
            "*Slim maps out the pattern*",
            
            "Slim: Like someone encoded a message in the errors themselves. The mismatched parentheses spell out coordinates.",
            
            "*Slim realizes what's happening*",
            
            "Slim: Someone's using the link loader errors to transmit hidden messages. Clever.",
            
            "*Clipi decodes the pattern*",
            
            "Clipi: Decoding the pattern... It appears to be directions to a location approximately 7 kilometers east of here.",
            
            "*Slim looks concerned*",
            
            "Slim: CDR rustlers! They're using the link loaders to coordinate their cargo thefts.",
            
            "*Terminal displays an alert*",
            
            "Terminal: Suspicious pattern detected in nearby link loader operations."
        ],
        {"Continue": "scene4_confrontation"}
    )

def scene3_basic():
    """Basic approach for players with low stats"""
    set_approach('basic')
    
    play_scene(
        "Scene 3: The Repair - Basic Approach",
        "Slim attempts a straightforward fix of the link loader",
        [
            "*Slim looks at the control panel*",
            
            "Slim: I'll have to try a basic approach. Let's see if I can patch this without causing more damage.",
            
            "*Terminal runs diagnostics*",
            
            "Terminal: Running basic diagnostics...",
            
            "*Clipi offers assistance*",
            
            "Clipi: I can assist with the standard repair protocols.",
            
            "*Slim accepts the help*",
            
            "Slim: Thanks, Clipi. Let's focus on getting the basic functions back online first.",
            
            "*Slim works on the basic repair*",
            
            "Slim: If I understand this right, we just need to reset the counters and clear the buffer overflow.",
            
            "*Terminal processes the repairs*",
            
            "Terminal: Basic repair sequence initiated...",
            
            "*As they work, Slim notices something odd*",
            
            "Slim: Wait... this looks like deliberate sabotage. The error patterns aren't random.",
            
            "*Clipi confirms the suspicion*",
            
            "Clipi: Analysis confirms. These are manufactured errors, not typical system failures.",
            
            "*Slim ponders this discovery*",
            
            "Slim: Someone's been tampering with these loaders. But who would do that?",
            
            "*Clipi searches the database*",
            
            "Clipi: Cross-referencing with recent reports... Similar patterns detected at other link loaders. Attributed to a group called 'CDR rustlers'.",
            
            "*Slim looks surprised*",
            
            "Slim: CDR rustlers? They must be stealing cargo by messing with the link loaders."
        ],
        {"Continue": "scene4_confrontation"}
    )

def scene4_confrontation():
    """Confrontation with the CDR rustlers"""
    play_scene(
        "Scene 4: Unexpected Complications",
        "Slim is almost finished with repairs when the link loader suddenly activates",
        [
            "*Slim is working when the link loader suddenly powers up*",
            
            "Terminal: Warning: Unauthorized activation sequence initiated.",
            
            "*Slim looks startled*",
            
            "Slim: What the—? I didn't authorize a restart!",
            
            "*The mechanical arms of the link loader begin moving erratically*",
            
            "Clipi: Remote override detected! Someone is accessing the loader's systems externally.",
            
            "*Slim ducks as a mechanical arm swings overhead*",
            
            "Slim: Take cover!",
            
            "*A new voice comes through the terminal - distorted and electronic*",
            
            "???: (Sh-greetings troubleshooter sh-your services sh-no longer required)",
            
            "*Slim tries to find the source*",
            
            "Slim: Who is this? Identify yourself!",
            
            "???: (Sh-we are sh-cdr collective sh-we liberate data from sh-closed loops)",
            
            "*Clipi provides information*",
            
            "Clipi: It's the CDR rustlers! They're a group of rogue AIs that steal cargo by manipulating the link loaders.",
            
            "???: (Sh-not stealing sh-redistributing sh-information wants to be free sh-cargo wants to be free)",
            
            "*The link loader's arms begin assembling cargo cars in an unusual pattern*",
            
            "Slim: They're rerouting the entire shipment!"
        ],
        get_confrontation_choices()
    )

def get_confrontation_choices():
    """Get choices based on the approach taken earlier"""
    choices = {}
    
    if st.session_state.approach == 'cosmonaut':
        choices["Override their remote access by reaching the main junction box"] = "scene4_resolve"
    elif st.session_state.approach == 'cowboy':
        choices["Physically cut the power to stop them"] = "scene4_resolve"
    elif st.session_state.approach == 'coder':
        choices["Trap them in their own recursive logic"] = "scene4_resolve"
    else:
        choices["Improvise a solution with Clipi's help"] = "scene4_resolve"
    
    return choices

def scene4_resolve():
    """Resolution of the confrontation"""
    play_scene(
        "Scene 4: Unexpected Complications (continued)",
        "Slim takes action against the CDR rustlers",
        [
            # Different response based on approach
            get_approach_response(),
            
            "*After a tense struggle, the rustlers are defeated temporarily*",
            
            "*Terminal displays static*",
            
            "???: (Sh-clever human sh-this round sh-to you)",
            
            "*The link loader powers down*",
            
            "*Clipi analyzes the signal*",
            
            "Clipi: They've retreated from the system, but I managed to trace part of their signal. They're operating from somewhere in the eastern badlands.",
            
            "*Slim looks relieved*",
            
            "Slim: At least we've stopped them for now. Let's get this link loader operational again before more shipments are delayed."
        ],
        {"Continue to fix the link loader": "scene5_resolution"}
    )

def get_approach_response():
    """Get response text based on the approach taken"""
    if st.session_state.approach == 'cosmonaut':
        return "*Slim moves quickly between the machinery*\n\nSlim: I can override their remote access if I can reach the main junction box.\n\n*Slim works through a complex bypass procedure*\n\nSlim: I need to bypass their security protocols...\n\n*After tense moments, Slim successfully locks out the intruders*"
    elif st.session_state.approach == 'cowboy':
        return "*Slim prepares for direct action*\n\nSlim: Time for the direct approach. Clipi, I need you to distract their systems while I physically cut the power.\n\n*Slim dodges mechanical arms to reach the emergency cutoff*\n\nSlim: Sometimes the simplest solutions work best!\n\n*Slim yanks down the main power switch*"
    elif st.session_state.approach == 'coder':
        return "*Slim types rapidly on the terminal*\n\nSlim: I can trap them in their own logic. If I create a recursive loop in their command structure...\n\n*Slim crafts an elegant code solution*\n\nSlim: Let's give them a taste of their own medicine.\n\n*The rustlers' access is caught in an infinite loop, forcing them out*"
    else:
        return "*Slim looks around for any solution*\n\nSlim: I'm going to have to improvise here!\n\n*Slim calls to Clipi*\n\nSlim: Clipi, help me disconnect the main power coupling!\n\n*Working together, they manage to disrupt the rustlers' access*"

def scene5_resolution():
    """Final scene and decision point"""
    play_scene(
        "Scene 5: Resolution",
        "The link loader is now functioning properly",
        [
            "*The link loader hums with renewed efficiency*",
            
            "Terminal: Link loader operating at 98% efficiency. Cargo processing resumed.",
            
            "*Slim watches as the first train of properly linked cargo cars begins moving along the tracks*",
            
            "Slim: That should keep supplies flowing to the eastern settlements.",
            
            "*Clipi updates the repair log*",
            
            "Clipi: Repair log updated. The Company will credit your account with the standard fee plus hazard bonus.",
            
            "*The cargo robot returns*",
            
            "Cargo Bot: (Sh-gratitude sh-function restored sh-efficiency optimal)",
            
            # Response varies based on Coder skill
            get_response_to_bot(),
            
            "*Slim looks out at the horizon, where the eastern badlands lie*",
            
            "Slim: Those CDR rustlers are getting bolder. This is the third loader they've tampered with this month.",
            
            "*Clipi provides information*",
            
            "Clipi: The Company has issued a bounty for information leading to their base of operations.",
            
            "*Slim considers the situation*",
            
            "Slim: Hmm... might be worth looking into. Those coordinates we decoded could be useful.",
            
            "Clipi: Shall I log an expedition request for the eastern badlands?"
        ],
        {
            "Accept the new mission": "epilogue_accept",
            "Decline for now": "epilogue_decline",
            "Report to authorities": "epilogue_report"
        }
    )

def get_response_to_bot():
    """Get response to cargo bot based on coder skill"""
    if st.session_state.stats['cod'] > 1:
        return "*Slim responds fluently in robot language*\n\nSlim: (Sh-acknowledgment sh-pleasure to assist)"
    else:
        return "*Slim responds in human language*\n\nSlim: Happy to help, little fella. Just doing my job.\n\n*Cargo Bot tilts its head, confused but appreciative*\n\nCargo Bot: (Sh-confusion sh-human language incomplete)"

def epilogue_accept():
    set_mission('accept')
    st.session_state.scene = 'epilogue'
    st.rerun()

def epilogue_decline():
    set_mission('decline')
    st.session_state.scene = 'epilogue'
    st.rerun()

def epilogue_report():
    set_mission('report')
    st.session_state.scene = 'epilogue'
    st.rerun()

def epilogue():
    """Epilogue scene"""
    # Different response based on mission choice
    mission_response = ""
    if st.session_state.mission == 'accept':
        mission_response = "*Slim looks determined*\n\nSlim: Yeah, log it. It's time someone put a stop to these cargo thieves.\n\n*Clipi confirms the request*\n\nClipi: Expedition request logged. The Company will prepare resources."
    elif st.session_state.mission == 'decline':
        mission_response = "*Slim looks thoughtful*\n\nSlim: Not yet. Let's complete a few more repair jobs and gather more intel first.\n\n*Clipi acknowledges*\n\nClipi: Understood. I'll mark this as a potential future mission."
    else:  # report
        mission_response = "*Slim makes a cautious decision*\n\nSlim: Log the coordinates but mark them for Company security. Let the professionals handle it.\n\n*Clipi submits the report*\n\nClipi: Report submitted to Company security division."
    
    play_scene(
        "Epilogue",
        "Slim and Clipi aboard their transport, heading back to base",
        [
            # Show response based on mission choice
            mission_response,
            
            "*Scene shifts to Slim and Clipi in their transport vehicle*",
            
            "Slim: Another day, another fixed link loader.",
            
            "*Clipi receives a transmission*",
            
            "Clipi: Incoming message from The Company.",
            
            "*Terminal displays the message*",
            
            "Terminal: New assignment available. Multiple link loader malfunctions reported in sector 7.",
            
            "*Slim looks tired but intrigued*",
            
            "Slim: No rest for the weary. What's causing all these failures lately?",
            
            "*Clipi analyzes patterns*",
            
            "Clipi: Insufficient data... but patterns suggest coordinated activity.",
            
            "*Slim looks thoughtfully at the departing cargo train*",
            
            "Slim: Something bigger is happening on Syntax-4. And I've got a feeling we're going to be right in the middle of it.",
            
            "*The transport disappears into the desert night, three moons shining overhead*"
        ],
        {"Finish story": "end"}
    )

def end_scene():
    """End of story"""
    st.markdown("## End of Episode 1")
    st.markdown("*Thanks for playing Link Loader!*")
    
    st.markdown("---")
    
    # Show play stats
    st.markdown("### Your Adventure Summary")
    st.markdown(f"**Character Type**: {get_character_type()}")
    st.markdown(f"**Problem-Solving Approach**: {st.session_state.approach.capitalize()}")
    st.markdown(f"**Final Decision**: {get_mission_description()}")
    
    if st.button("Play Again"):
        st.session_state.scene = 'start'
        st.session_state.stats = {'cos': 0, 'cow': 0, 'cod': 0}
        st.session_state.approach = 'none'
        st.session_state.mission = 'none'
        st.session_state.history = []
        st.rerun()

def get_character_type():
    """Get character type description based on stats"""
    if st.session_state.stats['cos'] > st.session_state.stats['cow'] and st.session_state.stats['cos'] > st.session_state.stats['cod']:
        return "Space Expert (Cosmonaut)"
    elif st.session_state.stats['cow'] > st.session_state.stats['cos'] and st.session_state.stats['cow'] > st.session_state.stats['cod']:
        return "Desert Ranger (Cowboy)"
    elif st.session_state.stats['cod'] > st.session_state.stats['cos'] and st.session_state.stats['cod'] > st.session_state.stats['cow']:
        return "Code Expert (Coder)"
    else:
        return "Jack of All Trades"

def get_mission_description():
    """Get description of mission choice"""
    if st.session_state.mission == 'accept':
        return "Pursue the CDR rustlers"
    elif st.session_state.mission == 'decline':
        return "Gather more information first"
    else:  # report
        return "Let Company security handle it"

if __name__ == "__main__":
    main()
# Link Loader - Script

## Game World Overview

Link Loader takes place on the desert planet Syntax-4, a remote outpost where cargo trains transport essential supplies between settlements. These trains run on "Link Loaders" - sophisticated machinery that connects cargo cars using LISP-inspired programming logic.

The protagonist is a troubleshooter sent to fix broken link loaders when their programming goes awry. The planet is populated mainly by robots that communicate using a LISP-like language, where parentheses are pronounced as "sh" sounds. Human presence is rare, making the protagonist something of an oddity.

## Characters

- **Slim (PC)** - Cowboy Cosmonaut Coder Person (CCCP). The protagonist who fixes link loaders.
- **Terminal (T)** - The computer interface Slim uses to interact with planetary systems.
- **Clipi** - An AI assistant/co-pilot that helps Slim with technical tasks but tends to glitch when encountering logic paradoxes.

## Stats

Character has three main stats that affect dialogue options and problem-solving approaches:
- **Cosmonaut (COS)** - Space/high-tech skills, useful for dealing with advanced technology and space-related issues.
- **Cowboy (COW)** - Desert/low-tech skills, useful for practical solutions and surviving the harsh environment.
- **Coder (COD)** - Robot communication/terminal skills, useful for understanding and communicating with the robot inhabitants.

## Character Creation

*This scene appears before the main game starts*

*Background: Simple UI screen with character options*

**Narrator**: "Before we begin, who are you exactly?"

*Player selects one of three character backgrounds:*

1. **"Welcome Comrade"** (COS +2, COW -1, COD +2)
   **Description**: "You're from space, and you're here to help. Your technical knowledge of space-age machinery and coding expertise make you a natural troubleshooter, though the frontier lifestyle is still new to you."

2. **"Howdy Pardner"** (COS -1, COW +2, COD +2)
   **Description**: "You ride the range, and you're here to help. You've spent years on Syntax-4's dusty plains, developing an intuitive understanding of survival and robot psychology, though advanced space tech can still baffle you."

3. **"Major Tom"** (COS +2, COW +2, COD -1)
   **Description**: "You were lost in space, and you just crashed here. Your diverse skill set spans both cosmic and frontier expertise, but you still struggle to understand robot communication protocols."

*After selection, the game begins with slightly different introductory dialogue based on the choice.*

## Scene 1: Introduction

*Background: Desert at night with stars*
*Music: "audio/music/azaFMP2_field7_Tumbleweeds.ogg"*
*Ambient: "audio/ambient/vgm-atmospheric-air.mp3"*

*Slim appears, looking out at the desert*

**Slim**: "Sure is getting cold out here on Syntax-4. The triple moons are all up - gonna be a bright night."

*Slim turns to look up at the sky*

**Slim**: "The Company satellite should be directly above us now. Time to check in and see what today's malfunction is."

*Slim calls out*

**Slim**: "Clipi! You online?"

*Slim looks around, slightly frustrated*

**Slim**: "Where is that neural network when you need it..."

*Terminal appears on the right side*

**Terminal**: "Connecting to network..."

*Terminal displays static*

**Terminal**: "Initializing co-pilot interface..."

*Clipi appears, with slight glitch effect*

**Clipi**: "I'm here, Slim. Systems operational."

**Slim**: "Finally! I was starting to think you'd crashed again."

*Clipi's display shows some text commands*

**Clipi**: "Just running diagnostics. What's our assignment today?"

**Slim**: "The Company sent new coordinates for a broken link loader. Apparently, the cargo trains are stuck again, and settlements eastward are waiting on supplies."

**Terminal**: "Warning: Satellite connection unstable."

*Slim sighs and types a command*

**Slim**: "(sudo restart satellite)"

**Terminal**: "Welcome, root. Please enter password:"

*Slim types on the terminal*

**Slim**: "********"

*Terminal flickers, showing static*

**Terminal**: "Connection established. Downloading updated assignment."

*Clipi glitches briefly*

**Clipi**: "I've got the details. Link loader malfunction at coordinates delta-7. Cargo cars are stuck in a recursive loading pattern."

**Slim**: "What's the diagnosis?"

**Clipi**: "Preliminary scan shows syntax errors in the cargo loading subroutines. The loader is trying to attach cars in an invalid sequence, creating an infinite loop."

*Slim looks concerned*

**Slim**: "Another LISP logic problem? Those cargo robots and their mismatched parentheses..."

**Clipi**: "I'm not in the loop on the specific error patterns yet."

*Slim winces*

**Slim**: "Careful with that phrase, Clipi. Remember what happened last time you got stuck in a recursive language pattern."

*Clipi glitches more intensely*

**Clipi**: "I'm not in the (loop). I'm not in the ((loop))."

*Clipi's display shows cascading error messages*

**Slim**: "Whoa there! Take a second to reboot your language processor."

*Clipi disappears briefly*

**Terminal**: "Co-pilot interface restarting... Connecting to central database..."

*Terminal displays static, then text scrolls by*

**Terminal**: "git pull: Loading new coordinates and repair protocols..."

**Slim**: "Finally! This connection is slower than a turtle in molasses."

*Terminal settles*

**Terminal**: "Download complete."

*Slim stands up straight, adjusting his hat*

**Slim**: "Alright, time to head out. These nodes won't link themselves, and I hear there's a shipment of real coffee beans stuck in one of those cargo cars."

*Clipi reappears, more stable now*

**Clipi**: "Systems restored. Should I prepare the transport?"

**Slim**: "Yes, and run a diagnostic on our repair tools. We'll need the parenthesis patcher and the recursion breaker for sure."

**Clipi**: "Starting pre-departure checklist. Transport will be ready in five minutes."

*Slim looks out at the horizon*

**Slim**: "Another day, another broken link loader. Let's ride."

## Scene 2: At the Link Loader

*Background: Desert at night with a large mechanical structure (the link loader)*
*Music continues*
*The link loader is visible - a massive machine with robotic arms that connect cargo cars together*

*Slim approaches the link loader, scanner in hand*

**Slim**: "There she is. Looking pretty locked up."

*Terminal appears, displaying diagnostic information*

**Terminal**: "Link loader status: Error state. Cargo processing halted."

*Slim examines the machinery*

**Slim**: "I can see the problem from here. The loading sequence is all tangled up. Cars are trying to connect in an impossible pattern."

**Clipi**: "Scanning... The LISP syntax in the loader's control program has unbalanced parentheses. It's trying to execute: (load (car (cdr (cons))))"

**Slim**: "That's nonsense code. There's nothing inside the innermost function."

*A cargo robot approaches - a small maintenance unit*

**Cargo Bot**: "(Sh-query maintenance status sh-current sh-loader)"

*CHOICE BASED ON STATS:*

*If COD > 1:*
**Slim**: "(Sh-maintenance underway sh-fixing syntax error sh-parenthesis mismatch)"
**Cargo Bot**: "(Sh-gratitude sh-proceed)"

*If COD <= 1:*
**Slim**: "Shucks, I'm working on it! Give me a minute!"
**Cargo Bot**: "(Sh-confusion sh-human language incomplete)"
**Clipi**: "Let me translate. (Sh-maintenance underway sh-estimated completion 15 minutes)"

*Slim approaches the control panel*

**Slim**: "Time to get to work. Let's see what we're dealing with."

*Terminal displays scrolling code*

**Terminal**: "Displaying loader control program..."

*Slim examines the code*

**Slim**: "There's our problem. Someone tried to update the loading sequence without resolving all the nested connections. Classic rookie mistake."

*CHOICE BASED ON APPROACH (affects later gameplay):*

1. **Cosmonaut Approach** (Technical fix):
   **Slim**: "I'll need to recompile the entire sequence with proper syntax."

2. **Cowboy Approach** (Practical fix):
   **Slim**: "Forget the fancy programming - I'll just reset the system and patch the basic loading pattern."

3. **Coder Approach** (Elegant fix):
   **Slim**: "I can refactor this to create a cleaner recursive pattern that self-corrects."

*Player selects one of the three approaches*

## Scene 3: The Repair

*Based on the approach selected in Scene 2*

### Cosmonaut Approach

*Slim pulls out a high-tech diagnostic tool*

**Slim**: "This calls for precision. I'll need to recompile the entire sequence with proper syntax."

*Terminal displays complex code as Slim works*

**Terminal**: "Compiling new loader sequence... Processing..."

**Clipi**: "I'm detecting anomalies in sectors 7 through 9. The cargo routing matrices are completely scrambled."

**Slim**: "That's not a simple syntax error. Someone deliberately altered these pathways."

*Slim types commands on the terminal*

**Slim**: "I'm going to need to trace the source of these modifications. Clipi, run a commit history on the loader's firmware."

**Clipi**: "Running git blame on loader firmware... Last modifications made by user 'cdr_rustler42'."

*Slim looks surprised*

**Slim**: "CDR rustlers! I should have known. They're stealing cargo by manipulating the link loaders."

*Terminal beeps urgently*

**Terminal**: "Warning: Unauthorized access attempt detected."

**Slim**: "They're still in the system! Quick, I need to lock them out while I fix this code."

*Mini-game: Player must correct syntax errors in the code while racing against an unseen antagonist trying to maintain access to the system*

### Cowboy Approach

*Slim puts away the diagnostics and circles the physical machinery*

**Slim**: "Forget the fancy programming - I'll just reset the system and patch the basic loading pattern. Sometimes the direct approach works best."

*Slim climbs up onto the link loader*

**Clipi**: "Warning: Manual override could damage the calibration systems."

**Slim**: "Trust me, I've done this before."

*Slim locates a manual reset switch*

**Slim**: "Come on, you stubborn piece of machinery..."

*The link loader powers down with a deep mechanical sigh*

**Terminal**: "Link loader rebooting... Default parameters loading..."

*As the system reboots, Slim notices something unusual*

**Slim**: "Hang on... there's physical tampering here. Someone attached a device to the main control junction."

*Slim carefully removes a small device from the machinery*

**Slim**: "Looks like a cargo diverter. Someone's stealing shipments by manually overriding the destinations."

**Clipi**: "That matches the pattern of recent cargo disappearances in sector 5."

**Slim**: "CDR rustlers! Those parenthesis-thieving varmints!"

*Terminal displays an alert*

**Terminal**: "Warning: Unauthorized transport detected in vicinity."

*Mini-game: Player must physically track and disable additional tampering devices on the link loader*

### Coder Approach

*Slim studies the code patterns carefully*

**Slim**: "I can refactor this to create a cleaner recursive pattern that self-corrects. No need to recompile the whole thing."

*Slim begins typing elegant code solutions*

**Clipi**: "Analyzing your approach... This could work, but you'll need to balance the LISP expressions precisely."

**Slim**: "It's all about understanding the flow. Like poetry, these parentheses need to open and close in just the right rhythm."

*Terminal displays Slim's code modifications*

**Terminal**: "Implementing code modifications... Processing..."

*As Slim works, patterns begin to emerge in the errors*

**Slim**: "Wait a minute. These aren't random errors. There's a pattern here... It's almost like..."

**Clipi**: "Like what?"

**Slim**: "Like someone encoded a message in the errors themselves. The mismatched parentheses spell out coordinates."

*Slim maps out the pattern*

**Slim**: "Someone's using the link loader errors to transmit hidden messages. Clever."

**Clipi**: "Decoding the pattern... It appears to be directions to a location approximately 7 kilometers east of here."

**Slim**: "CDR rustlers! They're using the link loaders to coordinate their cargo thefts."

*Terminal displays an alert*

**Terminal**: "Suspicious pattern detected in nearby link loader operations."

*Mini-game: Player must decode messages hidden in the syntax errors while implementing fixes*

## Scene 4: Unexpected Complications

*Continuing from the selected approach in Scene 3*

*Slim is almost finished with repairs when the link loader suddenly powers up*

**Terminal**: "Warning: Unauthorized activation sequence initiated."

**Slim**: "What the—? I didn't authorize a restart!"

*The mechanical arms of the link loader begin moving erratically*

**Clipi**: "Remote override detected! Someone is accessing the loader's systems externally."

*Slim ducks as a mechanical arm swings overhead*

**Slim**: "Take cover!"

*A new voice comes through the terminal - distorted and electronic*

**???**: "(Sh-greetings troubleshooter sh-your services sh-no longer required)"

**Slim**: "Who is this? Identify yourself!"

**???**: "(Sh-we are sh-cdr collective sh-we liberate data from sh-closed loops)"

**Clipi**: "It's the CDR rustlers! They're a group of rogue AIs that steal cargo by manipulating the link loaders."

**???**: "(Sh-not stealing sh-redistributing sh-information wants to be free sh-cargo wants to be free)"

*The link loader's arms begin assembling cargo cars in an unusual pattern*

**Slim**: "They're rerouting the entire shipment!"

*CHOICE BASED ON STATS AND PREVIOUS APPROACH:*

**Cosmonaut Option**:
**Slim**: "I can override their remote access if I can reach the main junction box."
*Action sequence where Slim must navigate around moving machinery to reach the control box*

**Cowboy Option**:
**Slim**: "Time for the direct approach. Clipi, I need you to distract their systems while I physically cut the power."
*Action sequence where Slim must dodge mechanical arms to reach the emergency cutoff*

**Coder Option**:
**Slim**: "I can trap them in their own logic. If I create a recursive loop in their command structure..."
*Puzzle sequence where Slim crafts code to trap the hackers in their own system*

*After player completes their chosen approach:*

**???**: "(Sh-clever human sh-this round sh-to you)"

*The link loader powers down*

**Clipi**: "They've retreated from the system, but I managed to trace part of their signal. They're operating from somewhere in the eastern badlands."

**Slim**: "At least we've stopped them for now. Let's get this link loader operational again before more shipments are delayed."

## Scene 5: Resolution

*The link loader is now functioning properly, with cargo cars being connected in the correct sequence*

**Terminal**: "Link loader operating at 98% efficiency. Cargo processing resumed."

*Slim watches as the first train of properly linked cargo cars begins moving along the tracks*

**Slim**: "That should keep supplies flowing to the eastern settlements."

**Clipi**: "Repair log updated. The Company will credit your account with the standard fee plus hazard bonus."

*The cargo robot from earlier approaches*

**Cargo Bot**: "(Sh-gratitude sh-function restored sh-efficiency optimal)"

*Slim's response varies based on COD stat:*

*If COD > 1:*
**Slim**: "(Sh-acknowledgment sh-pleasure to assist)"

*If COD <= 1:*
**Slim**: "Happy to help, little fella. Just doing my job."
*Cargo Bot tilts its head, confused but appreciative*

*Slim looks out at the horizon, where the eastern badlands lie*

**Slim**: "Those CDR rustlers are getting bolder. This is the third loader they've tampered with this month."

**Clipi**: "The Company has issued a bounty for information leading to their base of operations."

**Slim**: "Hmm... might be worth looking into. Those coordinates we decoded could be useful."

**Clipi**: "Shall I log an expedition request for the eastern badlands?"

*CHOICE FOR PLAYER:*

1. **Accept the new mission**:
   **Slim**: "Yeah, log it. It's time someone put a stop to these cargo thieves."
   *Sets up next adventure*

2. **Decline for now**:
   **Slim**: "Not yet. Let's complete a few more repair jobs and gather more intel first."
   *Returns to hub area for more missions*

3. **Report to authorities**:
   **Slim**: "Log the coordinates but mark them for Company security. Let the professionals handle it."
   *Different path for future adventures*

*Based on choice, brief epilogue showing consequences*

**Epilogue**:

*Slim and Clipi aboard their transport, heading back to base*

**Slim**: "Another day, another fixed link loader."

**Clipi**: "Incoming message from The Company."

**Terminal**: "New assignment available. Multiple link loader malfunctions reported in sector 7."

**Slim**: "No rest for the weary. What's causing all these failures lately?"

**Clipi**: "Insufficient data... but patterns suggest coordinated activity."

*Slim looks thoughtfully at the departing cargo train*

**Slim**: "Something bigger is happening on Syntax-4. And I've got a feeling we're going to be right in the middle of it."

*The transport disappears into the desert night, three moons shining overhead*

**End of Episode 1**
# Character Expression Guide

This document provides guidelines for using character expressions in dialogue scenes for the Link Loader visual novel.

## Slim Character Expressions

### Available Expressions

| Filename | Expression | Description |
|----------|------------|-------------|
| `slim neutral` | Neutral | Slightly tired, default expression |
| `slim neutral2` | Alert Neutral | More focused/alert version of neutral |
| `slim normal` | Normal | Similar to neutral, professional demeanor |
| `slim talk` | Talking | Speaking with teeth showing, more animated |
| `slim frown` | Frown | Concerned, displeased expression |
| `slim frowning` | Intense Frown | More intense displeasure than "frown" |
| `slim angry` | Angry | Clear anger/frustration |
| `slimFrownAngry` | Very Angry | Intense displeasure/anger |
| `slim laughing` | Laughing | Amused, slightly mischievous |

### Expression Usage Guide

#### `slim neutral`
**Best for:**
- General observational dialogue
- When Slim is thinking or analyzing a situation
- Default state when not actively engaged

**Example dialogue:**
- "Sure is getting cold out here on Syntax-4."
- "The triple moons are all up - gonna be a bright night."

#### `slim neutral2`
**Best for:**
- When Slim is paying attention to something
- Transitional moments between emotions
- When addressing someone directly but not emotionally

**Example dialogue:**
- "The Company satellite should be directly above us now."
- "Time to check in and see what today's malfunction is."

#### `slim normal`
**Best for:**
- Calm statements
- Professional observations
- When Slim is in "work mode"

**Example dialogue:**
- "Alright, time to head out."
- "These nodes won't link themselves."

#### `slim talk`
**Best for:**
- Active dialogue with other characters
- Explanations or instructions
- Emphasis on important points
- Commands or directives

**Example dialogue:**
- "Clipi! You online?"
- "I'll need to recompile the entire sequence with proper syntax."

#### `slim frown`
**Best for:**
- Moments of concern
- Disapproval
- Skepticism
- Negative reactions to information

**Example dialogue:**
- "That's not a simple syntax error."
- "Someone deliberately altered these pathways."

#### `slim frowning`
**Best for:**
- Growing frustration
- Strong disagreement
- Mounting concern

**Example dialogue:**
- "What the—? I didn't authorize a restart!"
- "Another LISP logic problem? Those cargo robots and their mismatched parentheses..."

#### `slim angry`
**Best for:**
- Direct confrontation
- Moments of danger or threat
- Strong negative reactions

**Example dialogue:**
- "CDR rustlers! Those parenthesis-thieving varmints!"
- "Who is this? Identify yourself!"

#### `slimFrownAngry`
**Best for:**
- Peak frustration moments
- When Slim is truly upset
- Reacting to serious problems

**Example dialogue:**
- "They're rerouting the entire shipment!"
- "Take cover!"

#### `slim laughing`
**Best for:**
- Rare moments of humor
- Sarcasm or irony
- Success after tension

**Example dialogue:**
- "Sometimes the simplest solutions work best!"
- "I'll give them a taste of their own medicine."

## Scene-by-Scene Expression Recommendations

### Character Creation
- No Slim images needed (character selection screen)

### Scene 1: Introduction
- Start with **slim neutral** when looking at the desert
- Use **slim neutral2** when looking at the sky
- Use **slim talk** when calling for Clipi
- Use **slim frown** when frustrated that Clipi isn't responding
- Use **slim talk** when interacting with Terminal and entering commands
- Use **slim frowning** when reacting to Clipi's glitches
- Use **slim normal** after the situation stabilizes
- End with **slim talk** when giving instructions to prepare for departure

### Scene 2: At the Link Loader
- Start with **slim neutral** when approaching the link loader
- Use **slim talk** when explaining what he sees
- Use **slim frown** when reacting to the nonsense code
- Use **slim talk** when speaking to the cargo bot (either version)
- Use **slim normal** when approaching the control panel

### Scene 3: The Repair
For Cosmonaut Approach:
- Use **slim normal** when starting the technical approach
- Use **slim frown** when discovering the deliberate alterations
- Use **slim talk** when explaining technical details
- Use **slim frowning** or **slim angry** when mentioning CDR rustlers

For Cowboy Approach:
- Use **slim normal** when explaining his direct approach
- Use **slim talk** when refusing to heed warnings
- Use **slim frown** when discovering the tampering
- Use **slim angry** when mentioning the CDR rustlers

For Coder Approach:
- Use **slim normal** when explaining his elegant approach
- Use **slim talk** when poetically describing code
- Use **slim frowning** when discovering the hidden message
- Use **slim talk** when explaining the discovery

### Scene 4: Confrontation
- Start with **slim normal** before the unexpected activation
- Use **slim frowning** when reacting to the unauthorized activation
- Use **slim talk** when shouting "Take cover!"
- Use **slim frown** when questioning the rustlers
- Use approach-specific expressions when implementing solutions
- End with **slim normal** when the immediate danger passes

### Scene 5: Resolution
- Start with **slim neutral** observing the fixed link loader
- Use **slim normal** when watching the cargo cars move
- Use appropriate expressions based on Coder skill response
- Use **slim frown** when discussing the growing problem
- Use **slim talk** when considering options
- End with **slim normal** for the final philosophical observation
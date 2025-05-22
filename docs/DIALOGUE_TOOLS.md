# Link Loader Dialogue Tools

This directory contains tools for creating and playing dialogue trees (conversation trees) for the Link Loader visual novel.

## Dialogue Format

The dialogue trees are stored in a JSON format inspired by Twine's TWEE format. This format allows for:

- Branching conversations with choices
- Variable tracking throughout the dialogue
- Conditional logic for dialogue paths
- Effects that modify variables based on choices
- Rich formatting including speaker identification and robot language styling

The full schema is defined in `dialogue_schema.json`.

## Available Tools

### 1. Console Dialogue Player

A command-line tool for playing dialogue trees with interactive choices.

**Usage:**
```bash
# Play a dialogue file
./dialogue_player.py sample_dialogue.json

# Options
./dialogue_player.py sample_dialogue.json --speed 0.02  # Adjust typing speed
./dialogue_player.py sample_dialogue.json --no-typing   # Disable typing animation
```

**Features:**
- Colored text for different characters
- Special formatting for robot language
- Typing animation effect
- Interactive choice selection
- Variable tracking and conditional paths
- History tracking

### 2. Streamlit Dialogue Player

A web-based interface for playing dialogue trees with a more visual presentation.

**Usage:**
```bash
# Start the Streamlit app
streamlit run dialogue_streamlit.py
```

**Features:**
- Interactive web UI
- Upload dialogue files or use samples
- Visual styling for different characters
- Choice buttons for easy navigation
- Variable inspection for debugging
- Auto-advance option for non-choice nodes
- Debug mode with detailed information
- Reset and control options

### 3. Unit Tests

A suite of tests to ensure the dialogue player functions correctly.

**Usage:**
```bash
# Run all tests
python -m unittest test_dialogue_player.py

# Run a specific test
python -m unittest test_dialogue_player.TestDialoguePlayer.test_evaluate_condition_true
```

## Creating Dialogue Files

Dialogue files are JSON documents that follow the dialogue schema. Here's a simple example:

```json
{
  "title": "Simple Conversation",
  "default_speaker": "Slim",
  "variables": {
    "friendliness": 0
  },
  "start": "greeting",
  "nodes": {
    "greeting": {
      "content": "Hello there! How are you today?",
      "choices": [
        {
          "text": "I'm doing well, thanks for asking!",
          "next": "friendly_response",
          "effects": [
            {
              "type": "inc",
              "variable": "friendliness",
              "value": 1
            }
          ]
        },
        {
          "text": "Mind your own business.",
          "next": "unfriendly_response",
          "effects": [
            {
              "type": "dec",
              "variable": "friendliness",
              "value": 1
            }
          ]
        }
      ]
    },
    "friendly_response": {
      "content": "Glad to hear it! It's a beautiful day, isn't it?",
      "next": "weather"
    },
    "unfriendly_response": {
      "content": "Well, excuse me for being polite.",
      "next": "weather"
    },
    "weather": {
      "content": "The weather on Syntax-4 is always unpredictable.",
      "choices": [
        {
          "text": "I like the variety.",
          "next": "end_friendly",
          "condition": "friendliness >= 0"
        },
        {
          "text": "It's terrible. Just like this conversation.",
          "next": "end_unfriendly",
          "condition": "friendliness < 0"
        }
      ]
    },
    "end_friendly": {
      "content": "Me too. Well, I'd better get back to work. See you around!",
      "next": null
    },
    "end_unfriendly": {
      "content": "Fine, I'm leaving. Have a nice day... or don't.",
      "next": null
    }
  }
}
```

### Key Components

1. **Metadata**: Title, author, version, and default speaker
2. **Variables**: Initial state variables for tracking dialogue state
3. **Start**: The ID of the first node in the dialogue
4. **Nodes**: The individual dialogue steps, each with:
   - Content (the text spoken)
   - Speaker (who is speaking)
   - Choices (branching options)
   - Effects (changes to variables)
   - Conditions (for when choices appear)

### Robot Language

The dialogue system supports special formatting for the robot language used in Link Loader, where parentheses are pronounced as "sh" sounds:

```
(Sh-query maintenance status sh-current sh-loader)
```

This will be automatically highlighted in the players to make it visually distinct.

## Integration with Ren'Py

While these tools are designed for standalone development and testing of dialogue trees, they can be integrated with Ren'Py:

1. **Development Workflow**:
   - Draft dialogues using the Streamlit player
   - Test interactions and variables
   - Export to a format compatible with Ren'Py

2. **Conversion**:
   - A future update will include a converter for Ren'Py format
   - The JSON format is designed to be easily mapped to Ren'Py syntax

## Advanced Features

### Conditional Logic

Dialogue choices can be conditional based on variables:

```json
{
  "text": "Speak in robot language",
  "condition": "cod >= 2",
  "next": "robot_response"
}
```

### Effects

Various effects can modify variables:

```json
"effects": [
  {
    "type": "set",
    "variable": "knows_about_rustlers",
    "value": true
  },
  {
    "type": "inc",
    "variable": "robot_trust",
    "value": 1
  }
]
```

### Entry and Exit Actions

Nodes can have effects that trigger when entering or exiting:

```json
"onentry": [
  {
    "type": "set",
    "variable": "location",
    "value": "desert"
  }
],
"onexit": [
  {
    "type": "inc",
  "variable": "locations_visited",
  "value": 1
  }
]
```

## Future Improvements

Planned enhancements include:

1. Visual dialogue editor in Streamlit
2. Ren'Py script converter
3. Dialogue validation tools
4. Visualization of dialogue trees as graphs
5. Support for audio and images in the web player
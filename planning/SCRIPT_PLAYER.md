# Link Loader Script Player Options

This document explains how to test the Link Loader story without using the full Ren'Py engine.

## Available Options

### 1. Streamlit Script Player

The `script_streamlit.py` file contains a complete interactive version of the story that runs in Streamlit.

**Setup:**
1. Install Streamlit: `pip install streamlit`
2. Run the script: `streamlit run script_streamlit.py`
3. The interactive story will open in your web browser

**Features:**
- Tracks character stats (Cosmonaut, Cowboy, Coder)
- Shows different choices based on stats
- Maintains history of all dialogue
- Visual styling for different characters
- Tracks progress through the story
- Provides a summary at the end

**Development:**
- New scenes can be added as functions
- Easy to modify text and choices
- Stats and variables are stored in session state

### 2. Twine Export

The `twine_export.html` file provides a template for creating a Twine version of the story.

**To use with Twine:**
1. Install Twine 2 from [twinery.org](https://twinery.org/)
2. Create a new story
3. Use the content from the `script.md` file to create passages
4. Use the styling examples from the HTML file for visual formatting
5. Create variables to track stats and decisions

**Advantages of Twine:**
- No coding required
- Built-in saving and state management
- Easy to share as a playable HTML file
- Support for styling and custom scripting

## Converting Back to Ren'Py

After testing and refining the story using the script player:

1. Use the `playable_script.rpy` as a basis
2. Copy any story changes from the script player back to the Ren'Py script
3. Test in the Ren'Py engine
4. Add additional visual effects, animations, and audio

## Recommended Development Workflow

1. **Narrative First**: Edit `script.md` to get the story and dialogue right
2. **Quick Testing**: Use the Streamlit player to test flow and choices
3. **Visual Design**: Create a Twine version for testing visual presentation
4. **Full Implementation**: Update the Ren'Py script with final content

This approach allows for rapid iteration on the story without waiting for the full Ren'Py engine to compile and run.
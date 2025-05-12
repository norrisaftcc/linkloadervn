# Link Loader Script Development Tools

This directory contains tools for developing and managing the Link Loader visual novel script outside of the Ren'Py engine.

## Available Tools

### 1. Script Editor (Streamlit)

The script editor is a web-based tool for editing and managing your script in a structured JSON format.

**Setup:**
```bash
# Install requirements
pip install streamlit

# Run the script editor
cd /Users/norrisa/Documents/dev/github/linkloadervn
streamlit run planning/script_editor.py
```

**Features:**
- Edit characters, stats, and variables
- Create and edit scenes with dialogue
- Convert between formats (JSON to Ren'Py, Markdown)
- Validate script consistency
- Visual editing interface

### 2. Script Validation Tool

This tool checks the consistency between your JSON script data and Ren'Py script files to ensure they stay in sync.

**Usage:**
```bash
# Basic validation
python planning/validate_script.py

# Custom paths
python planning/validate_script.py --json path/to/script_data.json --renpy path/to/script.rpy path/to/another_script.rpy

# Strict mode (exit with error code on warnings)
python planning/validate_script.py --strict
```

### 3. Script Conversion Tool

This tool converts between different script formats.

**Usage:**
```bash
# Convert JSON to Ren'Py
python planning/convert_script.py --input planning/script_data.json --output planning/generated_script.rpy --format json2renpy

# Convert Ren'Py to JSON
python planning/convert_script.py --input planning/playable_script.rpy --output planning/extracted_script.json --format renpy2json

# Convert JSON to Markdown
python planning/convert_script.py --input planning/script_data.json --output planning/script.md --format json2md

# Convert Ren'Py to JSON with base template
python planning/convert_script.py --input planning/playable_script.rpy --output planning/extracted_script.json --format renpy2json --base planning/script_data.json
```

## Script Formats

### JSON Format

The JSON format is the central representation used by the script editor. It contains:

- Metadata (title, version)
- Character definitions
- Stats definitions
- Game variables
- Scenes with dialogue and choices

This format is designed to be easily edited and validated.

### Ren'Py Format

The Ren'Py format is the actual script used by the game engine. The converters ensure that:

- All characters are properly defined
- Stats and variables are initialized
- Scenes are converted to labels
- Dialogue and choices are formatted correctly

### Markdown Format

The Markdown format is designed for easier reading and narrative-focused editing. It's a human-readable script format that highlights dialogue and scene structure.

## Recommended Workflow

1. **Edit in Script Editor** - Use the Streamlit script editor for most changes
2. **Test in Streamlit Player** - Test your script changes in the Streamlit player
3. **Convert to Ren'Py** - Convert your JSON script to Ren'Py format
4. **Test in Ren'Py** - Launch the game in Ren'Py to test with full visuals and audio
5. **Validate Changes** - Run the validation tool to ensure consistency

## Script Data Files

- `script_data.json` - The main JSON script data
- `script_schema.json` - JSON schema defining the structure
- `generated_script.rpy` - Generated Ren'Py script
- `script.md` - Markdown version of the script

## Advanced Features

### Interactive Scene Development

To develop a scene interactively:

1. Open the Script Editor
2. Create a new scene
3. Add dialogue and choices
4. Test the scene in the Streamlit player
5. Convert to Ren'Py and test in the engine

### Batch Processing

For batch conversions between formats:

```bash
# Convert all scripts in a directory
for file in planning/*.json; do
  python planning/convert_script.py --input "$file" --output "${file%.json}.rpy" --format json2renpy
done
```

### Integration with Version Control

Since the JSON format is structured and stable, it works well with version control systems:

```bash
# Track script changes
git diff planning/script_data.json

# Resolve merge conflicts
git mergetool planning/script_data.json
```
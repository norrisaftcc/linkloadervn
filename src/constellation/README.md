# Constellation Engine ⭐

A lightweight, web-native visual novel engine designed specifically for LinkLoader and similar narrative games.

## Features

### Core Engine
- **Pure Web Technologies**: HTML5, CSS3, JavaScript ES6+ - no external dependencies
- **Cross-Platform**: Runs anywhere with a modern web browser
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Performance Optimized**: Lightweight and fast-loading

### Visual Novel Features
- **JSON-Based Story Format**: Easy to write and version control
- **Typewriter Effect**: Configurable text animation speed
- **Character Sprites**: Support for character positioning and animations
- **Background Images**: Scene-based background management
- **Branching Dialogue**: Choice-driven narrative with conditional logic
- **Game State Management**: Variables, history, and save/load system

### LinkLoader Theme
- **Sci-Fi/Western Aesthetic**: Custom CSS themes for the space cowboy setting
- **Terminal-Style UI**: Monospace fonts and green-on-black color scheme
- **LISP Integration**: Support for parenthetical robot dialogue
- **Glitch Effects**: Built-in visual effects for malfunctioning characters

## Quick Start

### Try the Examples
1. Open `examples/index.html` in your browser
2. Choose from 5 different story types:
   - **LinkLoader Demo**: Classic space western adventure
   - **Neon Isekai**: Character creation with dual personalities
   - **Terminal Mystery**: Cyberpunk detective investigation
   - **Connection Protocol**: Human-AI romance story
   - **The Night Museum**: Belonging and memory in a transforming museum

### Basic Usage

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="ui/constellation.css">
</head>
<body>
    <div id="game"></div>
    
    <script type="module">
        import { ConstellationEngine } from 'core/engine.js';
        
        const engine = new ConstellationEngine('#game');
        const story = await fetch('story.json').then(r => r.json());
        await engine.loadStory(story);
    </script>
</body>
</html>
```

### Story Format

```json
{
  "title": "My Story",
  "startScene": "opening",
  "scenes": {
    "opening": {
      "background": "images/desert.jpg",
      "characters": [
        {"name": "slim", "sprite": "images/slim.png", "position": "center"}
      ],
      "dialogue": [
        {"speaker": "slim", "text": "Well, howdy there, partner!"}
      ],
      "choices": [
        {"text": "Howdy!", "goto": "friendly_response"},
        {"text": "Who are you?", "goto": "suspicious_response"}
      ]
    }
  }
}
```

## Architecture

```
constellation/
├── core/
│   └── engine.js          # Main engine class
├── ui/
│   └── constellation.css  # Core styles and themes
├── audio/                 # Audio management (future)
├── storage/              # Save/load system (future)
├── minigames/            # Interactive mini-games (future)
└── examples/
    ├── index.html              # Story showcase and launcher
    ├── player.html             # Universal story player
    ├── demo_story.json         # Original LinkLoader demo
    ├── character_creation.json # Neon Isekai character creation
    ├── terminal_mystery.json   # Cyberpunk detective story
    ├── ai_romance.json         # Human-AI relationship story
    ├── night_museum.json       # Museum spirits and memory fragments
    └── demo.html              # Legacy single-story demo
```

## Story Format Reference

### Scene Structure
```json
{
  "background": "path/to/background.jpg",
  "characters": [
    {
      "name": "character_name",
      "sprite": "path/to/sprite.png",
      "position": "left|center|right"
    }
  ],
  "dialogue": [
    {
      "speaker": "character_name|narrator",
      "text": "Dialogue text here"
    }
  ],
  "choices": [
    {
      "text": "Choice text",
      "goto": "scene_id",
      "condition": {"variable": "value"},
      "set": {"variable": "new_value"}
    }
  ]
}
```

### Advanced Features
- **Conditional Choices**: Show choices based on game state
- **Variable Management**: Track player decisions and story state  
- **Scene Transitions**: Smooth fading between scenes
- **Character Animations**: CSS-based sprite animations
- **Audio Integration**: Background music and sound effects (planned)

## Development Roadmap

### Sprint 1 - Foundation ✅
- [x] Core engine architecture
- [x] Basic dialogue system
- [x] Choice/branching system
- [x] CSS styling and themes

### Sprint 2 - Polish (In Progress)
- [ ] Audio system integration
- [ ] Save/load functionality
- [ ] Visual effects and transitions
- [ ] Mobile optimization

### Sprint 3 - Advanced Features (Planned)
- [ ] Mini-game framework
- [ ] Character animation system
- [ ] Story conversion tools
- [ ] Performance optimization

## Contributing

This engine is being developed as part of the LinkLoader project. See the main project documentation for contribution guidelines.

## License

Same as LinkLoader project - see main LICENSE file.
#!/bin/bash

# Constellation Engine Demo Startup Script

echo "🌟 Starting Constellation Engine Demo..."
echo ""

# Find the script directory (should be constellation/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to constellation directory (parent of examples, ui, core)
cd "$SCRIPT_DIR" || {
    echo "❌ Error: Could not find constellation directory at $SCRIPT_DIR"
    exit 1
}

# Find available port
PORT=8080
while lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; do
    PORT=$((PORT + 1))
done

echo "🚀 Starting server on port $PORT..."
echo ""
echo "📖 Available Stories:"
echo "  1. LinkLoader Demo (demo_story.json)"
echo "  2. Neon Isekai Character Creation (character_creation.json)"  
echo "  3. Terminal Mystery (terminal_mystery.json)"
echo "  4. Connection Protocol (ai_romance.json)"
echo "  5. The Night Museum (night_museum.json)"
echo "  6. Corporate Extraction (netrunner_heist.json)"
echo "  7. First Light - Neon Taxidermy Intro (neon_taxidermy_intro.json)"
echo ""
echo "🌐 Open in browser:"
echo "  Main Menu: http://localhost:$PORT/examples/index.html"
echo "  Direct Neon Taxidermy: http://localhost:$PORT/examples/player.html?story=neon_taxidermy_intro.json"
echo ""
echo "⌨️  Keyboard shortcuts: Press 1-7 on main page to jump to stories"
echo ""
echo "🛑 To stop: Press Ctrl+C"
echo ""

# Start server
python -m http.server $PORT
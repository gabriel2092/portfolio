#!/bin/bash
# Start script for the backend server

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Error: .env file not found!"
    echo "Please copy .env.example to .env and add your ANTHROPIC_API_KEY"
    exit 1
fi

# Check if ANTHROPIC_API_KEY is set
if ! grep -q "ANTHROPIC_API_KEY=sk-" .env 2>/dev/null; then
    echo "Warning: ANTHROPIC_API_KEY may not be configured in .env"
    echo "Please ensure you have a valid Anthropic API key"
fi

echo "Starting Clinical Trial Matcher API..."
python main.py

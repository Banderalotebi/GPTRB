#!/bin/bash

# Llama 3.1/3.2 Quick Setup Script
# This script sets up everything you need to run Llama models locally

echo "🦙 Llama 3.1/3.2 Setup Script"
echo "================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

echo "✅ Python 3 found"

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo "📥 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    
    # Start Ollama service
    echo "🚀 Starting Ollama service..."
    ollama serve &
    sleep 5
else
    echo "✅ Ollama is already installed"
    
    # Check if Ollama is running
    if ! pgrep -x "ollama" > /dev/null; then
        echo "🚀 Starting Ollama service..."
        ollama serve &
        sleep 5
    fi
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Quick Start Options:"
echo "1. Run setup tool:     python3 llama_setup.py"
echo "2. Test API:          python3 llama_api.py"
echo "3. Try examples:      python3 llama_examples.py"
echo ""
echo "📋 Recommended models to download:"
echo "  - llama3.2:1b   (Fast, 1.3GB)"
echo "  - llama3.2:3b   (Balanced, 2.0GB)"
echo "  - llama3.1:8b   (High quality, 4.7GB)"
echo ""
echo "💡 Download a model with: ollama pull llama3.2:3b"

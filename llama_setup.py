#!/usr/bin/env python3
"""
Llama 3.1/3.2 Setup and Usage Script
This script helps you download, setup, and use Llama models locally.
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

class LlamaSetup:
    def __init__(self):
        self.models = {
            "llama3.2:1b": "Llama 3.2 1B - Fastest, good for testing",
            "llama3.2:3b": "Llama 3.2 3B - Balanced speed and quality",
            "llama3.1:8b": "Llama 3.1 8B - High quality, reasonable speed",
            "llama3.1:70b": "Llama 3.1 70B - Highest quality, requires more resources",
            "llama3.1:405b": "Llama 3.1 405B - State-of-the-art, requires significant resources"
        }
        
    def check_ollama_installed(self):
        """Check if Ollama is installed"""
        try:
            result = subprocess.run(['ollama', '--version'], 
                                 capture_output=True, text=True)
            return result.returncode == 0
        except FileNotFoundError:
            return False
    
    def install_ollama(self):
        """Install Ollama on Linux"""
        print("Installing Ollama...")
        try:
            # Download and install Ollama
            subprocess.run([
                'curl', '-fsSL', 'https://ollama.com/install.sh'
            ], check=True, stdout=subprocess.PIPE)
            
            subprocess.run([
                'sh', '-c', 'curl -fsSL https://ollama.com/install.sh | sh'
            ], check=True)
            
            print("✅ Ollama installed successfully!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Ollama: {e}")
            return False
    
    def list_available_models(self):
        """List available Llama models"""
        print("\n🦙 Available Llama Models:")
        print("=" * 50)
        for model, description in self.models.items():
            print(f"{model:<20} - {description}")
        print()
    
    def download_model(self, model_name):
        """Download a specific Llama model"""
        if model_name not in self.models:
            print(f"❌ Model {model_name} not found in available models")
            return False
            
        print(f"📥 Downloading {model_name}...")
        print("This may take a while depending on model size and internet speed...")
        
        try:
            result = subprocess.run([
                'ollama', 'pull', model_name
            ], check=True, capture_output=True, text=True)
            
            print(f"✅ Successfully downloaded {model_name}!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to download {model_name}: {e}")
            return False
    
    def list_installed_models(self):
        """List locally installed models"""
        try:
            result = subprocess.run([
                'ollama', 'list'
            ], capture_output=True, text=True, check=True)
            
            print("\n🔧 Installed Models:")
            print("=" * 30)
            print(result.stdout)
        except subprocess.CalledProcessError:
            print("❌ Could not list installed models")
    
    def chat_with_model(self, model_name, prompt=None):
        """Start an interactive chat with a model"""
        if not prompt:
            print(f"\n💬 Starting interactive chat with {model_name}")
            print("Type 'exit' to quit, 'clear' to clear context\n")
            
            try:
                subprocess.run(['ollama', 'run', model_name], check=True)
            except subprocess.CalledProcessError:
                print(f"❌ Could not start chat with {model_name}")
        else:
            # Single prompt mode
            try:
                result = subprocess.run([
                    'ollama', 'run', model_name, prompt
                ], capture_output=True, text=True, check=True)
                
                return result.stdout.strip()
            except subprocess.CalledProcessError as e:
                print(f"❌ Error running prompt: {e}")
                return None

def main():
    setup = LlamaSetup()
    
    print("🦙 Llama 3.1/3.2 Setup Tool")
    print("=" * 40)
    
    # Check if Ollama is installed
    if not setup.check_ollama_installed():
        print("Ollama not found. Installing...")
        if not setup.install_ollama():
            print("Failed to install Ollama. Please install manually.")
            sys.exit(1)
    else:
        print("✅ Ollama is already installed")
    
    # Show available models
    setup.list_available_models()
    
    # Show installed models
    setup.list_installed_models()
    
    # Interactive menu
    while True:
        print("\nWhat would you like to do?")
        print("1. Download a model")
        print("2. Chat with a model")
        print("3. List installed models")
        print("4. Exit")
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            setup.list_available_models()
            model = input("Enter model name to download: ").strip()
            setup.download_model(model)
            
        elif choice == '2':
            setup.list_installed_models()
            model = input("Enter model name to chat with: ").strip()
            setup.chat_with_model(model)
            
        elif choice == '3':
            setup.list_installed_models()
            
        elif choice == '4':
            print("Goodbye! 👋")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

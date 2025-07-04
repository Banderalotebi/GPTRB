"""
Llama API Interface
Provides a Python API for working with Llama models via Ollama
"""

import requests
import json
from typing import Dict, List, Optional, Generator

class LlamaAPI:
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    def generate(self, model: str, prompt: str, stream: bool = False, **kwargs) -> Dict:
        """Generate text using a Llama model"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream,
            **kwargs
        }
        
        if stream:
            return self._stream_generate(url, payload)
        else:
            response = requests.post(url, json=payload)
            return response.json()
    
    def _stream_generate(self, url: str, payload: Dict) -> Generator[Dict, None, None]:
        """Stream generation responses"""
        with requests.post(url, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    yield json.loads(line.decode('utf-8'))
    
    def chat(self, model: str, messages: List[Dict], stream: bool = False, **kwargs) -> Dict:
        """Chat with a Llama model using conversation format"""
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream,
            **kwargs
        }
        
        if stream:
            return self._stream_generate(url, payload)
        else:
            response = requests.post(url, json=payload)
            return response.json()
    
    def list_models(self) -> List[Dict]:
        """List available models"""
        url = f"{self.base_url}/api/tags"
        response = requests.get(url)
        return response.json().get('models', [])
    
    def show_model_info(self, model: str) -> Dict:
        """Get information about a specific model"""
        url = f"{self.base_url}/api/show"
        payload = {"name": model}
        response = requests.post(url, json=payload)
        return response.json()
    
    def pull_model(self, model: str) -> Generator[Dict, None, None]:
        """Pull/download a model"""
        url = f"{self.base_url}/api/pull"
        payload = {"name": model}
        
        with requests.post(url, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    yield json.loads(line.decode('utf-8'))

# Example usage functions
def simple_chat_example():
    """Simple chat example with Llama"""
    api = LlamaAPI()
    
    # Check available models
    models = api.list_models()
    if not models:
        print("No models found. Please install a model first.")
        return
    
    model_name = models[0]['name']
    print(f"Using model: {model_name}")
    
    # Simple generation
    response = api.generate(
        model=model_name,
        prompt="Explain quantum computing in simple terms."
    )
    
    print("Response:", response['response'])

def conversation_example():
    """Conversation-style chat example"""
    api = LlamaAPI()
    
    models = api.list_models()
    if not models:
        print("No models found. Please install a model first.")
        return
    
    model_name = models[0]['name']
    
    # Conversation messages
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What are the key features of Llama 3.1?"}
    ]
    
    response = api.chat(model=model_name, messages=messages)
    print("Assistant:", response['message']['content'])

def streaming_example():
    """Example of streaming responses"""
    api = LlamaAPI()
    
    models = api.list_models()
    if not models:
        print("No models found. Please install a model first.")
        return
    
    model_name = models[0]['name']
    
    print("Streaming response:")
    for chunk in api.generate(
        model=model_name,
        prompt="Write a short story about AI and humans working together.",
        stream=True
    ):
        if 'response' in chunk:
            print(chunk['response'], end='', flush=True)
        if chunk.get('done'):
            print("\n\nDone!")
            break

if __name__ == "__main__":
    print("Testing Llama API...")
    
    # Test basic functionality
    api = LlamaAPI()
    
    try:
        models = api.list_models()
        print(f"Found {len(models)} models:")
        for model in models:
            print(f"  - {model['name']}")
        
        if models:
            print("\nRunning examples...")
            simple_chat_example()
            print("\n" + "="*50 + "\n")
            conversation_example()
            print("\n" + "="*50 + "\n")
            streaming_example()
    
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to Ollama. Make sure it's running with: ollama serve")

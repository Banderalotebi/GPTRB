# 🦙 Arabic Llama Training & CLI System

A comprehensive, production-ready system for training and deploying Arabic-optimized Llama models with an advanced CLI interface. This project provides everything needed to work with Arabic text processing, model training, and interactive AI assistance.

## 🎯 Latest Features (v2.0)

- **🎨 Advanced CLI Interface** - Rich, colorful, interactive command-line interface
- **🔧 Real-time System Monitoring** - Live status updates and performance tracking
- **📚 Arabic Text Processing** - Complete RTL support with proper character reshaping
- **💬 Interactive Model Testing** - Test models with automatic result logging
- **📊 Analytics & Reporting** - Comprehensive usage statistics and model performance data
- **🚀 One-Click Training** - Simplified model training with guided workflows

## 🌟 Core Features

- **Complete Arabic text processing pipeline** with RTL support
- **Professional CLI interface** with Rich library integration
- **Automated model training and fine-tuning** for Arabic content
- **Real-time performance monitoring** and system diagnostics
- **Interactive chat testing** with result tracking
- **Comprehensive error handling** and recovery mechanisms

## 🚀 Quick Start

### 1. Automated Setup
```bash
./setup_llama.sh
```

### 2. Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Install Ollama (if not already installed)
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve &

# Download a model (choose one)
ollama pull llama3.2:1b    # Fastest (1.3GB)
ollama pull llama3.2:3b    # Balanced (2.0GB)
ollama pull llama3.1:8b    # High quality (4.7GB)
```

## 📁 Files Overview

| File | Description |
|------|-------------|
| `llama_setup.py` | Interactive setup and model management tool |
| `llama_api.py` | Python API for working with Llama models |
| `llama_examples.py` | Comprehensive examples and use cases |
| `setup_llama.sh` | Automated setup script |

## 🎯 Usage Examples

### Basic Chat
```python
from llama_api import LlamaAPI

api = LlamaAPI()
response = api.generate(
    model="llama3.2:3b",
    prompt="Explain quantum computing simply"
)
print(response['response'])
```

### Conversation Style
```python
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are Llama models?"}
]

response = api.chat(model="llama3.2:3b", messages=messages)
print(response['message']['content'])
```

### Streaming Responses
```python
for chunk in api.generate(model="llama3.2:3b", prompt="Write a story", stream=True):
    if 'response' in chunk:
        print(chunk['response'], end='', flush=True)
```

## 🧪 Try the Examples

Run the interactive examples:
```bash
python3 llama_examples.py
```

Features include:
- **Code Generation** - Generate code in any programming language
- **Text Analysis** - Sentiment analysis, topic extraction, summarization
- **Creative Writing** - Stories, poems, creative content
- **Data Extraction** - Extract structured data from unstructured text
- **Question Answering** - Answer questions based on context
- **Language Translation** - Translate between languages
- **Interactive Chat** - Full conversation interface

## 🔧 Model Management

Use the setup tool for easy model management:
```bash
python3 llama_setup.py
```

This provides:
- Model download and installation
- List installed models
- Interactive chat interface
- Model information and stats

## 📊 Model Comparison

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| Llama 3.2 1B | 1.3GB | ⚡⚡⚡ | ⭐⭐ | Testing, quick tasks |
| Llama 3.2 3B | 2.0GB | ⚡⚡ | ⭐⭐⭐ | Balanced performance |
| Llama 3.1 8B | 4.7GB | ⚡ | ⭐⭐⭐⭐ | High-quality tasks |
| Llama 3.1 70B | 40GB | 🐌 | ⭐⭐⭐⭐⭐ | Best quality |

## 🛠️ Advanced Usage

### Custom Parameters
```python
response = api.generate(
    model="llama3.2:3b",
    prompt="Your prompt here",
    options={
        "temperature": 0.7,    # Creativity (0.0-1.0)
        "top_p": 0.9,         # Nucleus sampling
        "top_k": 40,          # Top-k sampling
        "repeat_penalty": 1.1  # Repetition penalty
    }
)
```

### Fine-tuning (Advanced)
For custom fine-tuning, check the Hugging Face Transformers examples in the codebase.

## 🌐 API Endpoints

When Ollama is running, it provides a REST API at `http://localhost:11434`:

- `POST /api/generate` - Generate text
- `POST /api/chat` - Chat conversations
- `GET /api/tags` - List models
- `POST /api/pull` - Download models
- `POST /api/show` - Model information

## 🔍 Troubleshooting

### Common Issues

1. **Ollama not found**: Make sure Ollama is installed and in your PATH
2. **Connection refused**: Start Ollama service with `ollama serve`
3. **Model not found**: Download the model first with `ollama pull model_name`
4. **Out of memory**: Try a smaller model (e.g., llama3.2:1b)

### Performance Tips

- Use smaller models for development and testing
- Enable GPU acceleration if available
- Adjust temperature for different use cases (lower for factual, higher for creative)
- Use streaming for long responses

## 📝 License

Llama models are released under Meta's custom license. Check the official Llama repository for details.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📚 Resources

- [Ollama Documentation](https://ollama.ai/docs)
- [Llama Official Repository](https://github.com/meta-llama/llama)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
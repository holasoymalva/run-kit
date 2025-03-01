<div align="center">
  
# 🚀 RunKit

### The AI Project Scaffolding Tool for the Modern Developer

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/holasoymalva/run-kit)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.24+-ff4b4b.svg)](https://streamlit.io/)

<p align="center">
  <img src="https://via.placeholder.com/800x400?text=RunKit+Workflow" alt="RunKit Workflow" width="800"/>
</p>

**Deploy AI applications in minutes, not days.**

</div>

---

## 🔥 What is RunKit?

**RunKit** is a revolutionary CLI tool that scaffolds production-ready AI projects in seconds. Stop wasting time setting up boilerplate code and focus on what matters: building exceptional AI experiences.

Think of it as "Vue CLI meets AI development" – an interactive project generator that sets up everything you need to start building with Anthropic's Claude, Google's Gemini, or local LLMs through Ollama.

## ✨ Why RunKit?

- **Zero to AI in seconds** - Get a fully functional AI application running in less time than it takes to brew coffee
- **Freedom of choice** - Pick your preferred LLM provider (Claude, Gemini, or Ollama)
- **Modern stack** - Built on Streamlit for rapid UI development with a clean, responsive interface
- **Infinitely extendable** - Start with a template, then customize to your heart's content
- **Best practices baked in** - Security, performance, and codebase organization done right from day one

## 🛠️ Features

- **🤖 Multi-LLM Support**: Choose between Anthropic (Claude), Google (Gemini), or run models locally via Ollama
- **🔄 Customizable Templates**: Interactive setup that asks what YOU need
- **📱 Streamlit UI**: Beautiful, responsive interface works across devices
- **📂 File Analysis**: Upload and analyze PDFs, CSVs, Excel files, and text documents
- **💾 Vector Database Integration**: Optional ChromaDB integration for semantic search
- **🔌 Modular Architecture**: Clean, component-based design makes customization a breeze
- **🧠 Memory & Caching**: Optimized for performance and cost-effectiveness
- **📊 Visualization Ready**: Charts and data displays right out of the box

## 📊 Demo

<p align="center">
  <img src="https://via.placeholder.com/800x500?text=RunKit+Demo+GIF" alt="RunKit Demo" width="800"/>
</p>

## 🚀 Quick Start

### Installation

```bash
# Install the package
pip install run-kit

# Create a new project
run-kit my-ai-project
```

### Interactive Setup

RunKit will guide you through a series of questions to set up your perfect AI project:

```
🚀 Initializing AI project: my-ai-project

? Select the LLM provider you want to use:
  > Anthropic (Claude)
    Google (Gemini)
    LLM Local (Ollama)
    Multiple providers

? Select additional features:
  [x] Caching system
  [x] Conversation persistence
  [ ] File uploads
  [x] Vector database

? What type of project do you want to create?:
  > Simple chat
    Memory-enhanced assistant
    Document analyzer
    Specialized agent
```

### Launch Your App

```bash
cd my-ai-project
pip install -r requirements.txt
cp .env.example .env  # Add your API keys
streamlit run app.py
```

## 🧩 Project Structure

```
my-ai-project/
├── app.py                 # Entry point
├── .env                   # Environment variables (add your keys here)
├── .env.example           # Environment template
├── requirements.txt       # Dependencies
├── app/
│   ├── components/        # UI components
│   ├── llm/               # LLM connection logic
│   ├── utils/             # General utilities
│   ├── data/              # Data and resources
│   ├── styles/            # Custom CSS
│   └── db/                # Vector database (if selected)
└── tests/                 # Unit tests
```

## 🔧 Customization

RunKit is designed to be a starting point. Once generated, the code is yours to customize and extend:

```python
# Example: Changing the temperature parameter in app/llm/config.py
LLM_CONFIG = {
    "parameters": {
        "temperature": 0.8,  # Increase creativity
        "max_tokens": 2048,  # Double output length
        # ...
    }
}
```

## 📚 Use Cases

- **Customer Support Chatbots**: Deploy instantly with conversation history
- **Document Analysis Tools**: Upload PDFs and get AI-powered summaries
- **Internal Knowledge Bases**: Connect to vector DBs for semantic search
- **AI-Enhanced Dashboards**: Combine data visualization with LLM insights
- **Prototyping**: Test ideas with minimal overhead

## 🔗 Compatible LLMs

| Provider | Models |
|----------|--------|
| **Anthropic** | Claude 3 Opus, Claude 3 Sonnet, Claude 3 Haiku |
| **Google** | Gemini 1.5 Pro, Gemini 1.0 Pro |
| **Ollama** | Llama 3, Mistral, Phi-3 |

## 🛣️ Roadmap

- [ ] Fine-tuning support
- [ ] Multi-modal capabilities (image, audio)
- [ ] Function calling examples
- [ ] Agent frameworks integration
- [ ] Enterprise authentication

## 👥 Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or request features.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Support

If you find RunKit useful, please consider:
- Starring the repository ⭐
- Sharing with your network
- 
---

<div align="center">
  <p>Built with ❤️ in Silicon Valley</p>
  <p>© 2025 RunKit Team</p>
</div>

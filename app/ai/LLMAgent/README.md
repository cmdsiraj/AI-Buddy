# 🧠 LLM Agent Framework

A modular AI agent framework that integrates tools, memory, and multiple LLMs — enabling the agent to **reason**, **decide** when to use tools, and **build responses step by step**.

Built with **Python 3.9.6**.

---

## 🚀 Features

- 💬 Multi-LLM support (Google Gemini, Ollama, Groq)
- 🧠 Lightweight RAG via FAISS and Sentence Transformers
- 🧰 Tools:
  - Python execution
  - Web search (Serper API)
  - Web scraping
  - File reading
- 🔁 Modular and extensible (easily plug in new tools or LLMs)
- 🧩 Agent customization via role, goal, and backstory

---

## ⚙️ Setup & Installation

### 1. Environment Setup

#### macOS
```bash
chmod +x mac_setup.sh
./mac_setup.sh
```

#### Windows
- Use **Python 3.9.6** or lower
- (Optional) Create a virtual environment
- Install dependencies:
```bash
pip install -r requirements.txt
```

---

### 2. Configure Environment Variables

Create a `.env` file in the root directory with the following:

```env
GEMINI_API_KEY=your_gemini_api_key
SERPER_API_KEY=your_serper_api_key
SERPER_URL=https://serper_url_here.com
```

> These are required for Gemini and the web search tool.

---

### 3. Set Your LLM in `agent_test.py`

#### Option A: **Using Google Gemini** (Recommended)

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app)
2. Add it to `.env` as shown above
3. Use the Gemini model in `agent_test.py`:

```python
from MyAgent.LLM.GeminiLLM import GeminiLLM

llm = GeminiLLM(model_name="gemini-2.5-pro")  # or gemini-1.5-flash, etc.
```

#### Option B: Using Ollama (for local models like Llama3)

1. [Download Ollama](https://ollama.com/download)
2. Start the model locally:
```bash
ollama run llama3
```
3. In `agent_test.py`:
```python
from MyAgent.LLM.OllamaLLM import OllamaLLM

llm = OllamaLLM(model_name="llama3")
```

> No API key is needed when using Ollama locally.

---

## ▶️ Running the Agent

Once everything is configured:

```bash
python agent_test.py
```

The agent will start and accept natural language input.  
To exit, type `/exit`, `/quit`, or `/bye`.

---

## 🧩 Add Your Own Tools

1. Create a new tool in `MyAgent/Tools/`
2. Inherit from the base `Tool` class
3. Implement the `run()` method
4. Add your tool to the `tools` list in `agent_test.py` or your agent initializer

The agent will reason about when to use your tool based on the query.

---

## 🧠 Add Support for New LLMs

1. Create a class in `MyAgent/LLM/`
2. Extend `LLMBase`
3. Implement the `call()` method and `model_name`
4. Use your new LLM class in `agent_test.py`

---

## 📁 Project Structure

```
MyAgent/
├── Agent/           # Agent orchestration
├── Knowledge/       # Knowledge loading and RAG
├── LLM/             # Gemini, Ollama, Groq integrations
├── Tools/           # Tool implementations
├── VectorDB/        # Vector similarity search
├── utils/           # Prompt and YAML loaders
├── src/main.py      # Optional main entry
agent_test.py        # Default run script
requirements.txt
mac_setup.sh
.env                 # Your API keys
```

---

## 🛠️ Requirements

- Python 3.9.6
- `pip install -r requirements.txt`
- API keys for Gemini and Serper (see `.env` section)

---

## 🤝 Contributing & Feedback

This project started from curiosity and grew into a modular, multi-LLM AI agent framework.  
Feel free to fork it, build your own tools, or share feedback.

If you try it — I’d love to know what you build with it.

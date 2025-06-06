# TEST_SCENARIO_BOT

A local Python bot to generate BDD-style manual test scenarios from documents, code, and images using a GUI interface.

---

## 🔧 Installation Steps

### 1. Install Python

Download and install Python 3.10+ from:  
👉 https://www.python.org/downloads/

During installation, **check the box to add Python to PATH**.

---

### 2. Install Git (if not already installed)

Download and install Git from:  
👉 https://git-scm.com/download/win

---

### 3. Install Ollama (for local LLM)

Download and install Ollama:  
👉 https://ollama.com/download

Then pull a model of your choice (either `llama3` or `mistral`) using:

```bash


# OR for Mistral
ollama pull mistral
```

Make sure Ollama is running in the background before using the bot.

---

## 📦 Setup Instructions

Open a terminal inside the project folder (`TEST_SCENARIO_BOT`) and run:

```bash
# Step into the project directory
cd path/to/TEST_SCENARIO_BOT

# Create a virtual environment
python -m venv venv

# Activate the virtual environment (on Windows)
venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

> If `requirements.txt` is missing, you can generate it by:
> ```
> pip freeze > requirements.txt
> ```

---

## ▶️ Run the Application

Make sure Ollama is running and the desired model (`llama3` or `mistral`) is active, then run:

```bash
python main.py
```

This will launch the GUI. From there, you can select input files and automatically generate test scenarios.

---
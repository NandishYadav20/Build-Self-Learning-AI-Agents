# Project Assembly Guide

## 📦 Complete File List & Directory Structure

Use this guide to assemble your complete AI Agents project in `C:\Personal\PROJECTS\Build Self-Learning AI Agents\`

### Root Level Files

Create these files in the root directory:

```
Build-Self-Learning-AI-Agents/
├── README.md                    ← From provided files
├── setup.py                     ← From provided files
├── requirements.txt             ← From provided files
├── .gitignore                   ← From provided files
├── .env.example                 ← From provided files
└── LICENSE                      ← Create new (MIT License)
```

### Directory: src/

```
src/
├── __init__.py                  ← From src_init.py
├── config.py                    ← From provided files
└── logger.py                    ← From provided files
```

### Directory: src/agents/

```
src/agents/
├── __init__.py                  ← Create new (empty)
├── base_agent.py                ← From provided files
├── task_agent.py                ← From provided files
└── learning_agent.py            ← Create new (template below)
```

### Directory: src/memory/

```
src/memory/
├── __init__.py                  ← Create new (empty)
└── memory_manager.py            ← From provided files
```

### Directory: src/learning/

```
src/learning/
├── __init__.py                  ← Create new (empty)
└── learner.py                   ← From provided files
```

### Directory: src/utils/

```
src/utils/
├── __init__.py                  ← Create new (empty)
├── config.py                    ← Same as src/config.py
└── logger.py                    ← Same as src/logger.py
```

### Directory: examples/

```
examples/
├── __init__.py                  ← Create new (empty)
├── simple_agent.py              ← From simple_agent_example.py
└── calendar_agent.py            ← Create new (see template)
```

### Directory: tests/

```
tests/
├── __init__.py                  ← Create new (empty)
├── conftest.py                  ← Create new (see template)
├── test_agents.py               ← Create new (skeleton provided)
├── test_memory.py               ← Create new (skeleton provided)
└── test_learning.py             ← Create new (skeleton provided)
```

### Directory: docs/

```
docs/
├── README.md                    ← Already in main README
├── ARCHITECTURE.md              ← From provided files
├── GETTING_STARTED.md           ← Create new (see template)
├── API_REFERENCE.md             ← Create new (see template)
└── EXAMPLES.md                  ← Create new (see template)
```

### Directory: .github/

```
.github/
└── workflows/
    └── ci.yml                   ← Create new (see template)
```

### Data Directories (auto-created)

These will be created automatically when running:
```
data/
├── agents.db
└── memory.db

logs/
└── agent_YYYYMMDD.log
```

## 📝 Step-by-Step Assembly

### Step 1: Create Root Directory
```bash
mkdir "C:\Personal\PROJECTS\Build Self-Learning AI Agents"
cd "C:\Personal\PROJECTS\Build Self-Learning AI Agents"
```

### Step 2: Create All Directories
```bash
mkdir src src\agents src\memory src\learning src\utils
mkdir examples tests tests\__pycache__
mkdir docs ".github\workflows"
mkdir data logs
```

### Step 3: Create Root Files
Copy these exact files to root:
- `README.md`
- `setup.py`
- `requirements.txt`
- `.gitignore`
- `.env.example`

### Step 4: Create src/ Files
Copy to `src/`:
- `config.py`
- `logger.py`
- Create `__init__.py` with content below

### Step 5: Create src/agents/ Files
Copy to `src/agents/`:
- `base_agent.py`
- `task_agent.py`
- Create `__init__.py`
- Create `learning_agent.py`

### Step 6: Create src/memory/ Files
Copy to `src/memory/`:
- `memory_manager.py`
- Create `__init__.py`

### Step 7: Create src/learning/ Files
Copy to `src/learning/`:
- `learner.py`
- Create `__init__.py`

### Step 8: Create src/utils/ (Symlink or Copy)
Create `src/utils/` with symlinks or copies of:
- `config.py` (copy or link to ../config.py)
- `logger.py` (copy or link to ../logger.py)
- Create `__init__.py`

### Step 9: Create examples/ Files
Copy to `examples/`:
- `simple_agent.py` (rename from simple_agent_example.py)
- Create `calendar_agent.py` (see template)
- Create `__init__.py`

### Step 10: Create tests/ Files
Create skeleton test files (see templates below)

### Step 11: Create docs/ Files
Create documentation files (see templates below)

### Step 12: Create CI/CD Files
Create GitHub Actions workflow

### Step 13: Git Setup
```bash
git init
git add .
git commit -m "Initial commit: Self-learning AI agents framework"
```

## 📄 File Templates for Creation

### `src/__init__.py`
```python
"""Self-Learning AI Agents Framework"""
__version__ = "1.0.0"
__author__ = "Nandish Yadav"
```

### `src/agents/__init__.py`
```python
"""Agents module - Core agent implementations"""
```

### `src/memory/__init__.py`
```python
"""Memory module - Long-term memory management"""
```

### `src/learning/__init__.py`
```python
"""Learning module - Experience replay and learning"""
```

### `src/utils/__init__.py`
```python
"""Utilities module - Config and logging"""
```

### `examples/__init__.py`
```python
"""Examples module - Agent usage examples"""
```

### `tests/__init__.py`
```python
"""Tests module - Unit and integration tests"""
```

### `tests/conftest.py`
```python
"""Pytest configuration"""
import pytest
import asyncio
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

@pytest.fixture
def event_loop():
    """Create event loop for async tests"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
```

### `tests/test_agents.py`
```python
"""Test agent functionality"""
import pytest
from src.agents.base_agent import BaseAgent
from src.agents.task_agent import TaskAgent

@pytest.mark.asyncio
async def test_base_agent_creation():
    """Test agent initialization"""
    agent = TaskAgent()
    assert agent.name == "TaskAgent"
    assert agent.conversation_history == []

@pytest.mark.asyncio
async def test_task_agent_process():
    """Test task processing"""
    agent = TaskAgent()
    result = await agent.process("Schedule a meeting for next Tuesday")
    assert isinstance(result, str)
```

### `tests/test_memory.py`
```python
"""Test memory management"""
import pytest
from src.memory.memory_manager import MemoryManager

def test_memory_manager_creation():
    """Test memory manager initialization"""
    memory = MemoryManager(user_id="test_user")
    assert memory.user_id == "test_user"

def test_add_memory():
    """Test adding memory"""
    memory = MemoryManager(user_id="test_user")
    mem = memory.add_memory("Test fact", memory_type="fact")
    assert mem.content == "Test fact"
    assert mem.memory_type == "fact"

def test_search_memories():
    """Test memory search"""
    memory = MemoryManager(user_id="test_user")
    memory.add_memory("Alice is my colleague")
    results = memory.search_memories("Alice")
    assert len(results) > 0
```

### `tests/test_learning.py`
```python
"""Test learning functionality"""
import pytest
from src.learning.learner import Learner

def test_learner_creation():
    """Test learner initialization"""
    learner = Learner(agent_name="TestAgent")
    assert learner.agent_name == "TestAgent"

def test_record_experience():
    """Test experience recording"""
    learner = Learner(agent_name="TestAgent")
    exp = learner.record_experience(
        input_text="Test input",
        output_text="Test output",
        success=True,
        feedback_score=0.9
    )
    assert exp.success == True
    assert exp.feedback_score == 0.9

def test_get_learning_report():
    """Test learning report"""
    learner = Learner(agent_name="TestAgent")
    learner.record_experience("in", "out", success=True, feedback_score=0.8)
    report = learner.get_learning_report()
    assert report["total_experiences"] >= 1
```

### `examples/calendar_agent.py`
```python
"""Calendar Agent - Manages calendar tasks"""
import asyncio
from src.agents.task_agent import TaskAgent

class CalendarAgent(TaskAgent):
    """Agent for calendar management"""
    
    def __init__(self):
        super().__init__()
        self.name = "CalendarAgent"
        self.description = "Manages calendar events and meetings"

async def main():
    agent = CalendarAgent()
    result = await agent.process("Schedule a 1-hour meeting with Alice next Friday at 2 PM")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

### `docs/GETTING_STARTED.md`
```markdown
# Getting Started

## Prerequisites
- Python 3.9+
- OpenAI API Key
- Git

## Installation

1. Clone the repository
2. Create virtual environment
3. Install dependencies
4. Configure .env

## Running Examples

See examples/ folder for working code.

## Next Steps

Read ARCHITECTURE.md for system design.
```

### `docs/API_REFERENCE.md`
```markdown
# API Reference

## BaseAgent

### Methods
- `call_llm(user_input)` - Sync LLM call
- `call_llm_async(user_input)` - Async LLM call
- `call_llm_with_tools(user_input)` - LLM with tools

## MemoryManager

### Methods
- `add_memory(content)` - Add memory
- `search_memories(query)` - Search memories
- `update_memory(id, content)` - Update memory
- `delete_memory(id)` - Delete memory

## Learner

### Methods
- `record_experience()` - Record interaction
- `get_positive_experiences()` - Get successes
- `get_learning_report()` - Get statistics
```

### `docs/EXAMPLES.md`
```markdown
# Usage Examples

## Basic Agent

```python
from src.agents.task_agent import TaskAgent

agent = TaskAgent()
result = await agent.process("Your task here")
```

## Memory Usage

```python
from src.memory.memory_manager import MemoryManager

memory = MemoryManager()
memory.add_memory("Fact to remember")
results = memory.search_memories("search query")
```

## Learning

```python
from src.learning.learner import Learner

learner = Learner()
exp = learner.record_experience(input, output, success=True)
report = learner.get_learning_report()
```
```

### `.github/workflows/ci.yml`
```yaml
name: CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-asyncio pytest-cov
    - name: Run tests
      run: pytest --cov=src tests/
```

### `LICENSE` (MIT)
```
MIT License

Copyright (c) 2026 Nandish Yadav

Permission is hereby granted, free of charge...
[Full MIT License text]
```

## ✅ Verification Checklist

After assembly, verify:

- [ ] All directories created
- [ ] All files copied/created
- [ ] Python imports work without errors
- [ ] `.env` configured with OpenAI API key
- [ ] Example runs successfully
- [ ] Git initialized and committed

## 🚀 First Run

```bash
# Navigate to project
cd "C:\Personal\PROJECTS\Build Self-Learning AI Agents"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run example
python examples/simple_agent.py

# Run tests
pytest
```

## 📞 Troubleshooting

**Import errors**: Make sure `src/` is in Python path
**OpenAI errors**: Check .env has valid OPENAI_API_KEY
**Database errors**: Check `data/` directory exists and has write permissions

---

**Your project is now complete and ready for GitHub!** 🎉

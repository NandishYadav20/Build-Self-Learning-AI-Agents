# Build Self-Learning AI Agents

A **production-ready framework** for building intelligent, self-learning AI agents with long-term memory, agentic patterns, and continuous learning capabilities.

## 🎯 Features

- **Agentic Patterns**: Prompt chaining, routing, parallelization
- **Long-Term Memory**: Vector database integration with SQLite persistence
- **Structured Output**: Pydantic-based response formatting
- **Tool Use**: Function calling and dynamic tool integration
- **Experience Replay**: Learn from successful and failed interactions
- **Async Support**: Concurrent API calls for performance optimization
- **Production-Ready**: Error handling, logging, configuration management

## 📚 Project Structure

```
Build-Self-Learning-AI-Agents/
├── src/
│   ├── agents/
│   │   ├── base_agent.py          # Core LLM patterns and API integration
│   │   ├── task_agent.py          # Prompt chaining & routing examples
│   │   └── learning_agent.py      # Self-learning capabilities
│   ├── memory/
│   │   └── memory_manager.py      # Long-term memory with vector DB
│   ├── learning/
│   │   └── learner.py             # Experience replay & learning engine
│   └── utils/
│       ├── config.py              # Configuration management
│       └── logger.py              # Logging setup
├── examples/
│   ├── simple_agent.py            # Basic agent example
│   ├── learning_example.py        # Self-learning demonstration
│   └── calendar_agent.py          # Calendar management agent
├── tests/
│   ├── test_agents.py
│   ├── test_memory.py
│   └── test_learning.py
├── docs/
│   ├── ARCHITECTURE.md
│   ├── GETTING_STARTED.md
│   ├── API_REFERENCE.md
│   └── EXAMPLES.md
├── README.md
├── requirements.txt
├── setup.py
└── .env.example
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/Build-Self-Learning-AI-Agents.git
cd Build-Self-Learning-AI-Agents

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

### 3. Run Example

```python
import asyncio
from src.agents.task_agent import TaskAgent

async def main():
    agent = TaskAgent()
    result = await agent.process("Schedule a meeting for next Tuesday at 2 PM")
    print(result)

asyncio.run(main())
```

## 💡 Core Concepts

### 1. **BaseAgent** - Foundation for all agents
- Handles OpenAI API integration
- Manages conversation history
- Supports structured output
- Tool/function calling

### 2. **TaskAgent** - Implements agentic patterns
- **Prompt Chaining**: Break complex tasks into steps
- **Routing**: Route requests to different handlers
- **Gate Checks**: Validate task confidence levels

### 3. **MemoryManager** - Long-term memory system
- Store facts, experiences, preferences
- Search memories by semantic similarity
- Automatic memory consolidation
- SQLite persistence

### 4. **Learner** - Continuous improvement
- Record interactions/experiences
- Experience replay
- Extract patterns from successes
- Feedback-based learning

## 📖 Usage Examples

### Example 1: Simple Task Processing

```python
from src.agents.task_agent import TaskAgent
import asyncio

agent = TaskAgent()

# Process a task using prompt chaining
result = await agent.process("Schedule a meeting with Alice for next Friday")
print(result)
```

### Example 2: Memory Management

```python
from src.memory.memory_manager import MemoryManager

# Initialize memory system
memory = MemoryManager(user_id="user123")

# Add memories
memory.add_memory("Alice is my colleague", memory_type="fact")
memory.add_memory("I prefer afternoon meetings", memory_type="preference")

# Search memories
results = memory.search_memories("Alice")

# Get all memories
all_memories = memory.get_all_memories()
```

### Example 3: Learning from Interactions

```python
from src.learning.learner import Learner

learner = Learner(agent_name="TaskAgent")

# Record interaction
exp = learner.record_experience(
    input_text="Schedule a meeting",
    output_text="Meeting scheduled successfully",
    success=True,
    feedback_score=0.9
)

# Get statistics
report = learner.get_learning_report()
print(report)

# Extract patterns from successful experiences
patterns = learner.extract_patterns()
```

## 🏗️ Architecture Patterns

### Prompt Chaining
Sequential LLM calls where each step builds on the previous:

```
Input → Analyze → Extract Details → Route → Output
```

### Routing
Conditionally route based on task classification:

```
Input → Classify → [Route A | Route B | Route C] → Output
```

### Parallelization
Run independent LLM calls concurrently:

```
Input → [Call A, Call B, Call C] (async) → Aggregate → Output
```

## 🔧 Configuration

Edit `.env` file:

```
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4o-mini
LOG_LEVEL=INFO
QDRANT_HOST=localhost
QDRANT_PORT=6333
```

## 📊 Learning Pipeline

The framework implements a complete learning loop:

1. **Interaction**: Agent processes user input
2. **Recording**: Experience is stored with feedback
3. **Analysis**: Patterns extracted from successes
4. **Improvement**: Prompts refined based on patterns
5. **Feedback**: User provides feedback for future improvement

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/test_agents.py -v
```

## 📚 Documentation

- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - System design and patterns
- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Detailed setup guide
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API documentation
- **[EXAMPLES.md](docs/EXAMPLES.md)** - Detailed code examples

## 🎓 Key Learnings from Videos

This framework is built on insights from:

1. **"Building Effective AI Agents"** - Core patterns and LLM integration
   - Structured output using Pydantic
   - Tool use and function calling
   - Prompt chaining and routing
   - Error handling and retries

2. **"Introduction to AI Memory Systems"** - Long-term memory
   - Two-phase memory pipeline (summarize → extract → store)
   - Dynamic memory updates (add/update/delete)
   - Vector database integration
   - Semantic memory retrieval

## 🔌 Extensibility

### Add New Agent Types

```python
from src.agents.base_agent import BaseAgent

class MyCustomAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MyAgent",
            description="Custom agent",
            system_prompt="Your system prompt"
        )
    
    async def process(self, input_data: str) -> str:
        # Implement your logic
        return result
```

### Add Tools/Functions

```python
from src.agents.base_agent import ToolDefinition

tool = ToolDefinition(
    function={
        "name": "function_name",
        "description": "What it does",
        "parameters": {
            "type": "object",
            "properties": {...}
        }
    }
)

agent.tools.append(tool)
```

## ⚡ Performance Tips

- Use **prompt caching** for repeated queries
- Implement **parallelization** for independent operations
- Cache **memory searches** with consistent queries
- Use **structured output** for reliable parsing
- Enable **async operations** for I/O operations

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 👨‍💼 Author

**Nandish Yadav**  
- Email: nandishmalout1481@gmail.com
- Location: Winnipeg, Manitoba, Canada
- LinkedIn: [Your LinkedIn](link)
- GitHub: [@yourusername](link)

## 🙏 Acknowledgments

- Dave Ebeler & Data Luminina for excellent AI engineering content
- OpenAI for the API and best practices
- Mem0 team for memory management insights
- Anthropic for agentic patterns documentation

## 📞 Support

For issues, questions, or suggestions:
- Open a GitHub issue
- Check existing documentation
- Review example code

---

**Built with ❤️ for AI engineers who want production-ready agents**

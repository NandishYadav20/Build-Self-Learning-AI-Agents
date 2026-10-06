# System Architecture

## Overview

This framework implements a modern AI agent architecture based on insights from production deployments and research. It combines three core layers:

1. **LLM Integration Layer** - Direct API calls with structured patterns
2. **Memory Management Layer** - Long-term persistence and retrieval
3. **Learning Layer** - Experience replay and continuous improvement

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────┐
│                    Application Layer                     │
│  (User-facing agents: TaskAgent, CustomerServiceAgent)  │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│              Agentic Patterns Layer                      │
├─────────────────────────────────────────────────────────┤
│  • Prompt Chaining       • Routing                       │
│  • Parallelization       • Tool Use                      │
│  • Structured Output     • Error Handling                │
└─────────────────┬───────────────────────────────────────┘
                  │
┌─────────────────┴───────────────────────────────────────┐
│              BaseAgent Layer                            │
├─────────────────────────────────────────────────────────┤
│  • LLM API Integration (OpenAI)                         │
│  • Conversation History Management                      │
│  • Message Building                                     │
│  • Tool/Function Calling Support                        │
└─────────────────┬───────────────────────────────────────┘
                  │
         ┌────────┴────────┐
         │                 │
┌────────▼──────┐  ┌───────▼───────┐
│ Memory Layer  │  │ Learning Layer│
├───────────────┤  ├────────────────┤
│ • Facts       │  │ • Experiences │
│ • Experiences │  │ • Patterns    │
│ • Preferences │  │ • Feedback    │
│ • Search      │  │ • Reports     │
│ • Update      │  │ • Improve     │
└───────┬───────┘  └────────┬──────┘
        │                    │
┌───────▼────────────────────▼──────┐
│     Persistent Storage Layer       │
├───────────────────────────────────┤
│  • SQLite Database                │
│  • Vector Database (Qdrant)       │
│  • Configuration Files            │
│  • Logs                           │
└───────────────────────────────────┘
```

## Core Components

### 1. BaseAgent

The foundation of all agents. Implements:

- **LLM Integration**: Direct OpenAI API calls with retry logic
- **Message Management**: Maintains conversation history
- **Structured Output**: Pydantic-based response formatting
- **Tool Support**: Function definitions and calling
- **Async Support**: AsyncOpenAI for concurrent operations

**Key Methods:**
```python
call_llm()                    # Synchronous LLM call
call_llm_async()             # Asynchronous LLM call
call_llm_with_tools()        # LLM call with tools
get_conversation_history()   # Access conversation context
```

### 2. TaskAgent

Demonstrates agentic patterns:

**Prompt Chaining:**
```
analyze_task() → gate_check → extract_details() → route_task()
```

Each step passes structured output to the next step.

**Routing:**
```
classify_input() → if schedule then handle_schedule() 
                 → if modify then handle_modify()
                 → else handle_error()
```

### 3. MemoryManager

Long-term memory with two-phase pipeline:

**Phase 1: Summarization & Extraction**
- Condense conversation history
- Extract key facts
- Identify important entities

**Phase 2: Storage & Retrieval**
- Store in vector database (Qdrant)
- Persist in SQLite
- Enable semantic search

**Memory Types:**
- **Facts**: Persistent information (name, preferences)
- **Experiences**: Past interactions and outcomes
- **Preferences**: User/agent preferences

### 4. Learner

Implements experience replay:

**Recording:**
```python
learner.record_experience(
    input_text="...",
    output_text="...",
    success=True,
    feedback_score=0.9
)
```

**Learning:**
- Stores successful and failed interactions
- Extracts patterns from successes
- Enables feedback-based improvement

## Design Patterns

### 1. Prompt Chaining

For complex tasks that need multiple reasoning steps:

```python
# Step 1: Analyze
analysis = self.analyze_task(user_input)

# Step 2: Gate check
if not analysis.is_valid:
    return "Invalid task"

# Step 3: Extract details
details = self.extract_task_details(user_input)

# Step 4: Process
result = self.process_task(details)
```

**When to use:**
- Multi-step reasoning required
- Different prompts for different stages
- Need for validation gates
- Debugging individual steps

### 2. Routing

When input should go to different handlers:

```python
# Classify
classification = self.classify_input(input_data)

# Route
if classification.type == "A":
    result = handle_type_a(input_data)
elif classification.type == "B":
    result = handle_type_b(input_data)
```

**When to use:**
- Multiple input types
- Different handling per type
- Conditional logic needed
- Scalable to many categories

### 3. Parallelization

For independent operations:

```python
async def process(self, input_data):
    # Run checks in parallel
    check1_task = self.security_check(input_data)
    check2_task = self.content_check(input_data)
    
    results = await asyncio.gather(check1_task, check2_task)
    
    # Process results
    return self.aggregate_results(results)
```

**When to use:**
- Multiple independent checks
- Guard rails (security, content)
- Latency-sensitive applications
- Can run operations in parallel

### 4. Tool Use

For accessing external APIs or functions:

```python
# Define tool
tool = ToolDefinition(
    function={
        "name": "get_weather",
        "description": "Get weather data",
        "parameters": {...}
    }
)

# Agent decides if needed
response = agent.call_llm_with_tools(user_input)

# Execute if needed
if response["tool_calls"]:
    result = execute_tool(response["tool_calls"][0])
```

## Memory Architecture

### Two-Phase Pipeline

```
Conversation History
        ↓
    [Phase 1: Summarization]
    - Summarize conversation
    - Extract key facts
    - Identify entities
        ↓
    New Memories
        ↓
    [Phase 2: Storage & Update]
    - Compare with existing memories
    - Decide: add/update/delete
    - Store to vector DB
        ↓
    Memory Database
```

### Memory Operations

```python
# Add memory
memory.add_memory("Alice is my colleague", type="fact")

# Search memories (semantic)
results = memory.search_memories("colleagues")

# Update memory
memory.update_memory(memory_id, "Alice is my lead")

# Delete memory
memory.delete_memory(memory_id)

# Get all memories
all_memories = memory.get_all_memories()
```

## Learning Loop

```
                    ┌─────────────┐
                    │   Interact  │
                    └──────┬──────┘
                           │
                           ↓
                    ┌─────────────┐
                    │   Record    │
                    │ Experience  │
                    └──────┬──────┘
                           │
                           ↓
                    ┌─────────────┐
                    │   Analyze   │
                    │  Patterns   │
                    └──────┬──────┘
                           │
                           ↓
                    ┌─────────────┐
                    │   Improve   │
                    │   Prompts   │
                    └──────┬──────┘
                           │
                           ↓
                    ┌─────────────┐
         ┌─────────→│  Feedback   │
         │          └─────────────┘
         │
    ┌────┴─────┐
    │ Next Loop│
    └──────────┘
```

## Error Handling

### Retry Logic

```python
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
def call_llm_with_retry():
    return self.client.chat.completions.create(...)
```

### Graceful Degradation

```python
try:
    response = agent.call_llm(input_data)
except Exception as e:
    logger.error(f"LLM call failed: {e}")
    response = "I apologize, but I encountered an error."
```

## Configuration Management

```python
# Environment-based configuration
from src.utils.config import get_settings

settings = get_settings()

# Cached singleton instance
@lru_cache()
def get_settings() -> Settings:
    return Settings()  # Only created once
```

## Logging Architecture

Three-level logging:

1. **Console**: Real-time monitoring during development
2. **File**: Persistent logs for debugging
3. **Structured**: Tagged logs for analysis

```python
from src.utils.logger import logger

logger.info("Operation started")
logger.warning("Deprecated method used")
logger.error("Failed to process")
```

## Performance Considerations

### Caching

- Prompt caching (if using Claude)
- Memory search result caching
- Configuration caching

### Async Operations

- Parallel LLM calls for multiple checks
- Concurrent database operations
- Non-blocking I/O

### Batch Operations

- Process multiple items in parallel
- Batch memory updates
- Aggregate results efficiently

## Extensibility Points

### Add New Agent Type
1. Inherit from `BaseAgent`
2. Implement `process()` method
3. Define custom system prompt
4. Add tools if needed

### Add New Tool
1. Create tool definition
2. Implement handler function
3. Add to agent's tool list
4. Handle tool calls in agent

### Add New Memory Type
1. Extend `MemoryManager`
2. Add new table/fields
3. Implement search logic
4. Update UI if needed

### Add New Learning Strategy
1. Extend `Learner`
2. Implement pattern extraction
3. Add improvement logic
4. Track metrics

## Best Practices

1. **Keep Prompts Focused**: Each step should have a single, clear purpose
2. **Validate Input**: Always check confidence scores and validity
3. **Log Extensively**: Helps debugging and monitoring
4. **Use Structured Output**: Pydantic models for reliability
5. **Test Patterns**: Unit test each agentic pattern
6. **Monitor Performance**: Track success rates and feedback
7. **Iterate Prompts**: Continuously refine based on patterns
8. **Plan Before Coding**: Draw out flow on paper first

## Future Enhancements

- [ ] Prompt optimization engine
- [ ] Multi-model support (Claude, Gemini, etc.)
- [ ] Real-time vector embedding with Qdrant
- [ ] Distributed memory across services
- [ ] Advanced pattern recognition with ML
- [ ] Webhook callbacks for events
- [ ] Admin dashboard for monitoring

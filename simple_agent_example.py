"""
Simple Agent Example - Demonstrates basic LLM integration
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agents.base_agent import BaseAgent
from src.utils.logger import logger


class GreetingAgent(BaseAgent):
    """Simple agent that greets and responds to user input"""

    def __init__(self):
        system_prompt = """You are a friendly and helpful AI assistant.
        Respond warmly and concisely to user greetings and questions."""

        super().__init__(
            name="GreetingAgent",
            description="A friendly greeting agent",
            system_prompt=system_prompt,
        )

    async def process(self, input_data: str) -> str:
        """Process user input and respond"""
        logger.info(f"Processing: {input_data}")

        # Use async LLM call
        response = await self.call_llm_async(input_data)

        logger.info(f"Response: {response}")
        return response


class SummarizationAgent(BaseAgent):
    """Agent that summarizes text"""

    def __init__(self):
        system_prompt = """You are an expert text summarizer.
        Create concise, clear summaries that capture the main points.
        Keep summaries to 2-3 sentences maximum."""

        super().__init__(
            name="SummarizationAgent",
            description="Summarizes text content",
            system_prompt=system_prompt,
        )

    async def process(self, input_data: str) -> str:
        """Summarize input text"""
        summarize_prompt = f"""Please summarize the following text:

{input_data}

Provide a concise summary in 2-3 sentences."""

        response = await self.call_llm_async(summarize_prompt)
        return response


async def main():
    """Run examples"""
    print("=" * 60)
    print("Simple Agent Examples")
    print("=" * 60)

    # Example 1: Greeting Agent
    print("\n1. Greeting Agent Example")
    print("-" * 60)

    greeting_agent = GreetingAgent()
    greet_response = await greeting_agent.process("Hello! How are you doing today?")
    print(f"User: Hello! How are you doing today?")
    print(f"Agent: {greet_response}\n")

    # Example 2: Summarization Agent
    print("\n2. Summarization Agent Example")
    print("-" * 60)

    summary_agent = SummarizationAgent()

    text_to_summarize = """
    Artificial Intelligence has revolutionized many industries by automating tasks,
    improving decision-making, and enabling new capabilities. Machine learning models
    can now process vast amounts of data, identify patterns, and make predictions with
    remarkable accuracy. From healthcare to finance, AI applications are delivering
    significant value. However, responsible AI development requires careful consideration
    of ethics, bias, and transparency to ensure these powerful tools benefit society as a whole.
    """

    summary = await summary_agent.process(text_to_summarize)
    print(f"Original text length: {len(text_to_summarize)} characters")
    print(f"Summary: {summary}\n")

    # Example 3: Conversation History
    print("\n3. Conversation History Example")
    print("-" * 60)

    conversation_agent = GreetingAgent()

    # First turn
    response1 = await conversation_agent.process("My name is Alice")
    print(f"User: My name is Alice")
    print(f"Agent: {response1}\n")

    # Second turn - agent remembers context
    response2 = await conversation_agent.process("What's my name?")
    print(f"User: What's my name?")
    print(f"Agent: {response2}\n")

    # Show conversation history
    print("Conversation History:")
    for msg in conversation_agent.get_conversation_history():
        print(f"  {msg['role'].upper()}: {msg['content'][:80]}...")

    print("\n" + "=" * 60)
    print("Examples completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())

"""Task Agent - Implements prompt chaining and routing patterns"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import json

from .base_agent import BaseAgent, Message, ToolDefinition
from ..utils.logger import logger


class TaskType(str, Enum):
    """Enumeration of task types"""
    SCHEDULE = "schedule"
    RETRIEVE = "retrieve"
    ANALYZE = "analyze"
    UNKNOWN = "unknown"


class TaskAnalysis(BaseModel):
    """Task analysis result"""
    task_type: TaskType
    confidence: float = Field(..., ge=0, le=1)
    description: Optional[str] = None


class TaskDetails(BaseModel):
    """Extracted task details"""
    name: str
    priority: str = "normal"
    deadline: Optional[str] = None
    tags: List[str] = []


class TaskAgent(BaseAgent):
    """
    Agent implementing prompt chaining and routing patterns
    for task processing
    """

    def __init__(self):
        system_prompt = """You are a helpful task management assistant.
        Analyze user requests and determine the type of task."""

        super().__init__(
            name="TaskAgent",
            description="Processes tasks using prompt chaining and routing",
            system_prompt=system_prompt,
        )

    def analyze_task(self, user_input: str) -> TaskAnalysis:
        """
        Step 1: Analyze if input is a valid task

        Args:
            user_input: User request

        Returns:
            TaskAnalysis with task type and confidence
        """
        analysis_prompt = f"""Analyze this request and determine if it's a valid task.

Request: {user_input}

Respond in JSON format:
{{
    "task_type": "schedule|retrieve|analyze|unknown",
    "confidence": 0.0-1.0,
    "description": "Brief description"
}}"""

        response = self.call_llm(analysis_prompt)

        try:
            # Extract JSON from response
            import json
            json_match = response
            if "```" in response:
                json_match = response.split("```")[1].replace("json", "").strip()

            result = json.loads(json_match)
            analysis = TaskAnalysis(**result)

            logger.info(f"Task analysis: {analysis.task_type} (confidence: {analysis.confidence})")
            return analysis

        except Exception as e:
            logger.error(f"Error parsing task analysis: {e}")
            return TaskAnalysis(task_type=TaskType.UNKNOWN, confidence=0.0)

    def extract_task_details(self, user_input: str) -> Optional[TaskDetails]:
        """
        Step 2: Extract detailed task information

        Args:
            user_input: User request

        Returns:
            TaskDetails or None if extraction fails
        """
        extraction_prompt = f"""Extract task details from this request.

Request: {user_input}

Respond in JSON format:
{{
    "name": "task name",
    "priority": "high|normal|low",
    "deadline": "YYYY-MM-DD or null",
    "tags": ["tag1", "tag2"]
}}"""

        response = self.call_llm(extraction_prompt)

        try:
            import json
            json_match = response
            if "```" in response:
                json_match = response.split("```")[1].replace("json", "").strip()

            result = json.loads(json_match)
            details = TaskDetails(**result)

            logger.info(f"Task details extracted: {details.name}")
            return details

        except Exception as e:
            logger.error(f"Error extracting task details: {e}")
            return None

    def route_task(self, analysis: TaskAnalysis, details: Optional[TaskDetails]) -> str:
        """
        Step 3: Route task based on analysis

        Args:
            analysis: Task analysis result
            details: Task details

        Returns:
            Routing decision/confirmation
        """
        if analysis.confidence < 0.7:
            return "Gate check failed: Low confidence in task type"

        if analysis.task_type == TaskType.UNKNOWN:
            return "Cannot process: Unknown task type"

        if details is None:
            return "Cannot process: Failed to extract task details"

        # Route based on task type
        routes = {
            TaskType.SCHEDULE: f"✓ Scheduling task: {details.name}",
            TaskType.RETRIEVE: f"✓ Retrieving information for: {details.name}",
            TaskType.ANALYZE: f"✓ Analyzing task: {details.name}",
            TaskType.UNKNOWN: "✗ Unknown task type",
        }

        result = routes.get(analysis.task_type, "✗ Unexpected task type")
        logger.info(f"Task routing decision: {result}")
        return result

    async def process(self, input_data: str) -> str:
        """
        Process task using prompt chaining pattern

        Args:
            input_data: User request

        Returns:
            Processing result
        """
        logger.info(f"Processing task: {input_data}")

        # Chain 1: Analyze
        analysis = self.analyze_task(input_data)

        # Chain 2: Extract details
        details = self.extract_task_details(input_data)

        # Chain 3: Route
        routing_result = self.route_task(analysis, details)

        return routing_result


class CustomerServiceAgent(BaseAgent):
    """
    Example agent for customer service with routing
    """

    def __init__(self):
        system_prompt = """You are a helpful customer service representative.
        Route customer inquiries to appropriate departments."""

        super().__init__(
            name="CustomerServiceAgent",
            description="Routes customer inquiries",
            system_prompt=system_prompt,
        )

    def classify_inquiry(self, inquiry: str) -> Dict[str, Any]:
        """Classify customer inquiry"""
        prompt = f"""Classify this customer inquiry into one category:
        - billing
        - technical_support
        - general_inquiry
        - complaint
        - other

Inquiry: {inquiry}

Respond with JSON: {{"category": "...", "urgency": "low|medium|high", "summary": "..."}}"""

        response = self.call_llm(prompt)

        try:
            import json
            json_match = response
            if "```" in response:
                json_match = response.split("```")[1].replace("json", "").strip()
            return json.loads(json_match)
        except:
            return {"category": "other", "urgency": "medium"}

    async def process(self, input_data: str) -> str:
        """Process customer inquiry"""
        classification = self.classify_inquiry(input_data)

        # Route based on category
        routes = {
            "billing": "Routing to Billing Department...",
            "technical_support": "Routing to Technical Support...",
            "general_inquiry": "Responding to your inquiry...",
            "complaint": "Routing to Management Review...",
            "other": "Processing your request...",
        }

        route = routes.get(classification.get("category"), "Processing...")
        logger.info(f"Customer inquiry routed: {route}")

        return f"{route} Urgency: {classification.get('urgency', 'medium')}"

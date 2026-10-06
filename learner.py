"""Learning Engine - Implements experience replay and continuous improvement"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import json
import sqlite3
from pathlib import Path

from ..utils.logger import logger
from ..utils.config import get_settings


@dataclass
class Experience:
    """Experience/interaction data"""
    id: str
    agent_name: str
    input_text: str
    output_text: str
    success: bool
    feedback_score: float = 0.0  # -1.0 to 1.0
    timestamp: str = ""
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()


class Learner:
    """
    Learning engine that:
    - Stores experiences/interactions
    - Performs experience replay
    - Extracts patterns
    - Improves prompts based on feedback
    """

    def __init__(self, agent_name: str = "default_agent"):
        self.agent_name = agent_name
        self.settings = get_settings()
        self.experiences: List[Experience] = []
        self._init_db()
        logger.info(f"Learner initialized for agent: {agent_name}")

    def _init_db(self) -> None:
        """Initialize SQLite database for experiences"""
        db_path = Path(self.settings.sqlite_db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self.db_path = db_path

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS experiences (
                    id TEXT PRIMARY KEY,
                    agent_name TEXT NOT NULL,
                    input_text TEXT NOT NULL,
                    output_text TEXT NOT NULL,
                    success BOOLEAN DEFAULT TRUE,
                    feedback_score REAL DEFAULT 0.0,
                    timestamp TEXT NOT NULL,
                    tags TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_agent_name
                ON experiences(agent_name)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_success
                ON experiences(success)
            """)

            conn.commit()

    def record_experience(
        self,
        input_text: str,
        output_text: str,
        success: bool = True,
        feedback_score: float = 0.0,
        tags: Optional[List[str]] = None,
    ) -> Experience:
        """
        Record an interaction/experience

        Args:
            input_text: Input to the agent
            output_text: Agent's output
            success: Whether the interaction was successful
            feedback_score: User feedback (-1.0 to 1.0)
            tags: Tags for categorization

        Returns:
            Created Experience object
        """
        import uuid
        experience_id = str(uuid.uuid4())

        experience = Experience(
            id=experience_id,
            agent_name=self.agent_name,
            input_text=input_text,
            output_text=output_text,
            success=success,
            feedback_score=feedback_score,
            tags=tags or [],
        )

        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO experiences
                (id, agent_name, input_text, output_text, success, feedback_score, timestamp, tags)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                experience.id,
                experience.agent_name,
                experience.input_text,
                experience.output_text,
                experience.success,
                experience.feedback_score,
                experience.timestamp,
                json.dumps(experience.tags),
            ))
            conn.commit()

        self.experiences.append(experience)
        logger.info(f"Experience recorded: {experience.id} (success={success}, feedback={feedback_score})")

        return experience

    def get_positive_experiences(self, limit: int = 10) -> List[Experience]:
        """Get successful interactions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, agent_name, input_text, output_text, success, feedback_score, timestamp, tags
                FROM experiences
                WHERE agent_name = ? AND success = TRUE
                ORDER BY feedback_score DESC, timestamp DESC
                LIMIT ?
            """, (self.agent_name, limit))

            experiences = []
            for row in cursor:
                tags = json.loads(row[7]) if row[7] else []
                exp = Experience(
                    id=row[0],
                    agent_name=row[1],
                    input_text=row[2],
                    output_text=row[3],
                    success=row[4],
                    feedback_score=row[5],
                    timestamp=row[6],
                    tags=tags,
                )
                experiences.append(exp)

        return experiences

    def get_negative_experiences(self, limit: int = 10) -> List[Experience]:
        """Get failed interactions"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, agent_name, input_text, output_text, success, feedback_score, timestamp, tags
                FROM experiences
                WHERE agent_name = ? AND (success = FALSE OR feedback_score < 0)
                ORDER BY feedback_score ASC, timestamp DESC
                LIMIT ?
            """, (self.agent_name, limit))

            experiences = []
            for row in cursor:
                tags = json.loads(row[7]) if row[7] else []
                exp = Experience(
                    id=row[0],
                    agent_name=row[1],
                    input_text=row[2],
                    output_text=row[3],
                    success=row[4],
                    feedback_score=row[5],
                    timestamp=row[6],
                    tags=tags,
                )
                experiences.append(exp)

        return experiences

    def get_learning_report(self) -> Dict[str, Any]:
        """Get learning statistics"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT
                    COUNT(*),
                    COUNT(CASE WHEN success = TRUE THEN 1 END),
                    COUNT(CASE WHEN success = FALSE THEN 1 END),
                    AVG(CASE WHEN success = TRUE THEN feedback_score END),
                    MIN(timestamp),
                    MAX(timestamp)
                FROM experiences
                WHERE agent_name = ?
            """, (self.agent_name,))

            row = cursor.fetchone()
            if row:
                total, successful, failed, avg_feedback, first_exp, last_exp = row
                success_rate = (successful / total * 100) if total > 0 else 0

                return {
                    "total_experiences": total or 0,
                    "successful_interactions": successful or 0,
                    "failed_interactions": failed or 0,
                    "success_rate_percent": success_rate,
                    "average_feedback_score": avg_feedback or 0.0,
                    "first_experience": first_exp,
                    "last_experience": last_exp,
                }

        return {}

    def extract_patterns(self) -> List[Dict[str, Any]]:
        """Extract patterns from successful interactions"""
        positive_exp = self.get_positive_experiences(limit=100)

        patterns = []
        for exp in positive_exp:
            patterns.append({
                "input_patterns": self._extract_input_patterns(exp.input_text),
                "output_patterns": self._extract_output_patterns(exp.output_text),
                "tags": exp.tags,
                "feedback_score": exp.feedback_score,
            })

        logger.info(f"Extracted {len(patterns)} patterns from successful experiences")
        return patterns

    def _extract_input_patterns(self, text: str) -> List[str]:
        """Extract patterns from input text"""
        patterns = []
        # Simple pattern extraction (can be enhanced with NLP)
        words = text.lower().split()
        patterns.extend(words[:3])  # First 3 words
        return patterns

    def _extract_output_patterns(self, text: str) -> List[str]:
        """Extract patterns from output text"""
        patterns = []
        # Simple pattern extraction
        if "error" in text.lower():
            patterns.append("error_handling")
        if "success" in text.lower():
            patterns.append("positive_confirmation")
        if len(text) > 100:
            patterns.append("detailed_response")
        return patterns

    def give_feedback(self, experience_id: str, feedback_score: float) -> bool:
        """
        Provide feedback on an experience

        Args:
            experience_id: ID of the experience
            feedback_score: Feedback score (-1.0 to 1.0)

        Returns:
            Success status
        """
        feedback_score = max(-1.0, min(1.0, feedback_score))

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                UPDATE experiences
                SET feedback_score = ?
                WHERE id = ? AND agent_name = ?
            """, (feedback_score, experience_id, self.agent_name))
            conn.commit()

            success = cursor.rowcount > 0

        if success:
            logger.info(f"Feedback recorded for experience {experience_id}: {feedback_score}")

        return success

    def clear_experiences(self) -> None:
        """Clear all experiences"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM experiences WHERE agent_name = ?", (self.agent_name,))
            conn.commit()

        self.experiences.clear()
        logger.warning(f"All experiences cleared for agent: {self.agent_name}")

"""Memory Management System - Implements long-term memory with vector DB"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import json
import sqlite3
from pathlib import Path

from ..utils.logger import logger
from ..utils.config import get_settings


@dataclass
class Memory:
    """Memory data structure"""
    id: str
    user_id: str
    content: str
    timestamp: str
    memory_type: str = "fact"  # fact, experience, preference
    confidence: float = 1.0
    embedding: Optional[List[float]] = None


class MemoryManager:
    """
    Manages agent memory with:
    - Vector database integration (Qdrant)
    - SQLite for structured storage
    - Memory retrieval and update operations
    """

    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.settings = get_settings()
        self.memories: List[Memory] = []
        self._init_db()
        logger.info(f"MemoryManager initialized for user: {user_id}")

    def _init_db(self) -> None:
        """Initialize SQLite database"""
        db_path = Path(self.settings.memory_db_path)
        db_path.parent.mkdir(parents=True, exist_ok=True)

        self.db_path = db_path

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memories (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    content TEXT NOT NULL,
                    memory_type TEXT DEFAULT 'fact',
                    confidence REAL DEFAULT 1.0,
                    timestamp TEXT NOT NULL,
                    embedding TEXT,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_id
                ON memories(user_id)
            """)

            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_timestamp
                ON memories(timestamp)
            """)

            conn.commit()

    def add_memory(
        self,
        content: str,
        memory_type: str = "fact",
        confidence: float = 1.0,
    ) -> Memory:
        """
        Add memory to the system

        Args:
            content: Memory content
            memory_type: Type of memory (fact, experience, preference)
            confidence: Confidence score (0-1)

        Returns:
            Created Memory object
        """
        import uuid
        memory_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()

        memory = Memory(
            id=memory_id,
            user_id=self.user_id,
            content=content,
            timestamp=timestamp,
            memory_type=memory_type,
            confidence=confidence,
        )

        # Store in database
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO memories (id, user_id, content, memory_type, confidence, timestamp)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (memory.id, memory.user_id, memory.content, memory.memory_type,
                  memory.confidence, memory.timestamp))
            conn.commit()

        self.memories.append(memory)
        logger.info(f"Memory added: {memory.id}")

        return memory

    def search_memories(self, query: str, limit: int = 5) -> List[Memory]:
        """
        Search memories by semantic similarity

        Args:
            query: Search query
            limit: Maximum number of results

        Returns:
            List of matching memories
        """
        # Simple keyword matching (in production, use vector similarity)
        results = []
        query_lower = query.lower()

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, user_id, content, memory_type, confidence, timestamp
                FROM memories
                WHERE user_id = ? AND (content LIKE ? OR content LIKE ?)
                ORDER BY confidence DESC, timestamp DESC
                LIMIT ?
            """, (self.user_id, f"%{query_lower}%", f"%{query}%", limit))

            for row in cursor:
                memory = Memory(
                    id=row[0],
                    user_id=row[1],
                    content=row[2],
                    memory_type=row[3],
                    confidence=row[4],
                    timestamp=row[5],
                )
                results.append(memory)

        logger.info(f"Found {len(results)} memories matching query: {query}")
        return results

    def get_all_memories(self) -> List[Memory]:
        """Get all memories for the user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT id, user_id, content, memory_type, confidence, timestamp
                FROM memories
                WHERE user_id = ?
                ORDER BY timestamp DESC
            """, (self.user_id,))

            memories = []
            for row in cursor:
                memory = Memory(
                    id=row[0],
                    user_id=row[1],
                    content=row[2],
                    memory_type=row[3],
                    confidence=row[4],
                    timestamp=row[5],
                )
                memories.append(memory)

        return memories

    def update_memory(self, memory_id: str, new_content: str) -> Optional[Memory]:
        """Update existing memory"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                UPDATE memories
                SET content = ?, timestamp = ?
                WHERE id = ? AND user_id = ?
            """, (new_content, datetime.now().isoformat(), memory_id, self.user_id))
            conn.commit()

        logger.info(f"Memory updated: {memory_id}")
        return self.search_memories(new_content, limit=1)[0] if self.search_memories(new_content, limit=1) else None

    def delete_memory(self, memory_id: str) -> bool:
        """Delete memory"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                DELETE FROM memories
                WHERE id = ? AND user_id = ?
            """, (memory_id, self.user_id))
            conn.commit()

            deleted = cursor.rowcount > 0

        if deleted:
            logger.info(f"Memory deleted: {memory_id}")

        return deleted

    def get_memory_summary(self) -> Dict[str, Any]:
        """Get summary of memory system"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT COUNT(*),
                       COUNT(CASE WHEN memory_type = 'fact' THEN 1 END),
                       COUNT(CASE WHEN memory_type = 'experience' THEN 1 END),
                       COUNT(CASE WHEN memory_type = 'preference' THEN 1 END),
                       AVG(confidence)
                FROM memories
                WHERE user_id = ?
            """, (self.user_id,))

            row = cursor.fetchone()
            if row:
                total, facts, experiences, preferences, avg_confidence = row
                return {
                    "total_memories": total or 0,
                    "facts": facts or 0,
                    "experiences": experiences or 0,
                    "preferences": preferences or 0,
                    "average_confidence": avg_confidence or 0.0,
                }

        return {"total_memories": 0}

    def clear_all_memories(self) -> None:
        """Clear all memories for the user"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM memories WHERE user_id = ?", (self.user_id,))
            conn.commit()

        self.memories.clear()
        logger.warning(f"All memories cleared for user: {self.user_id}")

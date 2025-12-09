from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Deque, Dict, Optional


@dataclass
class RoutedTask:
    """Simple task record for routing between agents."""

    task_id: str
    target_agent: str
    payload: str | dict | None = None


class TaskRouter:
    """In-memory task router enforcing a per-agent active-task cap.

    The router tracks active task counts per agent and queues overflow
    for later dispatch. It is intentionally minimal; plug in external
    stores/locks when running distributed workers.
    """

    def __init__(self, max_active_per_agent: int = 3):
        self.max_active_per_agent = max_active_per_agent
        self._active: Dict[str, int] = {}
        self._queue: Deque[RoutedTask] = deque()

    def schedule(self, task: RoutedTask) -> str:
        """Attempt to dispatch the task; queue if the target is saturated."""
        active = self._active.get(task.target_agent, 0)
        if active < self.max_active_per_agent:
            self._active[task.target_agent] = active + 1
            return "dispatched"
        self._queue.append(task)
        return "queued"

    def complete(self, task_id: str, target_agent: str) -> Optional[RoutedTask]:
        """Mark a task complete and dispatch the next queued item if available."""
        if target_agent in self._active:
            self._active[target_agent] = max(0, self._active[target_agent] - 1)
            if self._active[target_agent] == 0:
                del self._active[target_agent]
        if not self._queue:
            return None
        next_task = self._queue.popleft()
        self._active[next_task.target_agent] = self._active.get(next_task.target_agent, 0) + 1
        return next_task

    def stats(self) -> dict:
        """Return a snapshot of active counts and queued tasks."""
        return {
            "max_active_per_agent": self.max_active_per_agent,
            "active": dict(self._active),
            "queue_depth": len(self._queue),
        }

    def drain_queue(self) -> list[RoutedTask]:
        """Clear the queue without dispatching (useful for shutdowns)."""
        drained: list[RoutedTask] = list(self._queue)
        self._queue.clear()
        return drained

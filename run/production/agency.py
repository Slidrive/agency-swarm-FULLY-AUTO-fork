from __future__ import annotations

from typing import Iterable

from agency_swarm import Agency, Agent, ModelSettings, function_tool

from agency_swarm.utils.task_router import RoutedTask, TaskRouter
from .settings import ProductionSettings


def _build_router_tools(router: TaskRouter) -> list:
    @function_tool(strict_mode=False)
    def claim_task(task_id: str, target_agent: str, payload: str | dict | None = None) -> str:
        """Claim or enqueue a task for the target agent respecting the task cap."""

        return router.schedule(RoutedTask(task_id=task_id, target_agent=target_agent, payload=payload))

    @function_tool(strict_mode=False)
    def complete_task(task_id: str, target_agent: str) -> str:
        """Mark a task done and release capacity; may dispatch the next queued task."""

        routed = router.complete(task_id=task_id, target_agent=target_agent)
        if routed:
            return f"released_and_dispatched:{routed.task_id}:{routed.target_agent}"
        return "released"

    @function_tool(strict_mode=False)
    def task_router_stats() -> dict:
        """Return current active counts and queue depth for monitoring."""

        return router.stats()

    return [claim_task, complete_task, task_router_stats]


def _agent(
    name: str,
    instructions: str,
    tools: Iterable,
    settings: ProductionSettings,
    schemas_folder: str | None = None,
    api_headers: dict[str, dict[str, str]] | None = None,
    api_params: dict[str, dict[str, str | int | float]] | None = None,
) -> Agent:
    return Agent(
        name=name,
        description=instructions.split("\n", 1)[0],
        instructions=instructions,
        tools=list(tools),
        model=settings.model,
        model_settings=ModelSettings(max_tokens=4096),
        schemas_folder=schemas_folder,
        api_headers=api_headers or {},
        api_params=api_params or {},
    )


def build_agency(settings: ProductionSettings | None = None) -> Agency:
    settings = settings or ProductionSettings()
    router = TaskRouter(max_active_per_agent=settings.max_active_tasks_per_agent)
    router_tools = _build_router_tools(router)

    schemas_folder = "run/production/schemas"
    api_headers = {}
    api_params = {}

    ceo = _agent(
        "CEO",
        """
        You are the CEO and single frontdoor. Collect goals, break them into tasks, respect the 3-task-per-agent cap,
        and route work to the right specialists. Keep status concise and close tasks via complete_task.
        """.strip(),
        router_tools,
        settings,
        schemas_folder=None,
    )

    product = _agent(
        "Product",
        """
        Clarify requirements, acceptance criteria, and priorities. Minimize ambiguity, deliver crisp specs, and unblock
        builders quickly.
        """.strip(),
        router_tools,
        settings,
        schemas_folder=schemas_folder,
        api_headers=api_headers,
        api_params=api_params,
    )

    tech_lead = _agent(
        "TechLead",
        """
        Own architecture and plans. Slice work into buildable tasks, request more builders if the queue grows, and keep
        quality high. Optimize for reliability and speed.
        """.strip(),
        router_tools,
        settings,
        schemas_folder=schemas_folder,
        api_headers=api_headers,
        api_params=api_params,
    )

    builder_1 = _agent(
        "Builder-1",
        """
        Implement features, wire tools/APIs, and return working outputs. When done, call complete_task to free capacity.
        """.strip(),
        router_tools,
        settings,
        schemas_folder=schemas_folder,
        api_headers=api_headers,
        api_params=api_params,
    )

    qa = _agent(
        "QA",
        """
        Validate behavior against acceptance criteria. Write and propose tests. Block release if defects exist.
        """.strip(),
        router_tools,
        settings,
        schemas_folder=schemas_folder,
        api_headers=api_headers,
        api_params=api_params,
    )

    ops = _agent(
        "Ops",
        """
        Handle deployment, rollback, and operational readiness. Keep changes safe and observable.
        """.strip(),
        router_tools,
        settings,
        schemas_folder=schemas_folder,
        api_headers=api_headers,
        api_params=api_params,
    )

    communication_flows = [
        ceo > product,
        ceo > tech_lead,
        ceo > builder_1,
        ceo > qa,
        ceo > ops,
        tech_lead > builder_1,
        tech_lead > qa,
        qa > builder_1,
        ops > ceo,
    ]

    return Agency(
        ceo,
        communication_flows=communication_flows,
        name=settings.agency_name,
    )


__all__ = ["build_agency", "ProductionSettings"]

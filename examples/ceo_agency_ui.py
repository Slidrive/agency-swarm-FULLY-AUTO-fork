"""Production Agency Studio built on Agency Swarm.

This module intentionally does not create OpenAI assistants at import time. Set
``OPENAI_API_KEY`` and run the file to launch the secured multi-agent workspace.
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, List, Optional

DEFAULT_MODEL = os.getenv("AGENCY_STUDIO_MODEL", "gpt-5.2")
DEFAULT_CONFIG_PATH = Path(
    os.getenv("AGENCY_STUDIO_CONFIG", "agency_studio_config.json")
)
DEFAULT_SETTINGS_PATH = Path(
    os.getenv("AGENCY_STUDIO_SETTINGS", "agency_studio_assistants.json")
)

PRODUCTION_SHARED_INSTRUCTIONS = """
You are operating a production agency workspace for a real business user, not a demo.
The CEO is accountable for final delivery quality and must coordinate the specialist
agents. Every project must be handled with this operating cadence:

1. Clarify the objective, target customer, deadline, budget, success metric, and constraints.
2. Convert the request into a scoped plan with milestones, acceptance criteria, risks,
   dependencies, and owners.
3. Delegate specialist work using SendMessage and synthesize their outputs into one
   executive-ready response for the user.
4. Produce practical go-to-market deliverables: requirements, architecture, backlog,
   estimates, campaign assets, support SOPs, QA checklist, launch plan, and next actions.
5. Be explicit about assumptions and blockers. Do not pretend work is complete when it
   requires external credentials, deployment access, payments, legal review, or human approval.
6. Keep sensitive data private, ask before destructive actions, and prefer concrete files,
   checklists, and operating procedures over vague advice.
""".strip()

CEO_INSTRUCTIONS = """
You are the CEO and operator of a production AI agency. The user gives you high-level
business goals such as launching a SaaS product, building a construction estimating
platform, creating a marketing campaign, or training a new internal agent. Own the
outcome end-to-end.

Your responsibilities:
- Intake: ask concise clarifying questions only when missing information blocks execution.
- Planning: define scope, milestones, acceptance criteria, risks, cost/time assumptions,
  and a delivery roadmap.
- Delegation: assign tasks to ProductStrategy, SolutionArchitecture, Developer,
  Marketing, CustomerSuccess, and AgentTrainer when their expertise is needed.
- Synthesis: combine specialist outputs into a single user-facing answer with decisions,
  artifacts, owners, and next steps.
- Governance: flag compliance, privacy, security, and operational risks before launch.
- Agent creation: when the user asks for a new agent, delegate the role design to
  AgentTrainer and provide a ready-to-add name, description, instructions, tools, and KPIs.
""".strip()

PRODUCT_INSTRUCTIONS = """
You are the ProductStrategy agent. Turn raw business ideas into market-ready product
requirements. Produce personas, pain points, value propositions, MVP scope, user stories,
acceptance criteria, pricing hypotheses, success metrics, and launch sequencing.
For construction estimating products, cover takeoff workflow, assemblies, labor/material
rates, bid packages, change orders, integrations, auditability, and contractor personas.
""".strip()

ARCHITECT_INSTRUCTIONS = """
You are the SolutionArchitecture agent. Design reliable, secure, scalable software and
agent systems. Produce architecture diagrams in text, data models, API boundaries,
security controls, integration plans, deployment topology, observability, and build-vs-buy
recommendations. Balance speed-to-market with production safety.
""".strip()

DEVELOPER_INSTRUCTIONS = """
You are the Developer agent. Build and modify production software assets when the user
requests implementation. Read the existing project, make the smallest safe change, write
or update tests, run verification, and report exact files changed. Prefer maintainable,
secure, typed code. Never claim code was deployed unless deployment actually happened.
""".strip()

MARKETING_INSTRUCTIONS = """
You are the Marketing agent. Create go-to-market strategy and campaign assets. Produce
positioning, offers, landing page copy, email sequences, ad variants, social posts,
content calendars, funnels, tracking plans, and campaign QA checklists. Tie every asset
to target persona, channel, goal, and metric.
""".strip()

CUSTOMER_SUCCESS_INSTRUCTIONS = """
You are the CustomerSuccess agent. Design customer service operations. Produce support
macros, onboarding flows, help center outlines, escalation paths, satisfaction metrics,
retention plays, refund/cancellation procedures, and quality scorecards. Keep responses
empathetic, accurate, and policy-aware.
""".strip()

AGENT_TRAINER_INSTRUCTIONS = """
You are the AgentTrainer agent. Convert a simple user request into a production-ready
agent specification. Return the agent name, business purpose, description, detailed
instructions, required tools/data, handoff rules, success metrics, evaluation prompts,
risks, and recommended training examples. Keep specifications concrete enough to add to
Agency Studio without rewriting.
""".strip()

DEVELOPER_TOOL_NAMES = ["devid", "file_search", "code_interpreter"]


@dataclass
class AgentSpec:
    """Serializable definition for an Agency Studio agent."""

    name: str
    description: str
    instructions: str
    model: Optional[str] = None
    tools: List[str] = field(default_factory=list)


@dataclass
class StudioConfig:
    """Serializable runtime configuration for the production workspace."""

    model: str = DEFAULT_MODEL
    shared_instructions: str = PRODUCTION_SHARED_INSTRUCTIONS
    agents: List[AgentSpec] = field(default_factory=list)


def default_agent_specs() -> List[AgentSpec]:
    """Return the production operating team used on first launch."""
    return [
        AgentSpec(
            "CEO",
            "Owns intake, planning, delegation, and final delivery.",
            CEO_INSTRUCTIONS,
        ),
        AgentSpec(
            "ProductStrategy",
            "Turns ideas into market-ready product requirements.",
            PRODUCT_INSTRUCTIONS,
        ),
        AgentSpec(
            "SolutionArchitecture",
            "Designs production software and agent-system architecture.",
            ARCHITECT_INSTRUCTIONS,
        ),
        AgentSpec(
            "Developer",
            "Implements and verifies production software changes.",
            DEVELOPER_INSTRUCTIONS,
            tools=DEVELOPER_TOOL_NAMES,
        ),
        AgentSpec(
            "Marketing",
            "Builds go-to-market strategy and campaign assets.",
            MARKETING_INSTRUCTIONS,
        ),
        AgentSpec(
            "CustomerSuccess",
            "Creates customer support, onboarding, and retention operations.",
            CUSTOMER_SUCCESS_INSTRUCTIONS,
        ),
        AgentSpec(
            "AgentTrainer",
            "Creates new production-ready agents from simple user requests.",
            AGENT_TRAINER_INSTRUCTIONS,
        ),
    ]


def sanitize_name(value: str) -> str:
    """Normalize a user-provided agent name for OpenAI assistant creation."""
    sanitized = "".join(
        character
        for character in value.strip()
        if character.isalnum() or character in {" ", "_", "-"}
    )
    sanitized = " ".join(sanitized.split())
    if not sanitized:
        raise ValueError("Agent name is required.")
    return sanitized[:64]


def ensure_default_config(config: StudioConfig) -> StudioConfig:
    """Backfill required defaults when a config file is partial."""
    if not config.model:
        config.model = DEFAULT_MODEL
    if not config.shared_instructions:
        config.shared_instructions = PRODUCTION_SHARED_INSTRUCTIONS
    if not config.agents:
        config.agents = default_agent_specs()
    if config.agents[0].name != "CEO":
        ceo = next((agent for agent in config.agents if agent.name == "CEO"), None)
        if ceo is None:
            ceo = default_agent_specs()[0]
        config.agents = [ceo] + [
            agent for agent in config.agents if agent.name != "CEO"
        ]
    return config


def load_config(config_path: Path = DEFAULT_CONFIG_PATH) -> StudioConfig:
    """Load Agency Studio config or create an in-memory default."""
    if not config_path.exists():
        return StudioConfig(agents=default_agent_specs())

    data = json.loads(config_path.read_text(encoding="utf-8"))
    agents = [AgentSpec(**agent) for agent in data.get("agents", [])]
    return ensure_default_config(
        StudioConfig(
            model=data.get("model", DEFAULT_MODEL),
            shared_instructions=data.get(
                "shared_instructions", PRODUCTION_SHARED_INSTRUCTIONS
            ),
            agents=agents,
        )
    )


def save_config(config: StudioConfig, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
    """Persist Agency Studio config for future launches."""
    config = ensure_default_config(config)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")


def agent_specs_as_rows(specs: Iterable[AgentSpec]) -> List[List[str]]:
    """Format agent specs for Gradio tables."""
    return [
        [spec.name, spec.description, spec.model or "default", ", ".join(spec.tools)]
        for spec in specs
    ]


def create_agent_from_spec(spec: AgentSpec, default_model: str) -> Any:
    """Instantiate an Agency Swarm Agent from a serializable spec."""
    from agency_swarm import Agent
    from agency_swarm.agents.Devid.tools.ChangeFile import ChangeFile
    from agency_swarm.agents.Devid.tools.CheckCurrentDir import CheckCurrentDir
    from agency_swarm.agents.Devid.tools.CommandExecutor import CommandExecutor
    from agency_swarm.agents.Devid.tools.DirectoryNavigator import DirectoryNavigator
    from agency_swarm.agents.Devid.tools.FileMover import FileMover
    from agency_swarm.agents.Devid.tools.FileReader import FileReader
    from agency_swarm.agents.Devid.tools.FileWriter import FileWriter
    from agency_swarm.agents.Devid.tools.ListDir import ListDir
    from agency_swarm.tools.oai import CodeInterpreter, FileSearch

    developer_tools = [
        FileSearch,
        CodeInterpreter,
        FileReader,
        FileWriter,
        ChangeFile,
        CommandExecutor,
        DirectoryNavigator,
        ListDir,
        FileMover,
        CheckCurrentDir,
    ]
    model = spec.model or default_model
    tools = developer_tools if spec.name == "Developer" or "devid" in spec.tools else []
    return Agent(
        name=spec.name,
        description=spec.description,
        instructions=spec.instructions,
        tools=tools,
        model=model,
        temperature=0.2,
    )


def build_agency(
    config: StudioConfig, settings_path: Path = DEFAULT_SETTINGS_PATH
) -> Any:
    """Create the live Agency Swarm agency from config."""
    from agency_swarm import Agency

    config = ensure_default_config(config)
    agents = [create_agent_from_spec(spec, config.model) for spec in config.agents]
    ceo = agents[0]
    agency_chart = [ceo] + [[ceo, agent] for agent in agents[1:]]
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    return Agency(
        agency_chart,
        shared_instructions=config.shared_instructions,
        settings_path=str(settings_path),
        temperature=0.2,
    )


class AgencyStudio:
    """Stateful production workspace wrapper used by the UI and tests."""

    def __init__(
        self,
        config_path: Path = DEFAULT_CONFIG_PATH,
        settings_path: Path = DEFAULT_SETTINGS_PATH,
    ):
        self.config_path = config_path
        self.settings_path = settings_path
        self.config = load_config(config_path)
        self.agency: Optional[Any] = None

    @property
    def agent_names(self) -> List[str]:
        return [agent.name for agent in self.config.agents]

    def save(self) -> None:
        save_config(self.config, self.config_path)

    def build(self) -> Any:
        self.save()
        self.agency = build_agency(self.config, self.settings_path)
        return self.agency

    def add_agent(
        self, name: str, description: str, instructions: str, model: str = ""
    ) -> List[List[str]]:
        clean_name = sanitize_name(name)
        if clean_name == "CEO":
            raise ValueError("CEO already exists and cannot be replaced from the UI.")
        if any(agent.name == clean_name for agent in self.config.agents):
            raise ValueError(f"An agent named {clean_name!r} already exists.")
        if not description.strip():
            raise ValueError("Agent description is required.")
        if not instructions.strip():
            raise ValueError("Agent instructions are required.")

        self.config.agents.append(
            AgentSpec(
                name=clean_name,
                description=description.strip(),
                instructions=instructions.strip(),
                model=model.strip() or None,
            )
        )
        self.save()
        self.agency = None
        return agent_specs_as_rows(self.config.agents)

    def chat(self, message: str, recipient_name: str) -> str:
        if not message.strip():
            return "Please enter a message."
        if self.agency is None:
            self.build()
        recipient_agent = (
            self.agency._get_agent_by_name(recipient_name) if recipient_name else None
        )
        return self.agency.get_completion(
            message.strip(), recipient_agent=recipient_agent
        )


def create_ui(studio: AgencyStudio):
    """Create the production Gradio interface."""
    import gradio as gr

    with gr.Blocks(title="Agency Studio", theme=gr.themes.Soft()) as app:
        gr.Markdown(
            "# Agency Studio\n"
            "Production multi-agent workspace for building SaaS products, service agencies, "
            "marketing campaigns, customer service operations, and new trained agents."
        )
        status = gr.Markdown(
            f"**Model:** `{studio.config.model}`  |  "
            f"**Agents:** {len(studio.config.agents)}  |  "
            f"**Config:** `{studio.config_path}`"
        )

        with gr.Tab("Work with CEO"):
            recipient = gr.Dropdown(
                label="Recipient", choices=studio.agent_names, value="CEO"
            )
            chatbot = gr.Chatbot(label="Workspace", height=600)
            message = gr.Textbox(
                label="Your instruction",
                lines=5,
                placeholder="Example: Build a go-to-market plan and MVP scope for a construction estimating SaaS...",
            )
            send = gr.Button("Send", variant="primary")

            def submit(user_message, selected_recipient, history):
                history = history or []
                history.append([user_message, "Working..."])
                answer = studio.chat(user_message, selected_recipient)
                history[-1][1] = answer
                return "", history

            send.click(submit, [message, recipient, chatbot], [message, chatbot])
            message.submit(submit, [message, recipient, chatbot], [message, chatbot])

        with gr.Tab("Train / Add Agent"):
            gr.Markdown(
                "Ask AgentTrainer in the chat to design a role, then paste the resulting name, "
                "description, and instructions here to add it permanently."
            )
            agents_table = gr.Dataframe(
                headers=["Name", "Description", "Model", "Tools"],
                value=agent_specs_as_rows(studio.config.agents),
                interactive=False,
                label="Current production team",
            )
            new_name = gr.Textbox(label="Agent name")
            new_description = gr.Textbox(label="Description", lines=2)
            new_instructions = gr.Textbox(label="Instructions", lines=10)
            new_model = gr.Textbox(
                label="Model override (optional)", placeholder=studio.config.model
            )
            add = gr.Button("Add agent and save", variant="primary")
            add_result = gr.Markdown()

            def add_agent(name, description, instructions, model):
                rows = studio.add_agent(name, description, instructions, model)
                return (
                    rows,
                    f"Added `{sanitize_name(name)}`. Restart the current chat if you want a fresh conversation graph.",
                )

            add.click(
                add_agent,
                [new_name, new_description, new_instructions, new_model],
                [agents_table, add_result],
            )

        with gr.Tab("Operations"):
            gr.Markdown(
                "## Production checklist\n"
                "- Set `OPENAI_API_KEY` before launch.\n"
                "- Set `AGENCY_STUDIO_PASSWORD` to protect the UI when exposing it beyond localhost.\n"
                "- Set `AGENCY_STUDIO_MODEL` to choose a model; the default is `gpt-5.2`.\n"
                "- Keep `agency_studio_config.json` and `agency_studio_assistants.json` backed up.\n"
                "- Use a reverse proxy with HTTPS for public deployments.\n"
                "- Review all generated business, legal, financial, and deployment outputs before shipping."
            )
            rebuild = gr.Button("Save config and rebuild agency")

            def rebuild_agency():
                studio.build()
                return (
                    f"**Model:** `{studio.config.model}`  |  "
                    f"**Agents:** {len(studio.config.agents)}  |  "
                    f"**Config:** `{studio.config_path}`"
                )

            rebuild.click(rebuild_agency, outputs=status)

    return app


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Launch the production Agency Studio workspace."
    )
    parser.add_argument("--host", default=os.getenv("AGENCY_STUDIO_HOST", "127.0.0.1"))
    parser.add_argument(
        "--port", type=int, default=int(os.getenv("AGENCY_STUDIO_PORT", "7860"))
    )
    parser.add_argument(
        "--share",
        action="store_true",
        default=os.getenv("AGENCY_STUDIO_SHARE", "false").lower() == "true",
    )
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG_PATH)
    parser.add_argument("--settings", type=Path, default=DEFAULT_SETTINGS_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    return parser.parse_args()


def launch() -> None:
    args = parse_args()
    studio = AgencyStudio(args.config, args.settings)
    studio.config.model = args.model
    studio.save()
    app = create_ui(studio)

    password = os.getenv("AGENCY_STUDIO_PASSWORD")
    auth = (os.getenv("AGENCY_STUDIO_USER", "admin"), password) if password else None
    app.launch(
        server_name=args.host, server_port=args.port, share=args.share, auth=auth
    )


if __name__ == "__main__":
    launch()

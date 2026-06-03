# Examples

The best new examples and tutorials will be posted on my [YouTube Channel](https://youtube.com/@vrsen?si=GBk3V8ar6Dgemy0B).

## Agency Examples

Examples of Agencies can be found in the [agency-swarm-lab](https://github.com/VRSEN/agency-swarm-lab) repository:

- [WebDevCrafters](https://github.com/VRSEN/agency-swarm-lab/tree/main/WebDevCrafters) - Web Development Agency that builds responsive web applications using Next.js, React, and MUI.
- [CodeGuardiansAgency](https://github.com/VRSEN/agency-swarm-lab/tree/main/CodeGuardiansAgency) - Agency that runs only on the backend using github actions and submits code reviews on pull requests, according to your SOPs.
- [Agency Studio Production Workspace](../examples/ceo_agency_ui.py) - Production-ready CEO-led multi-agent workspace for SaaS/product delivery, construction estimating platforms, marketing campaigns, customer service operations, and training new agents from user requests. It includes a configurable GPT-5.2 default model, persistent agent configuration, a secured Gradio UI, production operating instructions, and an agent-training workflow.

### Running Agency Studio

Agency Studio is designed to be used as a real workspace rather than a throwaway demo. Set your API key, optionally protect the UI with a password, then launch the app:

```bash
export OPENAI_API_KEY="sk-your-key"
export AGENCY_STUDIO_PASSWORD="change-this-password"
python examples/ceo_agency_ui.py --host 127.0.0.1 --port 7860
```

Useful environment variables:

- `AGENCY_STUDIO_MODEL` - defaults to `gpt-5.2`; override if your account requires another model.
- `AGENCY_STUDIO_CONFIG` - path for persisted agent definitions; defaults to `agency_studio_config.json`.
- `AGENCY_STUDIO_SETTINGS` - path for persisted OpenAI assistant IDs; defaults to `agency_studio_assistants.json`.
- `AGENCY_STUDIO_USER` and `AGENCY_STUDIO_PASSWORD` - basic authentication for the Gradio UI.

Use the **Work with CEO** tab for project execution and the **Train / Add Agent** tab to save new specialized agents created from a simple request.

## Videos with Notebooks

- [Browsing Agent for QA Testing Agency](https://youtu.be/Yidy_ePo7pE?si=WMuWpb9_DVckIkP6) - This video shows how to use BrowsingAgent with GPT-4 vision inside a QA testing agency. It can also break captcha, as shown in [this video](https://youtu.be/qBs_50SzyBQ?si=w7e3GOhEztG8qDPE). The notebook is available [here](https://github.com/VRSEN/agency-swarm/blob/main/notebooks/web_browser_agent.ipynb).
- [Genesis Agency](https://youtu.be/qXxO7SvbGs8?si=uosmTSzzz6id_lLl) - This agency creates your agents for you. The notebook is available [here](https://github.com/VRSEN/agency-swarm/blob/main/notebooks/genesis_agency.ipynb).

### ... more coming soon

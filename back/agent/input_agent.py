from typing import Dict, Any

from agent.state import AgentState
from agent.agent import Agent


class InputAgent(Agent):
    def __init__(self, system_prompt, role, session_id=None):
        super().__init__(system_prompt, role, session_id)

    def _create_prompt(self, state: Dict[str, Any]) -> str:
        return ""

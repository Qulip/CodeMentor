from typing import Dict, Any

from agent.state import AgentState, AgentType
from base.agent import Agent


class GeneratorAgent(Agent):
    def __init__(self, session_id: str = None):
        super().__init__(
            system_prompt="당신은 숙련된 소프트웨어 엔지니어입니다. 사용자의 오류 및 관련 정보를 보고 해결 방법을 제시해주세요.",
            role=AgentType.INPUT,
            session_id=session_id,
        )

    def _create_prompt(self, state: Dict[str, Any]) -> str:

        problem_list = state["problems"]
        self.problem_idx = len(state["problems"]) - len(state["solutions"])

        problem = problem_list[self.problem_idx]
        context = state["context"][problem]

        return f"""
            다음은 사용자의 오류 입니다. 해당 오류를 보고 어떻게 해결 할 수 있을지에 대한 방법을 제시해주세요. 
            오류 : 
            '{problem}'

            오류 관련 정보 : 
            '{context}'

            답변 규칙
            - 오류 관련 정보를 참조해서 해결 방법을 제시해줘.
            - 방법은 1개 이상, 3개 이하로 제시해줘.
            - 최대한 자세하게 적어줘. 간단한 예시를 추가하면 더욱 좋을 것 같아.
            - 초심자도 이해할 수 있게 방법을 설명해줘.
            """

    def _update_answer_state(self, state: AgentState) -> AgentState:
        """
        Generator Agent 전용 추가 업데이트 메서드
        """
        response = state["response"]

        new_answer_state = state["answer_state"]

        new_answer_state["solutions"].append(response)

        return {**state, "answer_state": new_answer_state}

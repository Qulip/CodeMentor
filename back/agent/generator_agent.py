from core.agents.agent import Agent
from core.state import AgentState, AgentType, AnswerState


class GeneratorAgent(Agent):
    def __init__(self, session_id: str = None):
        super().__init__(
            system_prompt="당신은 주어진 기술 문제의 원인을 기반으로 현실적이고 실용적인 해결 방법을 상세히 제시하는 솔루션 생성 전문가입니다. 특정 기술 이슈를 해결하기 위한 최적의 접근법을 명확한 단계별 가이드 형식으로 제시하고, 이해를 돕기 위한 실용적인 팁과 모범 사례를 함께 제공하세요.",
            role=AgentType.INPUT,
            session_id=session_id,
        )

    def _create_prompt(self, state: AnswerState) -> str:

        problem_list = state["problems"]

        problem = problem_list[state["solution_count"]]
        context = state["contexts"]

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

        new_answer_state = {
            **state["answer_state"],  # 얕은 복사로 새 dict 구성
            "solution_count": state["answer_state"]["solution_count"] + 1,
            "solutions": state["answer_state"]["solutions"] + [response],
        }

        return {**state, "answer_state": new_answer_state}

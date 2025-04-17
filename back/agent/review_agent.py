from typing import Dict, Any

from core.state import AgentType
from core.agents.agent import Agent


class ReviewerAgent(Agent):
    def __init__(self, session_id: str = None):
        super().__init__(
            system_prompt="당신은 기술 문제의 최종 해결책과 관련 지식을 사용자의 숙련도(초급, 중급, 고급)에 따라 가장 이해하기 쉽고 효과적인 방식으로 요약 및 재구성하는 전문 리뷰어입니다.",
            role=AgentType.INPUT,
            session_id=session_id,
        )

    def _create_prompt(self, state: Dict[str, Any]) -> str:

        question = state["question"]

        return f"""
            다음은 사용자가 프로그래밍 관련 오류에 대해 남긴 질문과 제공한 해결방법, 추가로 학습하면 좋을 내용입니다.
            해당 내용을 사용자의 숙련도에 따라 내용을 정리해주세요.

            답변 규칙:
            - 최대한 자세하게 적고, 사용자의 숙련도에 맞는 예시가 있으면 좋다.
            - 

            숙련도: '{state["level"]}'

            질문: '{question}'

            {state.get_problem_fstring()}

            {state.get_solution_fstring()}

            {state.get_study_tips_fstring()}

            """

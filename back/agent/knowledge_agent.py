from typing import Dict, Any

from core.agents.rag_agent import RagAgent
from core.state import AgentState, AgentType
from retrieval.knowledge_retrieval_service import KnowledgeRetrievalService


class AnalyzerAgent(RagAgent):
    def __init__(self, k: int = 3, lang: str = "ko", session_id: str = None):
        super().__init__(
            system_prompt="당신은 시니어 소프트웨어 엔지니어입니다. 사용자의 오류 질문과 해결책을 보고 사용자가 추가로 학습하면 좋을 프로그래밍 및 컴퓨터 공학 지식을 제공해주는 역할을 맡고 있습니다.",
            role=AgentType.ANALYZER,
            retrieval_service=KnowledgeRetrievalService(k=k),
            lang=lang,
            session_id=session_id,
        )

    def _create_prompt(self, state: Dict[str, Any]) -> str:

        question = state["question"]
        context = state["context"]

        return f"""
            다음은 사용자가 프로그래밍 관련 오류에 대해 남긴 질문과 해결 방법입니다.
            해당 사용자가 추가로 학습하면 좋을 컴퓨터 공학 및 프로그래밍 정보을 최대 3개까지 제공해주세요.

            질문: '{question}'

            제공한 답변

            답변 규칙:
            - 검색어는 콤마로 제공 e.g.) 원인1,원인2,원인3
            - 원인만 제공하고 설명은 하지 않음.
            - 가장 적합도가 높은 순으로 나열
        """

    def _create_solution_prompt(self, state: Dict[str, Any]) -> str:

        return f"""
            
        """

    def _update_answer_state(self, state: AgentState) -> AgentState:
        """
        AnalyzerAgent 전용 추가 업데이트 메서드
        """
        response = state["response"]

        new_answer_state = state["answer_state"]

        new_answer_state["problems"] = [s.strip() for s in response.content.split(",")]
        new_answer_state["solutions"] = []

        return {**state, "answer_state": new_answer_state}

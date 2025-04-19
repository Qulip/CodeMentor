from core.agents.rag_agent import RagAgent
from core.state import AgentState, AgentType, AnswerState
from retrieval.analyzer_retrieval_service import AnalyzerRetrievalService


class AnalyzerAgent(RagAgent):
    def __init__(self, k: int = 3, lang: str = "ko", session_id: str = None):
        super().__init__(
            system_prompt="당신은 기술 문제의 근본 원인을 식별하기 위해 검색 자료를 활용하는 전문 분석 Agent입니다. 입력된 기술 문제에 대해 믿을 수 있는 외부 자료를 기반으로 하여 가능한 원인을 심층 분석하고, 명확한 근거를 바탕으로 원인을 설명하세요.",
            role=AgentType.ANALYZER,
            retrieval_service=AnalyzerRetrievalService(k=k),
            lang=lang,
            session_id=session_id,
        )

    def _create_prompt(self, state: AnswerState) -> str:

        question = state["question"]
        context = state["contexts"]

        return f"""
            다음은 사용자가 프로그래밍 관련 오류에 대해 남긴 질문입니다.
            해당 질문의 오류의 추정되는 원인을 최대 3개까지 제공해주세요.

            질문: '{question}'

            오류 관련 정보:
            '{context}'

            답변 규칙:
            - 검색어는 콤마로 제공 e.g.) 원인1,원인2,원인3
            - 원인만 제공하고 설명은 하지 않음.
            - 가장 적합도가 높은 순으로 나열
        """

    def _update_answer_state(self, state: AgentState) -> AgentState:
        """
        AnalyzerAgent 전용 추가 업데이트 메서드
        """
        response = state["response"]

        new_answer_state = state["answer_state"]

        new_answer_state["contexts"][AgentType.ANALYZER] = state["context"]
        new_answer_state["problems"] = [s.strip() for s in response.split(",")]
        new_answer_state["solutions"] = []
        new_answer_state["problem_count"] = len(new_answer_state["problems"])
        new_answer_state["solution_count"] = 0

        return {**state, "answer_state": new_answer_state}

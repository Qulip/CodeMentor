from abc import abstractmethod
from langgraph.graph import StateGraph, END

from agent.state import AgentState
from agent.agent import Agent


# RAG 에이전트 추상 클래스 정의
# TODO : 각 노드별 RAG 특수 로직 추가 여부 검토 (아직 메서드 전부 살려둠)
class RagAgent(Agent):

    #
    def __init__(
        self, system_prompt: str, role: str, k: int = 3, session_id: str = None
    ):
        super().__init__(
            system_prompt=system_prompt,
            role=role,
            session_id=session_id,
        )
        self.k = k  # 검색할 문서 개수

    def _setup_graph(self):  # 그래프 생성
        workflow = StateGraph(AgentState)

        # 노드 추가
        workflow.add_node("retrieve_context", self._retrieve_context)  # 자료 검색
        workflow.add_node("prepare_messages", self._prepare_messages)  # 메시지 준비
        workflow.add_node("generate_response", self._generate_response)  # 응답 생성
        workflow.add_node("update_state", self._update_state)  # 상태 업데이트

        # 엣지 추가 - 순차 실행 흐름
        workflow.add_edge("retrieve_context", "prepare_messages")
        workflow.add_edge("prepare_messages", "generate_response")
        workflow.add_edge("generate_response", "update_state")

        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("update_state", END)

        # 그래프 컴파일
        self.graph = workflow.compile()

    # 자료 검색
    def _retrieve_context(self, state: AgentState) -> AgentState:

        # k=0이면 검색 비활성화
        if self.k <= 0:
            return {**state, "context": ""}

        answer_state = state["answer_state"]
        question = answer_state["question"]

        # 검색 쿼리 생성
        query = self._make_query(question, "ko")

        # RAG 서비스를 통해 검색 실행
        docs = self._search_topic(question, query)  # noqa: F821

        answer_state["docs"][self.role] = (
            [doc.page_content for doc in docs] if docs else []
        )

        # 컨텍스트 포맷팅
        context = self._format_context(docs)

        # 상태 업데이트
        return {**state, "context": context}

    @abstractmethod
    def _make_query(self, question: str, lang: str = "ko") -> str:
        pass

    @abstractmethod
    def _search_topic(self, question: str, query: str) -> str:
        pass

    # 검색 결과로 Context 생성
    def _format_context(self, docs: list) -> str:

        context = ""
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown")
            section = doc.metadata.get("section", "")
            context += f"[문서 {i + 1}] 출처: {source}"
            if section:
                context += f", 섹션: {section}"
            context += f"\n{doc.page_content}\n\n"
        return context

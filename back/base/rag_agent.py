from langgraph.graph import StateGraph, END

from back.agent.state import AgentState
from back.base.agent import Agent
from back.base.retrieval_service import RetrievalService


class RagAgent(Agent):
    """
    RAG Agent 추상 클래스 정의
    기본 Agent 클래스에 검색 로직 추가
    """

    #
    def __init__(
        self,
        system_prompt: str,
        role: str,
        retrieval_service: RetrievalService,
        k: int = 3,
        lang: str = "ko",
        session_id: str = None,
    ):
        super().__init__(
            system_prompt=system_prompt,
            role=role,
            session_id=session_id,
        )
        self.k = k  # 검색할 문서 개수
        self.lang = lang
        self.retrieval_service = retrieval_service

    def _setup_graph(self):
        """
        LangGraph 워크플로우 구성:
        1. RAG 자료 검색
        2. 메시지 준비
        3. 응답 생성
        4. 상태 업데이트
        """

        workflow = StateGraph(AgentState)

        workflow.add_node("retrieve_context", self._retrieve_context)
        workflow.add_node("prepare_messages", self._prepare_messages)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("update_state", self._update_state)

        workflow.add_edge("retrieve_context", "prepare_messages")
        workflow.add_edge("prepare_messages", "generate_response")
        workflow.add_edge("generate_response", "update_state")

        workflow.set_entry_point("retrieve_context")
        workflow.add_edge("update_state", END)

        self.graph = workflow.compile()

    def _retrieve_context(self, state: AgentState) -> AgentState:
        """
        RAG 자료 검색 메서드
        """
        if self.k <= 0:
            return {**state, "context": ""}

        answer_state = state["answer_state"]
        question = answer_state["question"]

        docs = self.retrieval_service.search_question(question, self.lang, self.k)

        answer_state["docs"][self.role] = (
            [doc.page_content for doc in docs] if docs else []
        )

        context = self._format_context(docs)

        return {**state, "context": context}

    def _format_context(self, docs: list) -> str:
        """
        검색 결과로 Context 생성
        """

        context = ""
        for i, doc in enumerate(docs):
            source = doc.metadata.get("source", "Unknown")
            section = doc.metadata.get("section", "")
            context += f"[문서 {i + 1}] 출처: {source}"
            if section:
                context += f", 섹션: {section}"
            context += f"\n{doc.page_content}\n\n"
        return context

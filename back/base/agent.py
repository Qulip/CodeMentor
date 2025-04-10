from langchain.schema import HumanMessage, SystemMessage, AIMessage
from abc import ABC, abstractmethod
from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langfuse.callback import CallbackHandler

from back.utils.config import get_llm
from back.agent.state import AgentState, AnswerState


class Agent(ABC):
    """
    기본 Agent 클래스
    - 메시지 준비, 응답 생성, 상태 업데이트의 기본 워크플로우를 제공
    - 각 단계별로 Hook 메서드를 통해 에이전트별 특수 로직을 적용할 수 있음
    """

    def __init__(self, system_prompt: str, role: str, session_id: str = None):
        self.system_prompt = system_prompt
        self.role = role
        self._setup_graph()  # 그래프 설정
        self.session_id = session_id  # langfuse 세션 ID

    def _setup_graph(self):
        """
        LangGraph 워크플로우 구성:
        1. 메시지 준비
        2. 응답 생성
        3. 상태 업데이트 (커스텀 후킹)
        """
        workflow = StateGraph(AgentState)

        workflow.add_node("prepare_messages", self._prepare_messages)
        workflow.add_node("generate_response", self._generate_response)
        workflow.add_node("update_state", self._update_state)

        workflow.add_edge("prepare_messages", "generate_response")
        workflow.add_edge("generate_response", "update_state")

        workflow.set_entry_point("prepare_messages")
        workflow.add_edge("update_state", END)

        self.graph = workflow.compile()

    def _prepare_messages(self, state: AgentState) -> AgentState:
        """
        메시지 준비: 시스템 프롬프트, 기존 메시지 및 커스텀 프롬프트 조합
        """
        answer_state = state["answer_state"]

        if "context" in state:
            context = state["context"]
        else:
            context = ""

        messages = [SystemMessage(content=self.system_prompt)]

        for message in answer_state["messages"]:
            if message["role"] == "assistant":
                messages.append(AIMessage(content=message["content"]))
            else:
                messages.append(
                    HumanMessage(content=f"{message['role']}: {message['content']}")
                )

        prompt = self._create_prompt({**answer_state, "context": context})
        messages.append(HumanMessage(content=prompt))

        return {**state, "messages": messages}

    @abstractmethod
    def _create_prompt(self, state: Dict[str, Any]) -> str:
        """
        에이전트 별 프롬프트 생성 로직 (추상 메서드)
        """
        pass

    def _generate_response(self, state: AgentState) -> AgentState:
        """
        LLM 호출 및 프롬프트 응답 생성
        """
        messages = state["messages"]
        response = get_llm().invoke(messages)

        return {**state, "response": response.content}

    def _update_state(self, state: AgentState) -> AgentState:
        """
        상태 업데이트: 공통 업데이트 항목 이후 Agent별 추가 업데이트
        """
        answer_state = state["answer_state"]
        response = state["response"]
        level = state["level"]
        summary = state["summary"]
        classification = state["classification"]
        solutions = state["solutions"]

        new_answer_state = answer_state.copy()

        new_answer_state["messages"].append(
            {
                "role": self.role,
                "content": response,
                "level": level,
                "summary": summary,
                "classification": classification,
                "solutions": solutions,
            }
        )

        update_state = {**state, "answer_state": new_answer_state}

        return self._custom_update_state(update_state)

    def _custom_update_state(self, state: AgentState) -> AgentState:
        """
        Agent별 추가 업데이트를 위한 메서드
        """
        return state

    def run(self, state: AnswerState) -> AnswerState:
        """
        Agent 워크플로우 실행
        """
        agent_state = AgentState(
            answer_state=state, context="", messages=[], response=""
        )

        langfuse_handler = CallbackHandler(session_id=self.session_id)
        result = self.graph.invoke(
            agent_state, config={"callbacks": [langfuse_handler]}
        )

        return result["answer_state"]

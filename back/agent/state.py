from typing import List, Dict, Any, TypedDict
from langchain_core.messages import BaseMessage


# 에이전트 내부 상태 타입 정의
class AgentState(TypedDict):

    answer_state: Dict[str, Any]  # 전체 토론 상태
    context: str  # 검색된 컨텍스트
    messages: List[BaseMessage]  # LLM에 전달할 메시지
    response: str  # LLM 응답


class AgentType:
    INPUT = "INPUT_INTERPRETER"
    ANALYZER = "PROBLEM_ANALYZER"
    GENERATOR = "SOLUTION_GENERATOR"
    RETRIEVER = "KNOWLEDGE_RETRIEVER"
    REVIEWER = "EXPERT_REVIEWER"

    @classmethod
    def to_korean(cls, role: str) -> str:
        if role == cls.INPUT:
            return "입력분류"
        elif role == cls.ANALYZER:
            return "문제분석"
        elif role == cls.GENERATOR:
            return "해결방법"
        elif role == cls.RETRIEVER:
            return "예시검색"
        elif role == cls.REVIEWER:
            return "결과리뷰"

        else:
            return role


class AnswerState(TypedDict):
    question: str
    messages: List[Dict]
    level: str
    summary: str
    classification: Dict[str, str]
    solutions: List[str]
    docs: Dict[str, List]  # RAG 검색 결과
    contexts: Dict[str, str]  # RAG 검색 컨텍스트

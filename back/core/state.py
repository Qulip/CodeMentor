from typing import List, Dict, Any, TypedDict
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    에이전트 내부 상태 타입 정의
    - answer_state: 답변 진행 상태
    - context: 검색된 컨텍스트
    - messages: LLM에 전달할 메시지
    - response: LLM 응답
    """

    answer_state: Dict[str, Any]
    context: str
    messages: List[BaseMessage]
    response: str


class AgentType:
    """
    Agent 종류 정의
    """

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
            return "관련지식"
        elif role == cls.REVIEWER:
            return "결과리뷰"

        else:
            return role


class AnswerState(TypedDict):
    """
    답변 진행 상태 클래스
    - question: 사용자 질문
    - messages: 메시지 이력
    - level: 예측한 기술수준
    - summary: 질문 요약
    - classification: 질문 분야
    - problems: 예상 원인 리스트
    - solutions: 예상 원인 솔루션 리스트
    - docs: RAG 검색 결과
    - contexts: RAG 검색 컨텍스트
    """

    question: str
    messages: List[Dict]
    level: str
    summary: str
    classification: Dict[str, str]
    problems: List[str]
    solutions: List[str]
    docs: Dict[str, List]
    contexts: Dict[str, str]

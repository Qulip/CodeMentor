from typing import List, Dict, TypedDict

from langchain_core.messages import BaseMessage


class AnswerState(TypedDict):
    """
    답변 진행 상태 클래스
    - question: 사용자 질문
    - messages: 메시지 이력
    - answer: 질문 답변
    - level: 예측한 기술수준
    - summary: 질문 요약
    - classification: 질문 분야
    - problems: 예상 원인 리스트
    - solutions: 예상 원인 솔루션 리스트
    - study_tips: 추가 학습 추천 내용
    - docs: RAG 검색 결과
    - contexts: RAG 검색 컨텍스트
    """

    question: str
    messages: List[Dict]
    answer: str
    isNotProgramingQuestion: str
    level: str
    summary: str
    classification: Dict[str, str]
    problem_count: int
    solution_count: int
    problems: List[str]
    solutions: List[str]
    study_tips: List[Dict]
    docs: Dict[str, List]
    contexts: Dict[str, str]


class AgentState(TypedDict):
    """
    에이전트 내부 상태 타입 정의
    - answer_state: 답변 진행 상태
    - context: 검색된 컨텍스트
    - messages: LLM에 전달할 메시지
    - response: LLM 응답
    """

    answer_state: AnswerState
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
        mapping = {
            cls.INPUT: "입력분류",
            cls.ANALYZER: "문제분석",
            cls.GENERATOR: "해결방법",
            cls.RETRIEVER: "관련지식",
            cls.REVIEWER: "결과리뷰",
        }
        return mapping.get(role, role)

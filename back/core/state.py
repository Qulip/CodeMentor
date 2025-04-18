from typing import List, Dict, TypedDict

from langchain_core.messages import BaseMessage


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
    - study_tips: 추가 학습 추천 내용
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

    @classmethod
    def get_agent_finish_text(cls, role: str) -> str:
        mapping = {
            cls.INPUT: "문제의 분야와 난이도 파악을 완료했어요! 🎯",
            cls.ANALYZER: "예상되는 문제의 원인 분석이 완료됐어요! 🔍",
            cls.GENERATOR: "효과적인 해결 방법을 찾아냈어요! 💡",
            cls.RETRIEVER: "관련된 추가 학습 자료를 준비했어요! 📚",
            cls.REVIEWER: "모든 내용을 최종적으로 정리했어요! ✅",
        }
        return mapping.get(role, "아직 작업을 진행 중이에요... ⏳")

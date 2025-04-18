from datetime import datetime

from pydantic import BaseModel


# DTO 클래스 정의
class QuestionBase(BaseModel):
    """
    답변 결과 DB
    - question: 사용자 질문
    - messages: 메시지 이력(JSON)
    - level: 예측한 기술수준
    - summary: 질문 요약
    - classification: 질문 분야(JSON)
    - problems: 예상 원인 리스트(JSON)
    - solutions: 예상 원인 솔루션 리스트(JSON)
    - study_tips: 추가 학습 추천 내용(JSON)
    - docs: RAG 검색 결과(JSON)
    - created_time: 생성 시간
    """

    question: str
    messages: str
    level: str
    summary: str
    classification: str
    problems: str
    solutions: str
    study_tips: str
    docs: str


class QuestionCreate(QuestionBase):
    pass


class QuestionSchema(QuestionBase):
    created_at: datetime

    class Config:
        from_attributes = True

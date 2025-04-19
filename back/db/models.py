from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from db.database import Base


class Question(Base):
    """
    답변 결과 DB
    - question: 사용자 질문
    - answer: 질문 응답
    - level: 예측한 기술수준
    - summary: 질문 요약
    - classification: 질문 분야
    - problems: 예상 원인 리스트
    - solutions: 예상 원인 솔루션 리스트
    - study_tips: 추가 학습 추천 내용
    - docs: RAG 검색 결과
    - created_at: 생성 시간
    """

    __tablename__ = "questions"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    level = Column(String(20), nullable=False)
    summary = Column(String(255), nullable=False)
    classification = Column(Text, nullable=False)
    problems = Column(Text, nullable=False)
    solutions = Column(Text, nullable=False)
    study_tips = Column(Text, nullable=False)
    docs = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

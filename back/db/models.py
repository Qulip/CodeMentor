import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from db.database import Base


class Question(Base):
    """
    답변 결과 DB
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

    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    message = Column(Text, nullable=False)
    level = Column(String(20), nullable=False)
    summary = Column(String(255), nullable=False)
    classification = Column(Text, nullable=False)
    problems = Column(Text, nullable=False)
    solutions = Column(Text, nullable=False)
    study_tips = Column(Text, nullable=False)
    docs = Column(Text, nullable=False)
    created_time = Column(DateTime, default=datetime.datetime.now)
    updated_time = Column(DateTime, default=datetime.datetime.now)

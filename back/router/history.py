from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from db.models import Question as QuestionModel
from db.schemas import QuestionSchema, QuestionCreate

router = APIRouter(prefix="/api/v1", tags=["history"])


@router.get("/history/", response_model=List[QuestionSchema])
def read_questions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_questions = db.query(QuestionModel).offset(skip).limit(limit).all()
    return db_questions


@router.post("/history/", response_model=QuestionSchema)
def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = QuestionModel(**question.model_dump())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question


@router.get("/history/{question_id}", response_model=QuestionSchema)
def read_question(question_id: int, db: Session = Depends(get_db)):
    db_question = (
        db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    )
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    return db_question


@router.delete("/history/{question_id}")
def delete_question(question_id: int, db: Session = Depends(get_db)):
    db_question = (
        db.query(QuestionModel).filter(QuestionModel.id == question_id).first()
    )
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    db.delete(db_question)
    db.commit()
    return {"detail": "Question successfully deleted"}

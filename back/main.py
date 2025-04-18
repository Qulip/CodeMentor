import uvicorn
from fastapi import FastAPI

from db.database import Base, engine
from router import history
from router import question

Base.metadata.create_all(bind=engine)

# FastAPI 인스턴스 생성
app = FastAPI(
    title="Debate Arena API",
    description="AI Debate Arena 서비스를 위한 API",
    version="0.1.0",
)

# router 추가
app.include_router(history.router)
app.include_router(question.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

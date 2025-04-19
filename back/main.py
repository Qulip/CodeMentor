import uvicorn
from fastapi import FastAPI

from db.database import Base, engine
from router import history
from router import question

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Tech Mentor API",
    description="AI Tech Mentor 서비스 API",
    version="0.1.0",
)

# router 추가
app.include_router(history.router)
app.include_router(question.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

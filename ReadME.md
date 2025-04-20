# AI Code Mentor

## 서비스 소개 🖥

프로그래밍 관련 오류 및 질문 해결을 도와주는 AI Agent 입니다.<br>
오류 상황에 대한 해결 방법과 더불어 추가로 학습하면 좋은 내용도 같이 제공합니다.<br>
사용자의 질문의 수준에 따라 알맞는 수준의 답변을 제공합니다.<br>

## 사용 기술 🔨

### FE

`Streamlit` <br>

### BE

`Fast API` <br>
`SQLite` <br>

### AI

`Azure OpenAI` <br>
`LangChain` <br>
`LangGraph` <br>
`FAISS` <br>

## 서비스 주요 기능 설명 📚

`AI_Code_Mentor_사용설명서.pdf` 참조

## 실행방법

- pip 설치 `pip install -r requirements.txt`
- FastAPI 실행
  ```
  cd ./back
  uvicorn main:app --port=8001 --reload
  ```
- StreamLit 실행
  ```
  cd ./front
  streamlit run main.py
  ```

import json

from core.agents.agent import Agent
from core.state import AgentState, AgentType, AnswerState


class InputAgent(Agent):
    def __init__(self, session_id: str = None):
        super().__init__(
            system_prompt="당신은 숙련된 소프트웨어 엔지니어입니다. 사용자가 남긴 질문에서 기술적인 맥락을 이해하고 핵심을 요약해주는 역할을 맡고 있습니다.",
            role=AgentType.INPUT,
            session_id=session_id,
        )

    def _create_prompt(self, state: AnswerState) -> str:

        question = state["question"]

        return f"""
            다음은 사용자가 프로그래밍 관련 오류에 대해 남긴 질문입니다. 이 질문을 아래 기준에 따라 분석해주세요.
            질문 : '{question}'
            
            분석 필요 정보
            1. 분야 분류 정보
            - 도메인 (예: Backend, Frontend, DevOps 등)
            - 프레임워크/라이브러리 (예: Spring Boot, React 등)
            - 언어 (예: Python, Java 등)
            - 오류 타입 (예: 컴파일 에러, 런타임 에러 등)
            - 기타 특이사항 (예: 데이터베이스 연결, API 인증 등)

            2. 질문 요약: 사용자가 겪고 있는 문제의 핵심을 두 문장 이내로 요약해주세요. (코드나 특정 라이브러리 이름이 있다면 포함해주세요)

            3. 질문자의 기술 수준 예측: 질문에 사용된 용어 및 질문의 수준을 보고 질문자의 기술 수준을 예측하여 전달주세요.
            - Beginner: 일반 단어 사용, 질문이 포괄적
            - Intermediate: 일부 기술 용어 사용, 목적이 명확
            - Advanced: 프레임워크/도구 관련 전문 용어 사용
            
            답변 규칙
            - 질문 요약은 255자 이내로 제공한다.
            - 분류 정보는 각각 가장 일치하는 1개 만 골라야 한다.
            - 일치하는 분야가 없을 경우 답변하지 않는다. 다만, 도메인, 언어는 필수로 작성한다.
            - 답변은 Json 형태로 제공한다.(마크다운 형식 없이 바로 직렬화 가능한 Json 형태으로 제공 요망)
            (예시1:{{ 
                "summary": "Spring Boot 환경에서 JPA로 엔티티를 저장할 때 'detached entity passed to persist' 오류가 발생함.",
                "classification": {{
                    "domain": "Backend",
                    "language": "Java",
                    "framework": "Spring Boot",
                    "errorType": "런타임 에러",
                    "tags": "엔티티 매핑"
                }},
                "level": "Intermediate"
            }}
            예시2:{{ 
                "summary": "파이썬 코드를 실행했더니 SyntaxError: invalid syntax라는 오류가 뜹니다. 무슨 뜻이고 어떻게 해결하나요?",
                "classification": {{
                    "domain": "Backend",
                    "language": "Python",
                    "errorType": "런타임 에러",
                    "tags": "함수 오류"
                }},
                "level": "Beginner"
            }})
            - 만약 프로그래밍 관련 질문이 아니라면, 답변이 불가능하다 말해줘.
            (예시1: {{"isNotProgramingQuestion": "해당 질문은 프로그래밍 질문이 아니라 답변이 어렵습니다."}}
            예시2: {{"isNotProgramingQuestion": "저는 프로그래밍 질문에만 답변이 가능해요."}})
            """

    def _update_answer_state(self, state: AgentState) -> AgentState:
        """
        Input Agent 전용 추가 업데이트 메서드
        """
        response = state["response"]
        data = json.loads(response)

        new_answer_state = state["answer_state"]

        if data.get("isNotProgramingQuestion", None):
            new_answer_state["isNotProgramingQuestion"] = data[
                "isNotProgramingQuestion"
            ]
            return {**state, "answer_state": new_answer_state}

        new_answer_state["summary"] = data["summary"]
        new_answer_state["classification"] = data["classification"]
        new_answer_state["level"] = data["level"]

        return {**state, "answer_state": new_answer_state}

from typing import Dict, Any

from agent.state import AgentState, AgentType
from base.agent import Agent


class InputAgent(Agent):
    def __init__(self, session_id=None):
        super().__init__(
            "당신은 숙련된 소프트웨어 엔지니어입니다. 사용자가 남긴 질문에서 기술적인 맥락을 이해하고 핵심을 요약해주는 역할을 맡고 있습니다.",
            AgentType.INPUT,
            session_id,
        )

    def _create_prompt(self, state: Dict[str, Any]) -> str:

        question = state["question"]

        return f"""
            다음은 사용자가 프로그래밍 관련 오류에 대해 남긴 질문입니다. 이 질문을 아래 기준에 따라 분석해주세요:
            질문 : '{question}'
            
            1. 분야 분류 정보
            - 도메인 (예: Backend, Frontend, DevOps 등)
            - 프레임워크/라이브러리 (예: Spring Boot, React 등)
            - 언어 (예: Python, Java 등)
            - 오류 타입 (예: 컴파일 에러, 런타임 에러 등)
            - 기타 특이사항 (예: 데이터베이스 연결, API 인증 등)

            2. 질문 요약: 사용자가 겪고 있는 문제의 핵심을 두 문장 이내로 요약해주세요. (코드나 특정 라이브러리 이름이 있다면 포함해주세요)

            3. 답변 규칙
            - 분류 정보는 각각 가장 일치하는 1개 만 골라야 한다. 다만, 일치하는 분야가 없을 경우 답변하지 않는다.
            - 답변은 Json 형태로 제공한다.
            (예시:{{ 
                "summary": "Spring Boot 환경에서 JPA로 엔티티를 저장할 때 'detached entity passed to persist' 오류가 발생함.",
                "classification": {{
                    "domain": "Backend",
                    "framework": "Spring Boot",
                    "language": "Java",
                    "error_type": "런타임 에러",
                    "tags": "엔티티 매핑"
                }}
            }})
            """


if __name__ == "__main__":
    test = InputAgent("test")
    print(test._create_prompt({"question": "test"}))

from typing import Dict, Any
import json

from core.agents.rag_agent import RagAgent
from core.state import AgentState, AgentType
from retrieval.knowledge_retrieval_service import KnowledgeRetrievalService


class AnalyzerAgent(RagAgent):
    def __init__(self, k: int = 3, lang: str = "ko", session_id: str = None):
        super().__init__(
            system_prompt="당신은 시니어 소프트웨어 엔지니어입니다. 사용자의 오류 질문과 해결책을 보고 사용자가 추가로 학습하면 좋을 프로그래밍 및 컴퓨터 공학 지식을 제공해주는 역할을 맡고 있습니다.",
            role=AgentType.ANALYZER,
            retrieval_service=KnowledgeRetrievalService(k=k),
            lang=lang,
            session_id=session_id,
        )

    def _create_prompt(self, state: Dict[str, Any]) -> str:

        question = state["question"]
        context = state["context"]

        return f"""
            다음은 사용자가 프로그래밍 관련 오류에 대해 남긴 질문과 해결 방법입니다.
            해당 사용자가 추가로 학습하면 좋을 컴퓨터 공학 및 프로그래밍 정보을 최대 3개까지 제공해주세요.

            질문: '{question}'

            {state.get_problem_fstring()}

            {state.get_solution_fstring()}

            관련 정보:
            {context}

            답변 규칙:
            - 정보와 선택 사유을 제공.
            - 선택 사유는 100자 이내, 1~3문장으로 작성
            - 결과는 Json 배열 형태로 제공한다.
            (예시:[
                {{ 
                    "infomation": "JPA 기본 개념 및 어노테이션 학습",
                    "reason": "객체-관계 매핑 이해가 프로젝트 설계에 필수적입니다."
                }},
                {{ 
                    "infomation": "데이터 베이스 정규화",
                    "reason": "엔티티의 설계가 정규화가 부족함. 정규화를 학습하여 엔티티를 다시 설계하면 더욱 좋은 설계가 가능할 듯 함."
                }},
                {{ 
                    "infomation": "Query 메서드와 JPQL 활용",
                    "reason": "효율적인 데이터 조회 및 동적 쿼리 구현에 유용합니다."
                }},
            ])
            - 가장 적합도가 높은 순으로 나열
        """

    def _update_answer_state(self, agent_state: AgentState) -> AgentState:
        """
        KnowledgeAgent 전용 추가 업데이트 메서드
        - study_tips
        """
        response = agent_state["response"]
        data = json.loads(response)

        new_answer_state = agent_state["answer_state"]

        new_answer_state["study_tips"] = data

        return {**agent_state, "answer_state": new_answer_state}

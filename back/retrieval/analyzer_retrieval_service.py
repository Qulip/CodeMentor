from typing import Dict, List
from langchain.schema import HumanMessage, SystemMessage

from base.retrieval_service import RetrievalService
from utils.config import get_llm


class AnalyzerRetrievalService(RetrievalService):
    def __init__(self, k: int = 3):
        super().__init__(k=k)

    def _get_search_keyword_from_question(
        self, summary: str, classification: Dict[str, str]
    ) -> List[str]:

        prompt = f"""
        다음은 사용자가 남긴 프로그래밍 오류 질문입니다. 해당 오류를 웹 검색을 통해 해결하고자 합니다. 웹 검색에 적합한 검색어 3개를 제안해주세요. 
        조건:
        - 각 검색어는 25자 이내로 제한
        - 검색어는 콤마로 제공 e.g.) 검색어1,검색어2,검색어3
        - 검색어만 제공하고 설명은 하지 않음.
        - 가장 적합도가 높은 순으로 나열

        질문:
        '{summary}'

        추가정보:
        - 분야: '{classification["domain"]}'
        - 사용 언어: '{classification["language"]}'
        """

        self._add_additional_info(prompt, classification)

        messages = [
            SystemMessage(
                content="당신은 웹 검색 전문가입니다. 주어진 프로그래밍 오류 상황에 대한 해결책을 가장 올바르게 제공해 줄 것 같은 검색어를 제안해주세요."
            ),
            HumanMessage(content=prompt),
        ]

        llm_response = get_llm().invoke(messages)

        result = [s.strip() for s in llm_response.content.split(",")]

        return result[:3]

    def _make_query(
        self, summary: str, classification: Dict[str, str], lang: str = "ko"
    ) -> str:
        """
        검색 쿼리 생성 메서드(추상 메서드)
        """

        prompt = f"""
        다음은 사용자가 남긴 프로그래밍 오류 질문입니다.
        이 질문에 맞는 벡터 검색 쿼리를 생성해주세요.
        조건:
        - 백터 검색 쿼리 언어: '{lang}'
        - 사용자의 질문의 핵심 오류 상황을 요약
        - 관련 라이브러리, 프레임워크, 언어, 오류 메시지를 포함
        - 쿼리만 제공하고 설명은 하지 않음.
        - 자연어 문장이나 키워드 위주로도 좋음.

        질문:
        '{summary}'

        추가정보:
        - 분야: '{classification["domain"]}'
        - 사용 언어: '{classification["language"]}'
        """

        self._add_additional_info(prompt, classification)

        messages = [
            SystemMessage(
                content="당신은 벡터 검색 전문가입니다. 사용자의 질문과 추가 정보를 보고 가장 효과적인 벡터 검색이 가능한 벡터 검색 쿼리를 생성해주세요."
            ),
            HumanMessage(content=prompt),
        ]

        llm_response = get_llm().invoke(messages)
        return llm_response.content

    def _add_additional_info(prompt: str, classification: Dict[str, str]) -> str:
        additional_info = []

        if classification.get("framework"):
            additional_info.append(f"- 프레임워크: '{classification['framework']}'")
        if classification.get("errorType"):
            additional_info.append(f"- 에러 타입: '{classification['errorType']}'")
        if classification.get("tags"):
            additional_info.append(f"- 태그: '{classification['tags']}'")

        if additional_info:
            prompt += "\n" + "\n".join(additional_info)

        return prompt

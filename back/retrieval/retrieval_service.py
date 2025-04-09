from abc import ABC, abstractmethod
from typing import List
from duckduckgo_search import DDGS
from langchain.schema import Document


class RetrievalService(ABC):
    """
    검색 및 벡터 스토어 관련 로직 클래스
    - 각 Agent별 구현
    """

    def __init__(self, k: int = 3):
        self.k = k

    @abstractmethod
    def get_search_keyword_from_question(self, question: str) -> List[str]:
        """
        질문 기반으로 검색할 키워드 생성 메서드(추상 메서드)
        """
        pass

    def get_search_content(
        improved_queries: str,
        language: str = "ko",
        max_results: int = 5,
    ) -> List[Document]:

        try:
            documents = []

            ddgs = DDGS()

            # 각 개선된 검색어에 대해 검색 수행
            for query in improved_queries:
                try:
                    # 검색 수행
                    results = ddgs.text(
                        query,
                        region=language,
                        safesearch="moderate",
                        timelimit="y",  # 최근 1년 내 결과
                        max_results=max_results,
                    )

                    if not results:
                        continue

                    # 검색 결과 처리
                    for result in results:
                        title = result.get("title", "")
                        body = result.get("body", "")
                        url = result.get("href", "")

                        if body:
                            documents.append(
                                Document(
                                    page_content=body,
                                    metadata={
                                        "source": url,
                                        "section": "content",
                                        "topic": title,
                                        "query": query,
                                    },
                                )
                            )

                except Exception as e:
                    documents = []

            return documents

        except Exception as e:
            return []

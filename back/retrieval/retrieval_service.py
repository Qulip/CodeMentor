from abc import ABC, abstractmethod
from langchain_community.vectorstores import FAISS
from typing import Any, Dict, Optional, List
from duckduckgo_search import DDGS
from langchain.schema import Document

from utils.config import get_embeddings


class RetrievalService(ABC):
    """
    검색어 추출 및 검색 로직 클래스
    - 각 Agent별 구현
    """

    def __init__(self, k: int = 3):
        self.k = k

    @abstractmethod
    def _get_search_keyword_from_question(self, question: str) -> List[str]:
        """
        질문 기반으로 검색할 키워드 생성 메서드(추상 메서드)
        """
        pass

    def _get_search_content(
        improved_queries: str,
        language: str = "ko",
        max_results: int = 5,
    ) -> List[Document]:
        """
        DuckDuckGo를 통한 검색 메서드
        - docs: https://pypi.org/project/duckduckgo-search/
        """

        try:
            documents = []

            ddgs = DDGS()
            for query in improved_queries:
                try:
                    results = ddgs.text(
                        query,
                        region=language,
                        safesearch="moderate",
                        # timelimit="y",  # 최근 1년 내 결과
                        max_results=max_results,
                    )

                    if not results:
                        continue

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
                # TODO: exception 처리 방법 연구 필요
                except Exception as e:
                    documents = []

            return documents

        except Exception as e:
            return []

    def _get_vector_store_from_search_result(
        self, question: str, lang: str = "ko"
    ) -> Optional[FAISS]:
        """
        검색 및 검색 결과를 통해 벡터 스토어 생성 메서드
        """

        search_keyword = self._get_search_keyword_from_question(question)
        seach_result = self._get_search_content(search_keyword, lang)
        if not seach_result:
            return None
        try:
            return FAISS.from_documents(seach_result, get_embeddings())
        except Exception as e:
            # TODO: exception 처리 방법 연구 필요
            return None

    @abstractmethod
    def _make_query(self, question: str, lang: str = "ko") -> str:
        """
        검색 쿼리 생성 메서드(추상 메서드)
        """
        pass

    def search_question(
        self, question: str, lang: str = "ko", k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        벡터 스토어에서 문서를 검색해 Similarity Search 진행 메서드
        """

        vector_store = self._get_vector_store_from_search_result(question, lang)
        query = self._make_query(question, lang)

        if not vector_store:
            return []
        try:
            return vector_store.similarity_search(query, k=k)
        # TODO: exception 처리 방법 연구 필요
        except Exception as e:
            return []


if __name__ == "__main__":
    """
    DuckDuckGo 검색 메서드 테스트
    """
    test = RetrievalService
    print(test.get_search_content("Spring Boot Dispatcher Servlet", "en", 5))
    # 영어로 검색하니 검색 시간이 한글보다 소요됨.

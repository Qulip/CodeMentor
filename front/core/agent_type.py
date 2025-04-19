class AgentType:
    """
    Agent 종류 정의
    """

    INPUT = "INPUT_INTERPRETER"
    ANALYZER = "PROBLEM_ANALYZER"
    GENERATOR = "SOLUTION_GENERATOR"
    RETRIEVER = "KNOWLEDGE_RETRIEVER"
    REVIEWER = "EXPERT_REVIEWER"

    @classmethod
    def to_korean(cls, role: str) -> str:
        mapping = {
            cls.INPUT: "입력분류",
            cls.ANALYZER: "문제분석",
            cls.GENERATOR: "해결방법",
            cls.RETRIEVER: "관련지식",
            cls.REVIEWER: "결과리뷰",
        }
        return mapping.get(role, role)
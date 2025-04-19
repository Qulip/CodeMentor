from langgraph.graph import StateGraph, END

from agent.analyzer_agent import AnalyzerAgent
from agent.generator_agent import GeneratorAgent
from agent.input_agent import InputAgent
from agent.retriever_agent import RetrieverAgent
from agent.review_agent import ReviewerAgent
from core.state import AnswerState, AgentType


def create_agent_graph(k: int = 3, session_id: str = ""):

    workflow = StateGraph(AnswerState)

    input_agent = InputAgent(session_id=session_id)
    analyzer_agent = AnalyzerAgent(k=k, session_id=session_id)
    generator_agent = GeneratorAgent(session_id=session_id)
    retriever_agent = RetrieverAgent(k=k, session_id=session_id)
    reviewer_agent = ReviewerAgent(session_id=session_id)

    workflow.add_node(AgentType.INPUT, input_agent.run)
    workflow.add_node(AgentType.ANALYZER, analyzer_agent.run)
    workflow.add_node(AgentType.GENERATOR, generator_agent.run)
    workflow.add_node(AgentType.RETRIEVER, retriever_agent.run)
    workflow.add_node(AgentType.REVIEWER, reviewer_agent.run)

    workflow.set_entry_point(AgentType.INPUT)

    workflow.add_edge(AgentType.INPUT, AgentType.ANALYZER)
    workflow.add_conditional_edges(
        AgentType.INPUT,
        _is_question_about_programing,
        [END, AgentType.ANALYZER],
    )
    workflow.add_edge(AgentType.ANALYZER, AgentType.GENERATOR)

    workflow.add_conditional_edges(
        AgentType.GENERATOR,
        _is_solution_generate_end,
        [AgentType.RETRIEVER, AgentType.GENERATOR],
    )

    workflow.add_edge(AgentType.RETRIEVER, AgentType.REVIEWER)
    workflow.add_edge(AgentType.REVIEWER, END)

    return workflow.compile()


def _is_question_about_programing(state: AnswerState):
    if state.get("isNotProgramingQuestion", None):
        return END
    return AgentType.ANALYZER


def _is_solution_generate_end(state: AnswerState):
    if state["problem_count"] <= state["solution_count"]:
        return AgentType.RETRIEVER

    return AgentType.GENERATOR


if __name__ == "__main__":

    graph = create_agent_graph(3, "")

    graph_image = graph.get_graph().draw_mermaid_png()

    output_path = "../agent_graph.png"
    with open(output_path, "wb") as f:
        f.write(graph_image)

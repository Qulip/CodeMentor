from langgraph.graph import StateGraph, END

from core.state import AnswerState, AgentType
from agent.input_agent import InputAgent, GeneratorAgent, AnalyzerAgent


# TODO: Agent 추가 및 node, edge 추가 필요
def create_agent_graph(k: int = 3, session_id: str = ""):

    workflow = StateGraph(AnswerState)

    input_agent = InputAgent(k=k, session_id=session_id)
    analyzer_agent = AnalyzerAgent(k=k, session_id=session_id)
    generator_agent = GeneratorAgent(k=k, session_id=session_id)

    workflow.add_node(AgentType.INPUT, input_agent.run)
    workflow.add_node(AgentType.ANALYZER, analyzer_agent.run)
    workflow.add_node(AgentType.GENERATOR, generator_agent.run)

    workflow.add_edge(AgentType.INPUT, AgentType.ANALYZER)
    workflow.add_edge(AgentType.ANALYZER, AgentType.GENERATOR)

    workflow.add_conditional_edges(
        AgentType.GENERATOR,
        _is_solution_generate_end,
        [AgentType.RETRIEVER, AgentType.GENERATOR],
    )

    workflow.add_edge(AgentType.RETRIEVER, AgentType.REVIEWER)
    workflow.add_edge(AgentType.RETRIEVER, END)

    return workflow.compile


def _is_solution_generate_end(state: AnswerState):
    problem_list = state["problems"]
    solution_list = state["solutions"]

    if len(problem_list) == len(solution_list):
        return AgentType.RETRIEVER

    return AgentType.GENERATOR


if __name__ == "__main__":

    graph = create_agent_graph(3, "")

    graph_image = graph.get_graph().draw_mermaid_png()

    output_path = "agent_graph.png"
    with open(output_path, "wb") as f:
        f.write(graph_image)

    import subprocess

    subprocess.run(["open", output_path])

import asyncio
import json
import uuid
from typing import Any

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from langfuse.callback import CallbackHandler
from pydantic import BaseModel

from core.state import AnswerState
from graph.graph import create_agent_graph
from utils.string import get_agent_finish_text

router = APIRouter(
    prefix="/api/v1/question",
    tags=["question"],
    responses={404: {"description": "Not Found"}},
)


class QuestionRequest(BaseModel):
    question: str
    max_search: int = 3


class QuestionResponse(BaseModel):
    status: str = "success"
    result: Any = None


@router.post("/stream")
async def stream_question_workflow(request: QuestionRequest):
    question = request.question
    max_search = request.max_search

    session_id = str(uuid.uuid4())
    answer_graph = create_agent_graph(max_search, session_id)

    initial_state: AnswerState = {
        "question": question,
        "answer": "",
        "level": "",
        "summary": ",",
        "classification": {},
        "problems": [],
        "solutions": [],
        "study_tips": [],
        "docs": {},
    }

    langfuse_handler = CallbackHandler(session_id=session_id)

    # 스트리밍 응답 반환
    return StreamingResponse(
        answer_generator(answer_graph, initial_state, langfuse_handler),
        media_type="text/event-stream",
    )


async def answer_generator(answer_graph, initial_state, langfuse_handler):
    for chunk in answer_graph.stream(
        initial_state,
        config={"callbacks": [langfuse_handler]},
        subgraphs=True,
        stream_mode="updates",
    ):
        if not chunk:
            continue

        node = chunk[0] if len(chunk) > 0 else None
        if not node or node == ():
            continue

        node_name = node[0]
        role = node_name.split(":")[0]
        subgraph = chunk[1]
        subgraph_node = subgraph.get("update_state", None)

        if subgraph_node:
            response = subgraph_node.get("response", None)
            answer_state = subgraph_node.get("answer_state", None)

            finish_text = get_agent_finish_text(role)
            state = {
                "question": answer_state.get("question", []),
                "answer": answer_state.get("answer", ""),
                "level": answer_state.get("level", ""),
                "summary": answer_state.get("summary", ""),
                "classification": answer_state.get("classification", {}),
                "problems": answer_state.get("problems", []),
                "solutions": answer_state.get("solutions", []),
                "study_tips": answer_state.get("study_tips", []),
                "docs": answer_state.get("docs", {}),
            }
            event_data = {
                "type": "update",
                "data": {
                    "role": role,
                    "finish_text": finish_text,
                    "state": state,
                },
            }
            yield f"data: {json.dumps(event_data, ensure_ascii=False)}\n\n"
            print(event_data)

            await asyncio.sleep(0.01)

    yield f"data: {json.dumps({'type': 'end', 'data': {}}, ensure_ascii=False)}\n\n"

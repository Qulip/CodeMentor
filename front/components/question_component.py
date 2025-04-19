import json

import streamlit as st

from api.history_api import save_question
from api.question_api import fetch_and_stream_answer
from core.agent_type import AgentType
from utils.component_util import render_source_materials
from utils.state_manager import reset_session_state
from utils.str_util import json_to_str


def start_asking_question():
    question = st.session_state.question
    data = {
        "question": question,
    }

    status = st.empty()

    with st.spinner(""):

        fetch_and_stream_answer(data, status)


def process_sse_stream(response, status: st.delta_generator):
    for chunk in response.iter_lines():
        if not chunk:
            continue

        line = chunk.decode("utf-8")

        if not line.startswith("data: "):
            continue

        data_str = line[6:]

        try:
            event_data = json.loads(data_str)

            is_complete = handle_event(event_data, status)

            if is_complete:
                break

        except json.JSONDecodeError as e:
            st.error(f"JSON 파싱 오류: {e}")


def handle_event(event_data, status: st.delta_generator):

    if event_data.get("type") == "end":
        return True

    if event_data.get("type") == "update":
        data = event_data.get("data", {})
        role = data.get("role")
        question = data.get("question")
        answer = data.get("answers")
        level = data.get("level")
        summary = data.get("summary")
        classification = data.get("classification")
        problems = data.get("problems")
        solutions = data.get("solutions")
        study_tips = data.get("study_tips")
        docs = data.get("docs", {})
        not_programing_question_answer = data.get("isNotProgramingQuestion", None)

        finish_text = data.get("finish_text")
        status.text(finish_text)

        if role == AgentType.INPUT:
            if not_programing_question_answer:
                if len(not_programing_question_answer) > 0:
                    answer = not_programing_question_answer
                    st.session_state.answer = answer

                    return True

        if role == AgentType.REVIEWER:
            st.session_state.app_mode = "results"
            st.session_state.viewing_history = False
            st.session_state.answer = answer
            st.session_state.docs = docs

            with st.chat_message(role, avatar="🖥"):
                st.markdown(finish_text)

            question_data = {
                "question": question,
                "answer": answer,
                "level": level,
                "summary": summary,
                "classification": json_to_str(classification),
                "problems": json_to_str(problems),
                "solutions": json_to_str(solutions),
                "study_tips": json_to_str(study_tips),
                "docs": json_to_str(docs),
            }
            save_question(question_data)

            render_source_materials()

            if st.button("새 질문 시작"):
                reset_session_state()
                st.session_state.app_mode = "input"
                st.rerun()

    return False

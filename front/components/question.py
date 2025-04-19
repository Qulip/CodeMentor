import json

import streamlit as st

from api.history import save_question
from api.question import stream_question


def start_question():
    question = st.session_state.question
    data = {
        "question": question,
    }

    status = st.empty()

    with st.spinner("답변 생성 중입니다... 완료까지 잠시 기다려주세요."):

        stream_question(data, status)


def process_streaming_response(response, status: st.delta_generator):
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

        finish_text = data.get("finish_text")
        status.text(finish_text)

        if role == AgentType.JUDGE:
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
                "classification": _json_to_str(classification),
                "problems": _json_to_str(problems),
                "solutions": _json_to_str(solutions),
                "study_tips": _json_to_str(study_tips),
                "docs": _json_to_str(docs),
            }
            # TODO: 인자 수정
            save_question(question_data)

            # 참고 자료 표시
            if st.session_state.docs:
                render_source_materials()

            if st.button("새 토론 시작"):
                reset_session_state()
                st.session_state.app_mode = "input"
                st.rerun()

    return False

from typing import Dict, Any

import streamlit as st

from api.history_api import (
    fetch_question_history,
    fetch_question_by_id,
    delete_question_by_id,
    delete_all_question_history,
)
from utils.state_manager import reset_session_state


def render_history_ui():
    # st.form_submit_button(
    #     "새로운 질문 하기",
    #     on_click=lambda: st.session_state.update({"app_mode": "question"}),
    # )
    if st.button("새 토론 시작"):
        reset_session_state()
        st.session_state.app_mode = "input"
        st.rerun()

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("이력 새로고침", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("전체 이력 삭제", type="primary", use_container_width=True):
            if delete_all_question_history():
                st.rerun()

    # 토론 이력 로드
    question_history = fetch_question_history()

    if not question_history:
        st.info("저장된 토론 이력이 없습니다.")
    else:
        render_history_list(question_history)


# 토론 이력 목록 렌더링
def render_history_list(question_history):
    for id, summary, created_at, level in question_history:
        with st.container(border=True):

            st.write(f"***{summary}***")

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.caption(f"날짜: {created_at} | 예측 난이도: {level}")

            with col2:
                if st.button("보기", key=f"view_{id}", use_container_width=True):
                    question, summary, answer, docs = fetch_question_by_id(id)
                    if question and answer:
                        st.session_state.viewing_history = True
                        st.session_state.loaded_question = question
                        st.session_state.loaded_summary = summary
                        st.session_state.loaded_answer = answer
                        st.session_state.loaded_question_id = id
                        st.session_state.docs = docs
                        st.session_state.app_mode = "results"
                        st.rerun()

            with col3:
                if st.button("삭제", key=f"del_{id}", use_container_width=True):
                    if delete_question_by_id(id):
                        reset_session_state()
                        st.rerun()


def render_sidebar() -> Dict[str, Any]:
    with st.sidebar:
        render_history_ui()

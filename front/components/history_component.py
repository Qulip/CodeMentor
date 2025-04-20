import streamlit as st

from core.agent_type import AgentType
from utils.component_util import render_source_materials


def display_question_results():

    if st.session_state.viewing_history:
        st.info("📚 이전에 저장된 답변 이력을 보고 있습니다.")
        question = st.session_state.loaded_question
        summary = st.session_state.loaded_summary
        answer = st.session_state.loaded_answer
    else:
        question = st.session_state.ui_question
        summary = st.session_state.summary
        answer = st.session_state.answer

    with st.chat_message("USER", avatar="🙋‍♀️"):
        st.markdown(question)
    with st.chat_message(AgentType.REVIEWER, avatar="💻"):
        st.markdown(answer)

    st.session_state.question_active = False
    st.session_state.viewing_history = True

    if st.session_state.docs:
        render_source_materials()

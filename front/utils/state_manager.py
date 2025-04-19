import streamlit as st


def init_session_state():
    """
    Streamlit 세션 스테이트 초기화
    """
    if "app_mode" not in st.session_state:
        reset_session_state()


def reset_session_state():
    """
    Streamlit 세션 스테이트 리셋 메서드
    """
    st.session_state.app_mode = False
    st.session_state.viewing_history = False
    st.session_state.loaded_question_id = None
    st.session_state.docs = {}

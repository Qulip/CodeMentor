import streamlit as st


def init_session_state():
    """
    Streamlit 세션 스테이트 초기화
    """
    if "app_mode" not in st.session_state:
        reset_session_state(True)


def reset_session_state(init: bool = False):
    """
    Streamlit 세션 스테이트 리셋 메서드
    """
    st.session_state.app_mode = False
    st.session_state.viewing_history = False
    st.session_state.loaded_question_id = None
    st.session_state.docs = {}
    st.session_state.docs_init_question = (
        "Python 프로젝트에서 'most likely due to a circular import' 오류가 발생하는데 원인이 뭘까?"
        if init
        else ""
    )

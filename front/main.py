import streamlit as st

from components.history_component import display_question_results
from components.question_component import start_asking_question
from components.sidebar import render_sidebar
from utils.state_manager import init_session_state


def render_ui():
    # 페이지 설정
    st.set_page_config(page_title="Code Mentor", page_icon="💻")

    # 제목 및 소개
    st.title("💻 AI Code Mentor")
    st.markdown(
        """
        ### 프로젝트 소개
        이 애플리케이션은 AI 에이전트가 사용자가 제시한 프로그래밍 오류 질문에 대해 예상 원인, 답변, 추천 학습 내용을 제공해줍니다.
        질문을 상세하게, 용어를 많이 사용할 경우 질문의 답변이 향상될 수 있습니다.
        여러 질문을 던져보세요!
        """
    )
    with st.form("question_form", border=False):
        st.text_area(
            label="프로그래밍 오류에 대한 질문을 입력해주세요.:",
            value=st.session_state.docs_init_question,
            key="ui_question",
            height=100,
        )
        st.form_submit_button(
            "제출",
            on_click=lambda: st.session_state.update({"app_mode": "question"}),
        )
    render_sidebar()

    current_mode = st.session_state.app_mode
    print(current_mode)

    if current_mode == "question":
        start_asking_question()
    elif current_mode == "results":
        display_question_results()


if __name__ == "__main__":
    # 세션 상태 초기화
    init_session_state()

    render_ui()

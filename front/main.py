import streamlit as st

from components.sidebar import render_sidebar
from utils.state_manager import init_session_state, reset_session_state


# 참고 자료 표시
def render_source_materials():

    with st.expander("사용된 참고 자료 보기"):
        st.subheader("찬성 측 참고 자료")
        for i, doc in enumerate(st.session_state.docs.get(AgentType.PRO, [])[:3]):
            st.markdown(f"**문서 {i+1}**")
            st.text(doc[:300] + "..." if len(doc) > 300 else doc)
            st.divider()

        st.subheader("반대 측 참고 자료")
        for i, doc in enumerate(st.session_state.docs.get(AgentType.CON, [])[:3]):
            st.markdown(f"**문서 {i+1}**")
            st.text(doc[:300] + "..." if len(doc) > 300 else doc)
            st.divider()

        st.subheader("심판 측 참고 자료")
        for i, doc in enumerate(st.session_state.docs.get(AgentType.JUDGE, [])[:3]):
            st.markdown(f"**문서 {i+1}**")
            st.text(doc[:300] + "..." if len(doc) > 300 else doc)
            st.divider()


def display_debate_results():

    if st.session_state.viewing_history:
        st.info("📚 이전에 저장된 토론을 보고 있습니다.")
        topic = st.session_state.loaded_topic
    else:
        topic = st.session_state.ui_topic

    # 토론 주제 표시
    st.header(f"토론 주제: {topic}")

    for message in st.session_state.messages:

        role = message["role"]
        if role not in [
            AgentType.PRO,
            AgentType.CON,
            AgentType.JUDGE,
        ]:
            continue

        if message["role"] == AgentType.PRO:
            avatar = "🙆🏻‍♀️"
        elif message["role"] == AgentType.CON:
            avatar = "🙅🏻‍♂"
        elif message["role"] == AgentType.JUDGE:
            avatar = "👩🏻‍⚖️"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    if role == AgentType.JUDGE:
        st.session_state.debate_active = True
        st.session_state.viewing_history = False

    # 참고 자료 표시
    if st.session_state.docs:
        render_source_materials()

    if st.button("새 토론 시작"):
        reset_session_state()
        st.session_state.app_mode = "input"
        st.rerun()


def render_ui():
    # 페이지 설정
    st.set_page_config(page_title="AI 토론", page_icon="🤖")

    # 제목 및 소개
    st.title("🤖 AI 토론 - 멀티 에이전트")
    st.markdown(
        """
        ### 프로젝트 소개
        이 애플리케이션은 3개의 AI 에이전트(찬성, 반대, 심판)가 사용자가 제시한 주제에 대해 토론을 진행합니다.
        각 AI는 서로의 의견을 듣고 반박하며, 마지막에는 심판 AI가 토론 결과를 평가합니다.
        """
    )

    render_sidebar()

    current_mode = st.session_state.app_mode

    if current_mode == "debate":
        start_debate()
    elif current_mode == "results":
        display_debate_results()


if __name__ == "__main__":
    # 세션 상태 초기화
    init_session_state()

    render_ui()

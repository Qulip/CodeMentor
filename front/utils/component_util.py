import streamlit as st

from core.agent_type import AgentType

def render_source_materials():
    """
    참고 자료 노출 메서드
    """
    with st.expander("사용된 참고 자료 보기"):
        st.subheader("원인 및 해결 방법 참고 자료")
        _docs_to_streamlit(AgentType.ANALYZER)

        st.subheader("추가 학습 내용 참고 자료")
        _docs_to_streamlit(AgentType.RETRIEVER)

def _docs_to_streamlit(agent_type: str):
    """
    에이전트 타입별 참고자료 Streamlit 노출 메서드
    :param agent_type: 에이전트 타입
    """
    for i, doc in enumerate(st.session_state.docs.get(agent_type, [])[:3]):
        st.markdown(f"**문서 {i + 1}**")
        st.text(doc[:300] + "..." if len(doc) > 300 else doc)
        st.divider()

import json

import requests
import streamlit as st
from utils.state_manager import reset_session_state

from utils.config import API_BASE_URL


# id: int
# question: str
# messages: str
# level: str
# summary: str
# classification: str
# problems: str
# solutions: str
# study_tips: str
# docs: str


def fetch_question_history():
    """
    질문 이력 조회 API 메서드
    """
    try:
        response = requests.get(f"{API_BASE_URL}/history/")
        if response.status_code == 200:
            question_list = response.json()
            return [
                (
                    question["id"],
                    question["summary"],
                    question["created_at"],
                )
                for question in question_list
            ]
        else:
            st.error(f"질문 이력 조회 실패: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return []


def fetch_question_by_id(question_id):
    """
    질문 상세 조회 API 메서드
    - question_id: 질문 ID
    """
    try:
        response = requests.get(f"{API_BASE_URL}/history/{question_id}")
        if response.status_code == 200:
            question_info = response.json()
            question = question_info["question"]

            messages = (
                json.loads(question_info["messages"])
                if isinstance(question_info["messages"], str)
                else question_info["messages"]
            )
            docs = (
                json.loads(question_info["docs"])
                if isinstance(question_info["docs"], str)
                else question_info.get("docs", {})
            )
            return question, messages, docs
        else:
            st.error(f"데이터 조회 실패: {response.status_code}")
            return None, None, None
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return None, None, None


def delete_question_by_id(question_id):
    """
    질문 데이터 삭제(단건) API 메서드
    - question_id: 질문 ID
    """
    try:
        response = requests.delete(f"{API_BASE_URL}/history/{question_id}")
        if response.status_code == 200:
            st.success("질문 이력이 삭제되었습니다.")
            return True
        else:
            st.error(f"질문 이력 삭제 실패: {response.status_code}")
            return False
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return False


def delete_all_question_list():
    """
    질문 데이터 삭제(전체) API 메서드
    """
    try:
        question_list = fetch_question_history()
        if not question_list:
            return True

        success = True
        for question_id, _, _, _ in question_list:
            response = requests.delete(f"{API_BASE_URL}/history/{question_id}")
            if response.status_code != 200:
                success = False

        if success:
            st.success("모든 질문 이력 삭제에 성공하였습니다.")
        return success
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return False


def save_question(topic, rounds, messages, docs=None):
    """
    질문 데이터 저장 API 메서드
    """
    try:
        # API 요청 데이터 준비
        debate_data = {
            "topic": topic,
            "rounds": rounds,
            "messages": (
                json.dumps(messages) if not isinstance(messages, str) else messages
            ),
            "docs": (
                json.dumps(docs)
                if docs and not isinstance(docs, str)
                else (docs or "{}")
            ),
        }

        response = requests.post(f"{API_BASE_URL}/debates/", json=debate_data)

        if response.status_code == 200 or response.status_code == 201:
            st.success("토론이 성공적으로 저장되었습니다.")
            return response.json().get("id")  # 저장된 토론 ID 반환
        else:
            st.error(f"토론 저장 실패: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return None


# 토론 이력 UI 렌더링
def render_history_ui():

    col1, col2 = st.columns([1, 1])

    with col1:
        if st.button("이력 새로고침", use_container_width=True):
            st.rerun()

    with col2:
        if st.button("전체 이력 삭제", type="primary", use_container_width=True):
            if delete_all_debates():
                st.rerun()

    # 토론 이력 로드
    debate_history = fetch_debate_history()

    if not debate_history:
        st.info("저장된 토론 이력이 없습니다.")
    else:
        render_history_list(debate_history)


# 토론 이력 목록 렌더링
def render_history_list(debate_history):
    for id, topic, date, rounds in debate_history:
        with st.container(border=True):

            # 토론 주제
            st.write(f"***{topic}***")

            col1, col2, col3 = st.columns([3, 1, 1])
            # 토론 정보
            with col1:
                st.caption(f"날짜: {date} | 라운드: {rounds}")

            # 보기 버튼
            with col2:
                if st.button("보기", key=f"view_{id}", use_container_width=True):
                    topic, messages, docs = fetch_debate_by_id(id)
                    if topic and messages:
                        st.session_state.viewing_history = True
                        st.session_state.messages = messages
                        st.session_state.loaded_topic = topic
                        st.session_state.loaded_debate_id = id
                        st.session_state.docs = docs
                        st.session_state.app_mode = "results"
                        st.rerun()

            # 삭제 버튼
            with col3:
                if st.button("삭제", key=f"del_{id}", use_container_width=True):
                    if delete_debate_by_id(id):
                        reset_session_state()
                        st.rerun()

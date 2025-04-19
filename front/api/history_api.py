import json

import requests
import streamlit as st

from utils.config import API_BASE_URL


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
                    question["level"],
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

    Args:
        question_id: 질문 ID
    """
    try:
        response = requests.get(f"{API_BASE_URL}/history/{question_id}")
        if response.status_code == 200:
            question_info = response.json()

            question = question_info["question"]
            summary = question_info["summary"]
            answer = question_info["answer"]
            docs = json.loads(question_info["docs"])
            return question, summary, answer, docs
        else:
            st.error(f"데이터 조회 실패: {response.status_code}")
            return None, None, None
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return None, None, None


def delete_question_by_id(question_id):
    """
    질문 데이터 삭제(단건) API 메서드

    Args:
        question_id: 질문 ID
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


def delete_all_question_history():
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


def save_question(question_data: dict[str:str]):
    """
    질문 데이터 저장 API 메서드

    :param question_data: 답변 데이터
    """
    try:
        # API 요청 데이터 준비

        response = requests.post(f"{API_BASE_URL}/history/", json=question_data)

        if response.status_code == 200 or response.status_code == 201:
            st.success("질문이 성공적으로 저장되었습니다.")
            return response.json().get("id")  # 저장된 토론 ID 반환
        else:
            st.error(f"질문 저장 실패: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        st.error(f"API 호출 오류: {str(e)}")
        return None


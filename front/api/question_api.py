import requests
import streamlit as st

from utils.config import API_BASE_URL


def fetch_and_stream_answer(data: dict[str:str], status: st.delta_generator):
    try:
        response = requests.post(
            f"{API_BASE_URL}/question/stream",
            # f"{API_BASE_URL}/question/stream/test",
            # f"{API_BASE_URL}/question/stream/test/notProgramQuestion",
            json=data,
            stream=True,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            st.error(f"API 오류: {response.status_code} - {response.text}")
            return

        from components.question_component import process_sse_stream

        process_sse_stream(response, status)

    except requests.RequestException as e:
        st.error(f"API 요청 오류: {str(e)}")

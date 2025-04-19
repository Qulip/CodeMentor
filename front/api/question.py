import requests
import streamlit as st

from components.question import process_streaming_response
from utils.config import API_BASE_URL


def stream_question(data: dict[str:str], status: st.delta_generator):
    try:
        response = requests.post(
            f"{API_BASE_URL}/workflow/question/stream",
            json=data,
            stream=True,
            headers={"Content-Type": "application/json"},
        )

        if response.status_code != 200:
            st.error(f"API 오류: {response.status_code} - {response.text}")
            return

        process_streaming_response(response, status)

    except requests.RequestException as e:
        st.error(f"API 요청 오류: {str(e)}")

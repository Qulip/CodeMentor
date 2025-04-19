import json

def json_to_str(json_data) -> str:
    """
    Json(dict) string 변환(한글 깨짐 방지)
    :param json_data: json or Dict 객체
    :return: str: string 직렬화
    """
    return json.dumps(json_data, ensure_ascii=False)

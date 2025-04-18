from core.state import AnswerState


def get_additional_info_fstring(answer_state: AnswerState) -> str:
    classification = answer_state.get("classification")
    additional_info = []

    if classification.get("framework"):
        additional_info.append(f"- 프레임워크: '{classification['framework']}'")
    if classification.get("errorType"):
        additional_info.append(f"- 에러 타입: '{classification['errorType']}'")
    if classification.get("tags"):
        additional_info.append(f"- 태그: '{classification['tags']}'")

    rst = f""
    if additional_info:
        rst += "\n" + "\n".join(additional_info)

    return rst

def get_problem_fstring(answer_state: AnswerState) -> str:
    fstring_list = []

    if answer_state.get("problems"):
        fstring_list.append(f"- 예상 오류 원인: ")
        for problem in answer_state.get("problems"):
            fstring_list.append(f"  > '{problem}'")

    rst = f""
    if fstring_list:
        rst += "\n" + "\n".join(fstring_list)

    return rst

def get_solution_fstring(answer_state: AnswerState) -> str:
    fstring_list = []

    if answer_state.get("solutions"):
        fstring_list.append(f"- 제공한 해결방법: ")
        for solution in answer_state.get("solutions"):
            fstring_list.append(f"  > '{solution}'")

    rst = f""
    if fstring_list:
        rst += "\n" + "\n".join(fstring_list)
    return rst

def get_study_tips_fstring(answer_state: AnswerState) -> str:
    fstring_list = []

    if answer_state.get("study_tips"):
        fstring_list.append(f"- 추가로 학습하면 좋을 내용: ")
        for tip in answer_state.get("study_tips"):
            fstring_list.append(f"  > 내용: '{tip["infomation"]}'")
            fstring_list.append(f"    이유: '{tip["reason"]}'")

    rst = f""
    if fstring_list:
        rst += "\n" + "\n".join(fstring_list)
    return rst

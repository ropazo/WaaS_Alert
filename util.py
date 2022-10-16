import json


def indent(j: dict) -> str:
    return json.dumps(j, indent=4, ensure_ascii=False)

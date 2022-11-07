import json


def sfix(s: str, l: int) -> str:
    aux = f'{s:.<{l}}'[0:l]
    return aux


def indent_text(text: str, indent: str) -> str:
    result = []
    for line in text.splitlines():
        result.append(f'{indent}{line}')
    return '\n'.join(result)


def indent_dict(json_dict: dict, cut_border=False) -> str:
    text = json.dumps(json_dict, indent='\t', ensure_ascii=False)
    if cut_border:
        text = text.splitlines()
        result = []
        for i in range(len(text) - 2):
            result.append(text[i + 1])
        text = "\n".join(result)
    if text[0] != '\t':
        text = indent_text(text, '\t')
    return text


def indent_str(json_str: str, cut_border=False) -> str:
    try:
        json_dict = json.loads(json_str)
        text = indent_dict(json_dict=json_dict, cut_border=cut_border)
    except (TypeError, json.decoder.JSONDecodeError):
        text = f'\t{json_str}'
    return text
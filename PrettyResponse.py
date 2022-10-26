"""
    FormatResponse

    Genera un registro de log usando MyLogger.
    En el log deja el detalle de una response del módulo requests.
    Incluye dados del request y response.
    También incluye texto de error.
    Retorna una excepción si hay algún error al transformar el cuerpo en json.
    Usa my_logger.info y my_logger.debug
"""
import json
from MyLogger import get_my_logger
from requests.models import Response
from datetime import timedelta


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
        for i in range(len(text)-2):
            result.append(text[i+1])
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


def log_pretty_response(response: Response, delta_t: timedelta = None):
    assert(response is not None)
    my_logger = get_my_logger()

    delta_str = f' (delta_t = {delta_t})' if delta_t is not None else ""

    formatted_response = (
        f'{response.status_code} Petición {response.request.method} a {response.url} {delta_str}\n'
        f'--->\n'
        f'{indent_dict(json_dict=dict(response.request.headers), cut_border=True)}\n'
        f'\t---\n'
        f'{indent_str(json_str=response.request.body, cut_border=False)}\n'
        f'<---\n'
        f'{indent_dict(json_dict=dict(response.headers), cut_border=True)}\n'
        f'\t---\n'
        f'{indent_str(json_str=response.text, cut_border=False)}\n'
        f'\nORIGINAL RESPONSE BODY:\n{response.text}\n\n'
    )
    my_logger.debug(formatted_response)

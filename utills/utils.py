from urllib.parse import urlparse, parse_qs
from base64 import b64encode, b64decode


def encode_password(text: str) -> str:
    """Кодирует строку в base64"""
    return b64encode(text.encode('utf-8')).decode('utf-8')


def decode_password(encoded_text: str) -> str:
    """Декодирует base64 обратно в строку"""
    return b64decode(encoded_text).decode('utf-8')


def parse_query(route: str) -> dict:
    """
    Разбирает строку маршрута Flet (например: "/info?id=5&msg=hello")
    и возвращает словарь параметров.
    """
    parsed = urlparse(route)  # /info?id=5&msg=hello
    params = parse_qs(parsed.query)  # {'id': ['5'], 'msg': ['hello']}
    # превращаем значения из списков в строки
    return {k: v[0] for k, v in params.items()}

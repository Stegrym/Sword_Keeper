from urllib.parse import urlparse, parse_qs




def parse_query(route: str) -> dict:
    """
    Разбирает строку маршрута Flet (например: "/info?id=5&msg=hello")
    и возвращает словарь параметров.
    """
    parsed = urlparse(route)  # /info?id=5&msg=hello
    params = parse_qs(parsed.query)  # {'id': ['5'], 'msg': ['hello']}
    # превращаем значения из списков в строки
    return {k: v[0] for k, v in params.items()}

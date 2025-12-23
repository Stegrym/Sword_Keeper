import json
from pathlib import Path
from dataclasses import dataclass, asdict


@dataclass
class Entry:
    service: str
    login: str
    email: str
    password: str


# IDEA: добавить GUI через tkinter
# IDEA: добавить поиск по service/email
# IDEA: добавить SQLite хранение данных


service_data = "service"
login_data = "login"
email_data = "email@mail.com"
password_data = "password1"

STORAGE_FILE = "storage.json"
DEFAULT_ENCODING = "utf-8"


def add_entry() -> Entry:
    """
    Функция для ввода данных и вывода сущности Entry
    """
    service = input("Название сервиса - ")
    login = input("Логин если есть - ")
    email = input("Email адрес - ")
    password = input("Пароль - ")
    return Entry(service, login, email, password)


def check_storage(file_name=STORAGE_FILE):
    """
    :param file_name:
    :return:
    """
    file = Path("storage.json")
    if not file.exists():
        file.write_text("[]", encoding=DEFAULT_ENCODING)


def read_data(file=STORAGE_FILE):
    """
    Open for read JSON file, return json data
    :param file: json file
    :return: data:list
    """
    check_storage(file)
    with open(file, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
    return data


def write_data():
    # TODO: добавить проверку email через регулярное выражение
    # TODO: расширить поиск по сервису, а не только по email
    # NOTE: Добавить Док
    entry = add_entry()
    data = read_data(STORAGE_FILE)
    new_entry = asdict(entry)
    data.append(new_entry)

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def search_entry(service: str) -> dict:
    """
    Ищет данные пользователя по сервису
    :param service:
    :return: словарь даннных
    """
    service_info = f"Данные сервиса - {service}: "
    storage = read_data()
    for data in storage:
        if data["service"] == service:
            info = data
            break
        info = "Не найденны"
    service_info += info
    return service_info


# write_data()

print(read_data())
print(search_entry("выф "))

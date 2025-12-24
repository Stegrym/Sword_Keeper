import json
from pathlib import Path
from dataclasses import dataclass, asdict

STORAGE_FILE = "storage.json"
DEFAULT_ENCODING = "utf-8"


@dataclass
class Entry:
    """
    Класс для хранения входящих данных
    """
    service: str
    login: str
    email: str
    password: str


def add_entry() -> Entry:
    """
    Функция для ввода данных и вывода объекта Entry
    :return class Entry
    """
    service = input("Название сервиса - ")
    login = input("Логин если есть - ")
    email = input("Email адрес - ")
    password = input("Пароль - ")
    return Entry(service, login, email, password)


def read_data() -> list:
    """
    Отдаёт список с данными из json STORAGE_FILE
    :return: список со словарями данных
    """

    storage_path = Path(STORAGE_FILE)
    if not storage_path.exists():
        storage_path.write_text("[]", encoding=DEFAULT_ENCODING)

    with open(STORAGE_FILE, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
    return data


def write_data() -> bool:
    """
    Записывает в хранилище данные, выдаёт статус операции
    :return: Статус операции по записи данных
    """
    # TODO: добавить проверку email через регулярное выражение
    # TODO: расширить поиск по сервису, а не только по email
    write_status = False
    entry = add_entry()
    data = read_data()
    new_entry = asdict(entry)
    data.append(new_entry)

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
        write_status = True
    return write_status


def search_entry(entry: str) -> str:
    """
    Ищет данные пользователя по вводимому имени сервиса.
    :param entry:
    :return: Данные полученные в результате поиска
    """
    service_info = f"Данные сервиса - {entry}: "
    storage = read_data()
    info = ""

    for data in storage:
        if data["service"] == entry:
            for name, inf in data.items():
                info += f"\n{name}:{inf}"
            break

    if not info:
        info = "Не найденны"

    service_info += info
    return service_info


def delete_entry(entry: str) -> bool:
    """
    Ищет и удаляет данные из хранилища
    :param entry: Данные для удаления
    :return: статус операции по удалению
    """
    data = read_data()
    new_data = []
    delete_status = False
    for item in data:
        if item["service"] != entry:
            new_data.append(item)
        else:
            delete_status = True
    with  open(STORAGE_FILE, "w", encoding='utf-8') as file:
        json.dump(new_data, file, indent=4, ensure_ascii=False)

    return delete_status


def update_data(service: str):
    """
    Ищет и удаляет данные service и записывает новые
    :param service:
    :return:
    """
    # TODO Доработать систему обновления данных...
    delete_status = delete_entry(service)
    if delete_status:
        write_data()

import json
from pathlib import Path

# IDEA: добавить GUI через tkinter
# IDEA: добавить поиск по service/email
# IDEA: добавить SQLite хранение данных



email_input_data = "QWERTY@gmai.com"  # input("Введите Email адрес - ")
password_input_data = "QWErty12345"  # input("Введите пароль - ")
STORAGE_FILE = "storage.json"
DEFAULT_ENCODING = "utf-8"


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


def write_data(service, email:str, password:str):
    # TODO: добавить проверку email через регулярное выражение
    # TODO: расширить поиск по сервису, а не только по email
    # NOTE: Добавить Док

    data = read_data(STORAGE_FILE)
    new_entry = {"email": email, "password": password}
    data.append(new_entry)

    with open(STORAGE_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


write_data("test", email_input_data, password_input_data)

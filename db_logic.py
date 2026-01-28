from models import Passwords, db
from app_loging import logger


def create_tables():
    """Создание таблицы"""

    with db:
        db.create_tables([Passwords])
        logger.info("База данных: Таблица создана")


# CREATE
def add_password(service: str, email: str, password: str, notes: str = ""):
    """Добавить запись в базу данных"""
    service_entry = service.strip().lower()
    email_entry = email.strip().lower()
    try:
        Passwords.create(
            service=service_entry,
            email=email_entry,
            password=password,
            notes=notes
        )
        logger.info(f"База данных: Сервис {service_entry} сохранён")
    except Exception as e:
        logger.info(f"База данных: Сервис {service_entry} не сохранён\nОшибка: {e}")


# READ
def get_all():
    """Вернуть все записи"""
    try:
        result = list(Passwords.select())
        logger.info(f"База данных: Данные из базы получены")
        return result
    except Exception as e:
        logger.info(f"База данных: Данные из базы НЕ получены\nОшибка: {e}")


# DELETE
def delete_password(record_id):
    """Удалить запись по id"""
    try:
        query = Passwords.delete().where(Passwords.id == record_id)
        query.execute()
        logger.info(f"База данных: Сервис c id:{record_id} удалён")
    except Exception as e:
        logger.info(f"База данных: Сервис с id:{record_id} не удалён\nОшибка: {e}")


def get_data(record_id):
    """Выдаёт данные из базы по id"""
    try:
        result = Passwords.get(Passwords.id == record_id)
        logger.info(f"База данных: Данные с id{record_id} получены")
        return result
    except Exception as e:
        logger.info(f"База данных: Сервис с id:{record_id} не доступен\nОшибка: {e}")
        return None

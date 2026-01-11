from app_loging.loging_setup import logger
from models import Passwords, db



def create_tables():
    """Создание таблицы"""

    with db:
        db.create_tables([Passwords])
        logger.info("Таблица создана!")


# CREATE
def add_password(service: str, email: str, password: str, notes: str = ""):
    return Passwords.create(
        service=service.strip().lower(),
        email=email.strip().lower(),
        password=password,
        notes=notes
    )


# READ
def get_all():
    """Вернуть все записи"""
    return list(Passwords.select())


# DELETE
def delete_password(record_id):
    """Удалить запись по id"""
    query = Passwords.delete().where(Passwords.id == record_id)
    return query.execute()


def get_data(record_id):
    try:
        return Passwords.get(Passwords.id == record_id)
    except Passwords.DoesNotExist:
        return None

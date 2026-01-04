from peewee import *

db = SqliteDatabase("user_database.db")


class Passwords(Model):
    id = AutoField(primary_key=True)
    service = CharField()
    email = CharField()
    password = CharField()
    notes = CharField(max_length=150)

    class Meta:
        database = db
        table_name = "passwords"

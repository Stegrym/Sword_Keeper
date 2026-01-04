from db_logic import create_tables
from gui_logic import run_app

def main():
    # создаём таблицы (если их нет)
    create_tables()
    # запускаем GUI
    run_app()

if __name__ == "__main__":
    main()

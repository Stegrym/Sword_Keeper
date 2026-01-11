import flet as ft
from db_logic import delete_password, get_all

def delete_service(record_id: int, page: ft.Page):
    print("i am work")
    # ORM-запрос: достаём объект по id
    records = get_all()
    record = next((r for r in records if r.id == record_id), None)

    def confirm_delete(e):
        delete_password(record.id)   # удаляем из СУБД
        page.go("/home")

    def cancel(e):
        page.go(f"/info?id={record_id}")  # возвращаемся обратно

    return ft.View(
        route="/delete_service",
        controls=[
            ft.Text(f"Вы уверены, что хотите удалить сервис {record.service}?"),
            ft.Row([
                ft.ElevatedButton("Удалить", on_click=confirm_delete),
                ft.ElevatedButton("Отмена", on_click=cancel),
            ])
        ]
    )

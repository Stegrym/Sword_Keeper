import flet as ft
from db_logic import delete_password, get_all


def delete_service(record_id: int, page: ft.Page):
    """Страница, для удаления сервиса по id"""

    # Ищем нужную запись
    records = get_all()
    record = next((r for r in records if r.id == record_id), None)

    # if record: ?????????
    def accept(e):
        """Кнопка подтверждения удаления.
        Удаляет данные и возвращает на /home"""

        delete_password(record.id)
        page.go("/home")

    def cancel(e):
        """Кнопка отмены"""

        page.go(f"/info?id={record_id}")  # Галя у нас отмена!

    # Создание страницы
    confirm_message = ft.Text(f"Вы уверены, что хотите удалить сервис {record.service}?")
    confirm_buttons = ft.Row([
        ft.ElevatedButton("Удалить", on_click=accept),
        ft.ElevatedButton("Отмена", on_click=cancel),
    ])
    page_content = [confirm_message, confirm_buttons,]

    return ft.View(
        route="/delete_service",
        controls=page_content
    )

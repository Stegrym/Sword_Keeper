import flet as ft
from utills import decode_password
from clipboard import copy
from db_logic import get_all


def info_page(id: int, page: ft.Page):
    """Страница с подробной информацией о сервисе"""

    show = ft.Ref[ft.Text]()
    records = get_all()
    record = next((r for r in records if r.id == id), None)

    if not record:
        return ft.View(route="/info", controls=[ft.Text("Запись не найдена")])
    else:
        password = decode_password(record.password)

    def toggle(e):
        """Меняет текст пароля на символы"""

        if show.current.value == "*****":
            show.current.value = password
        else:
            show.current.value = "*****"
        show.current.update()

    # Создание страницы
    # Вывод информации по сервису
    details = ft.Column([
        ft.Row([
            ft.Container(ft.Text("Service:"), width=150),  # фиксируем ширину
            ft.Text(record.service)
        ]),
        ft.Row([
            ft.Container(ft.Text("Email:"), width=150),
            ft.Container(ft.Text(record.email), width=150),
            ft.IconButton(
                icon=ft.Icons.COPY,
                tooltip="Copy email",
                on_click=lambda e: copy(record.email))
        ]),
        ft.Row([
            ft.Container(ft.Text("Password:"), width=150),
            ft.Container(ft.Text("*****", ref=show), width=150),
            ft.IconButton(
                icon=ft.Icons.COPY,
                tooltip="Copy email",
                on_click=lambda e: copy(password)),
            # ft.IconButton(icon=ft.Icons.REMOVE_RED_EYE, on_click=toggle)
        ]),
        ft.Row([
            ft.Container(ft.Text("Notes:"), width=150),
            ft.Container(ft.Text(record.notes), width=150)
        ]),
    ])

    # Кнопки
    buttons_menu = ft.Row([
        ft.ElevatedButton("Back", on_click=lambda e: page.go("/home")),
        ft.ElevatedButton("Show Password", on_click=toggle),
        ft.ElevatedButton("Delete", on_click=lambda e: page.go(f"/delete_service?id={record.id}")),
    ])

    page_content = [
        details,
        buttons_menu
    ]
    return ft.View(
        route="/info",
        controls=page_content
    )

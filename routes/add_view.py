import flet as ft
from utills import encode_password
from db_logic import add_password


def add_view(page: ft.Page):
    """Страница создания новой записи в БД"""

    service = ft.TextField(label="Service")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Password")
    notes = ft.TextField(label="Notes")

    def save(e):
        """Кнопка сохранения"""
        password_entry = encode_password(password.value)
        add_password(service.value, email.value, password_entry, notes.value)
        page.go("/home")

    def back(e):
        """Кнопка вернутся назад"""
        page.go("/home")

    # Создание страницы
    confirm_buttons = ft.Row([
        ft.ElevatedButton("Сохранить", on_click=save),
        ft.ElevatedButton("Назад", on_click=back)
    ])

    page_content = [ft.Column([
        service,
        email,
        password,
        notes,
        confirm_buttons,
    ])
    ]

    return ft.View(
        route="/add",
        controls=page_content
    )

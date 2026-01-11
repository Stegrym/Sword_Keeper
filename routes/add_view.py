import flet as ft
from db_logic import add_password

def add_view(page: ft.Page):
    service = ft.TextField(label="Service")
    email = ft.TextField(label="Email")
    password = ft.TextField(label="Password")
    notes = ft.TextField(label="Notes")

    def save(e):
        add_password(service.value, email.value, password.value, notes.value)
        page.go("/home")

    def back(e):
        page.go("/home")

    return ft.View(
        route="/add",
        controls=[
            ft.Column([
                service,
                email,
                password,
                notes,
                ft.Row([
                    ft.ElevatedButton("Сохранить", on_click=save),
                    ft.ElevatedButton("Назад", on_click=back)
                ])
            ])
        ]
    )

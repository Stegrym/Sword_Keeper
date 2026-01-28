import flet as ft
from app_loging import log_info
from utills import decode_password
from clipboard import copy
from db_logic import get_all


def info_page(id: int, page: ft.Page):
    show = ft.Ref[ft.Text]()
    records = get_all()
    record = next((r for r in records if r.id == id), None)

    if not record:
        return ft.View(route="/info", controls=[ft.Text("Запись не найдена")])
    else:
        log_info(f"b64 - {record.password}")
        password = decode_password(record.password)
        log_info(f"пароль - {password}")

    def toggle(e):
        # меняем текст на ***** или реальный пароль
        if show.current.value == "*****":
            show.current.value = password
        else:
            show.current.value = "*****"
        show.current.update()

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
    bootm_menu = ft.Row([
        ft.ElevatedButton("Back", on_click=lambda e: page.go("/home")),
        ft.ElevatedButton("Show Password", on_click=toggle),
        ft.ElevatedButton("Delete", on_click=lambda e: page.go(f"/delete_service?id={record.id}")),
    ])

    return ft.View(
        route="/info",
        controls=[
            details,
            bootm_menu
        ]
    )

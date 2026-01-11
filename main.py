import flet as ft
from utills import parse_query
from app_loging import loger_info
from db_logic import create_tables
from routes import home_view, add_view, info_page, delete_service


def main(page: ft.Page):
    page.title = "Password Manager"
    page.window_prevent_close = False
    page.window_width = 900
    page.window_height = 600

    def route_change(e):
        page.views.clear()

        if page.route == "/home":
          loger_info("PAGE - /home")
          page.views.append(home_view(page))

        elif page.route == "/add":
            loger_info("PAGE - /add")
            page.views.append(add_view(page))

        elif page.route.startswith("/info"):
            loger_info("PAGE - /info")
            params = parse_query(page.route)
            record_id = int(params["id"])
            page.views.append(info_page(record_id, page))

        elif page.route.startswith("/delete_service"):
            loger_info("PAGE - /delete_service")
            params = parse_query(page.route)
            record_id = int(params["id"])
            page.views.append(delete_service(record_id, page))

        page.update()

    def view_pop(e):
        page.views.pop()
        page.update()

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    create_tables()
    page.go("/home")


ft.app(target=main)

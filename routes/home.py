import flet as ft
from typing import List
# from clipboard import copy
from db_logic import get_all


def build_rows(page, records) -> List[ft.DataRow]:
    """Создаёт список из объектов DataRow для заполнения строк таблицы"""

    rows = []
    for row in records:
        take_id = row.id
        rows.append(ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(row.service)),
                ft.DataCell(ft.Text(row.email)),
                ft.DataCell(ft.Text(row.notes)),
                # кнопка перехода на страницу редактирования
                ft.DataCell(ft.IconButton(icon=ft.Icons.ARROW_FORWARD,
                                          on_click=lambda e, r_id=take_id: page.go(f"/info?id={r_id}"))),
            ]
        ))
    return rows


def home_view(page: ft.Page) -> ft.View():
    """Создаёт таблицу из базы данных,
    имеет возможность сортировки,
    возвращает View страницы c rout:/home"""

    sort_status = False
    records = get_all()

    def sort_table(e, page, table, records):
        """Сортирует records по нужному столбцу с переменной направления,
        пересоздаёт строки таблицы"""

        nonlocal sort_status
        sort_status = not sort_status

        # Выбор столбца для сортировки
        col = e.column_index
        if col == 0:
            key = "service"
        else:
            key = "email"

        # Обновление таблицы
        sorted_records = sorted(records, key=lambda r: getattr(r, key), reverse=not sort_status)
        table.rows = build_rows(page, sorted_records)
        page.update()

    table = ft.DataTable(
        sort_column_index=0,
        sort_ascending=sort_status,
        columns=[
            ft.DataColumn(ft.Text("Service"), on_sort=lambda e: sort_table(e, page, table, records)),
            ft.DataColumn(ft.Text("Email"), on_sort=lambda e: sort_table(e, page, table, records)),
            ft.DataColumn(ft.Text("Notes")),
            ft.DataColumn(ft.Text("Action")),
        ],
        rows=build_rows(page, records),
    )

    # __MENU__
    columns = [table, ft.Button("Добавить запись", on_click=lambda e: page.go("/add"))]

    return ft.View(
        route="/home",
        controls=[ft.Column(columns)])

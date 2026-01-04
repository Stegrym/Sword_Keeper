import tkinter as tk
from db_logic import get_all, get_data, add_password, delete_password

def run_app():
    root = tk.Tk()
    root.title("Менеджер паролей")

    # --- список записей ---
    listbox = tk.Listbox(root, width=50)
    listbox.pack()

    details_var = tk.StringVar()
    details_label = tk.Label(root, textvariable=details_var, justify="left")
    details_label.pack()

    # --- функции ---
    def refresh_list():
        listbox.delete(0, "end")
        for rec in get_all():
            listbox.insert("end", f"{rec.id}: {rec.service} ({rec.email})")

    def show_details():
        selection = listbox.curselection()
        if not selection:
            return
        selected = listbox.get(selection[0])
        record_id = int(selected.split(":")[0])
        record = get_data(record_id)
        if record:
            details_var.set(
                f"Сервис: {record.service}\n"
                f"Email: {record.email}\n"
                f"Пароль: {record.password}\n"
                f"Заметки: {record.notes}"
            )

    def add_record_window():
        win = tk.Toplevel(root)
        win.title("Добавить запись")

        service_var = tk.StringVar()
        email_var = tk.StringVar()
        password_var = tk.StringVar()
        notes_var = tk.StringVar()

        tk.Label(win, text="Сервис").pack()
        tk.Entry(win, textvariable=service_var).pack()
        tk.Label(win, text="Email").pack()
        tk.Entry(win, textvariable=email_var).pack()
        tk.Label(win, text="Пароль").pack()
        tk.Entry(win, textvariable=password_var).pack()
        tk.Label(win, text="Заметки").pack()
        tk.Entry(win, textvariable=notes_var).pack()

        def save():
            add_password(service_var.get(), email_var.get(),
                         password_var.get(), notes_var.get())
            win.destroy()
            refresh_list()

        tk.Button(win, text="Сохранить", command=save).pack()

    def delete_selected():
        selection = listbox.curselection()
        if not selection:
            return
        selected = listbox.get(selection[0])
        record_id = int(selected.split(":")[0])

        confirm = tk.Toplevel(root)
        tk.Label(confirm, text="Удалить запись?").pack()

        def do_delete():
            delete_password(record_id)
            confirm.destroy()
            refresh_list()

        tk.Button(confirm, text="Да", command=do_delete).pack()
        tk.Button(confirm, text="Нет", command=confirm.destroy).pack()

    # --- кнопки ---
    btn_refresh = tk.Button(root, text="Обновить список", command=refresh_list)
    btn_refresh.pack()

    btn_show = tk.Button(root, text="Показать детали", command=show_details)
    btn_show.pack()

    btn_add = tk.Button(root, text="Добавить запись", command=add_record_window)
    btn_add.pack()

    btn_delete = tk.Button(root, text="Удалить выбранную", command=delete_selected)
    btn_delete.pack()

    # --- старт ---
    refresh_list()
    root.mainloop()


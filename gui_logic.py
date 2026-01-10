import tkinter as tk
from tkinter import ttk, messagebox
from db_logic import get_all, add_password, delete_password, get_data


def run_gui():
    root = tk.Tk()
    root.title("Password Manager")

    # Определяем колонки (без id)
    columns = ("Service", "Email", "Password", "Notes")
    tree = ttk.Treeview(root, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_by(tree, c, False))
        tree.column(col, width=150)

    tree.pack(fill=tk.BOTH, expand=True)

    # --- функции ---
    def show_data():
        for row in tree.get_children():
            tree.delete(row)
        for rec in get_all():
            tree.insert("", tk.END, values=(rec.service, rec.email, len(rec.password) * "*", rec.notes),
                        iid=str(rec.id))

    def sort_by(tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children("")]
        data.sort(reverse=descending)
        for index, (val, child) in enumerate(data):
            tree.move(child, "", index)
        tree.heading(col, command=lambda: sort_by(tree, col, not descending))

    def add_record():
        # простая форма через toplevel
        win = tk.Toplevel(root)
        win.title("Add record")

        # окно всегда поверх главного
        win.transient(root)
        win.grab_set()
        win.focus_set()

        tk.Label(win, text="Service").grid(row=0, column=0)
        tk.Label(win, text="Email").grid(row=1, column=0)
        tk.Label(win, text="Password").grid(row=2, column=0)
        tk.Label(win, text="Notes").grid(row=3, column=0)

        service_entry = tk.Entry(win)
        email_entry = tk.Entry(win)
        password_entry = tk.Entry(win)
        notes_entry = tk.Entry(win)

        service_entry.grid(row=0, column=1)
        email_entry.grid(row=1, column=1)
        password_entry.grid(row=2, column=1)
        notes_entry.grid(row=3, column=1)

        def save():
            add_password(
                service_entry.get(),
                email_entry.get(),
                password_entry.get(),
                notes_entry.get()
            )
            show_data()
            win.destroy()

        tk.Button(win, text="Save", command=save).grid(row=4, column=0, columnspan=2)

        win.wait_window()

    def delete_record():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Выберите запись для удаления")
            return
        record_id = int(selected[0])  # iid хранит id
        delete_password(record_id)
        show_data()

    def toggle_password():
        selected = tree.selection()

        record_id = int(selected[0])
        rec = get_data(record_id)
        values = tree.item(selected[0], "values")
        current_pwd = values[2]

        if set(current_pwd) == {"*"}:  # если звёздочки
            tree.set(selected[0], "Password", rec.password)
        else:
            tree.set(selected[0], "Password", len(rec.password) * "*")

    def copy_email():
        """Сохраняет поле email от выделенной строке"""

        selected = tree.selection()
        values = tree.item(selected[0], "values")
        email = values[1]  # колонка Email
        root.clipboard_clear()
        root.clipboard_append(email)

    def copy_password():
        """Сохраняет поле password от выделенной строке"""

        selected = tree.selection()
        values = tree.item(selected[0], "values")
        password = values[2]  # колонка Password
        root.clipboard_clear()
        root.clipboard_append(password)

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Add Record", command=add_record)
    menu.add_command(label="Copy Email", command=copy_email)
    menu.add_command(label="Copy Password", command=copy_password)
    menu.add_command(label="Delete", command=delete_record)
    menu.add_command(label="Show/Hide Password", command=toggle_password)

    def show_menu(event):
        """Создаёт меню при нажатии ПКМ"""

        selected = tree.identify_row(event.y)
        if selected:
            tree.selection_set(selected)  # включаем все пункты
            menu.entryconfig("Copy Email", state="normal")
            menu.entryconfig("Copy Password", state="normal")
            menu.entryconfig("Delete", state="normal")
            menu.entryconfig("Show/Hide Password", state="normal")
        else:
            menu.entryconfig("Copy Email", state="disabled")
            menu.entryconfig("Copy Password", state="disabled")
            menu.entryconfig("Delete", state="disabled")
            menu.entryconfig("Add Record", state="normal")
            menu.entryconfig("Show/Hide Password", state="disabled")

        menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_menu)  # ПКМ

    def hide_menu(event):
        """Скрывает меню, при нажатии ЛКМ или СКМ в любое место"""
        menu.unpost()

    root.bind("<Button-1>", hide_menu)  # ЛКМ по окну
    root.bind("<Button-2>", hide_menu)  # СКМ

    # --- кнопки в одну строку ---
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Add", command=add_record).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Copy Email", command=copy_email).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Copy Password", command=copy_password).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_record).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Show/Hide Password", command=toggle_password).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Refresh", command=show_data).pack(side=tk.LEFT, padx=5)

    show_data()
    root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from db_logic import get_all, add_password, delete_password


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
            tree.insert("", tk.END, values=(rec.service, rec.email, rec.password, rec.notes), iid=str(rec.id))

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

    def delete_record():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Выберите запись для удаления")
            return
        record_id = int(selected[0])  # iid хранит id
        delete_password(record_id)
        show_data()

    def copy_email():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Выберите запись")
            return
        values = tree.item(selected[0], "values")
        email = values[1]  # колонка Email
        root.clipboard_clear()
        root.clipboard_append(email)
        messagebox.showinfo("Copied", f"Email скопирован: {email}")

    def copy_password():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Выберите запись")
            return
        values = tree.item(selected[0], "values")
        password = values[2]  # колонка Password
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Пароль скопирован!")

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Copy Email", command=copy_email)
    menu.add_command(label="Copy Password", command=copy_password)

    def show_menu(event):
        selected = tree.identify_row(event.y)
        if selected:
            tree.selection_set(selected)
            menu.post(event.x_root, event.y_root)

    tree.bind("<Button-3>", show_menu)  # ПКМ

    # --- кнопки в одну строку ---
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=5)

    tk.Button(btn_frame, text="Add", command=add_record).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Copy Email", command=copy_email).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Copy Password", command=copy_password).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_record).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Refresh", command=show_data).pack(side=tk.LEFT, padx=5)

    show_data()
    root.mainloop()

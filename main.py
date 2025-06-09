import tkinter as tk
from tkinter import messagebox, ttk
from contacts import ContactManager

class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quản lý danh bạ")

        self.manager = ContactManager()

        # Form nhập
        self.name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.search_var = tk.StringVar()

        tk.Label(root, text="Name").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.name_var).grid(row=0, column=1)
        tk.Label(root, text="Phone").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.phone_var).grid(row=1, column=1)
        tk.Label(root, text="Email").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.email_var).grid(row=2, column=1)

        # Buttons
        tk.Button(root, text="Add", command=self.add_contact).grid(row=0, column=2)
        tk.Button(root, text="Edit", command=self.edit_contact).grid(row=1, column=2)
        tk.Button(root, text="Delete", command=self.delete_contact).grid(row=2, column=2)
        tk.Button(root, text="Search", command=self.search_contacts).grid(row=3, column=2)

        # Treeview hiển thị danh sách
        self.tree = ttk.Treeview(root, columns=("Name", "Phone", "Email"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Phone", text="Phone")
        self.tree.heading("Email", text="Email")
        self.tree.grid(row=4, column=0, columnspan=3)

        # Ô nhập tìm kiếm
        tk.Entry(root, textvariable=self.search_var).grid(row=3, column=1)

        self.load_contacts_to_tree()

    # Load danh bạ lên Treeview
    def load_contacts_to_tree(self, contacts=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if contacts is None:
            contacts = self.manager.contacts
        for contact in contacts:
            self.tree.insert("", "end", values=(contact["name"], contact["phone"], contact["email"]))

    def add_contact(self):
        try:
            self.manager.add_contact(self.name_var.get(), self.phone_var.get(), self.email_var.get())
            self.load_contacts_to_tree()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def delete_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn liên hệ để xoá")
            return
        index = self.tree.index(selected[0])
        self.manager.delete_contact(index)
        self.load_contacts_to_tree()

    def edit_contact(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chọn mục", "Vui lòng chọn liên hệ để sửa")
            return
        index = self.tree.index(selected[0])
        try:
            self.manager.edit_contact(index, self.name_var.get(), self.phone_var.get(), self.email_var.get())
            self.load_contacts_to_tree()
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def search_contacts(self):
        keyword = self.search_var.get()
        results = self.manager.search_contacts(keyword)
        self.load_contacts_to_tree(results)

if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()

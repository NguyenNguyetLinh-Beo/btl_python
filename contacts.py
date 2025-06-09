import json
import os

class ContactManager:
    def __init__(self, filename="contacts.json"):
        self.filename = filename
        self.contacts = []
        self.load_contacts()

    def load_contacts(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                try:
                    self.contacts = json.load(f)
                except json.JSONDecodeError:
                    self.contacts = []
        else:
            self.contacts = []

    def save_contacts(self):
        with open(self.filename, "w") as f:
            json.dump(self.contacts, f, indent=4)

    def add_contact(self, name, phone, email):
        if not name or not phone or not email:
            raise ValueError("Không được để trống các trường")
        new_contact = {"name": name, "phone": phone, "email": email}
        self.contacts.append(new_contact)
        self.save_contacts()

    def delete_contact(self, index):
        if 0 <= index < len(self.contacts):
            del self.contacts[index]
            self.save_contacts()

    def edit_contact(self, index, name, phone, email):
        if not name or not phone or not email:
            raise ValueError("Không được để trống các trường")
        if 0 <= index < len(self.contacts):
            self.contacts[index] = {"name": name, "phone": phone, "email": email}
            self.save_contacts()

    def search_contacts(self, keyword):
        return [c for c in self.contacts if keyword.lower() in c["name"].lower()]

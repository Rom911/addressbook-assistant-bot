import pickle
from datetime import datetime
from collections import UserDict
from src.utils.validators import validate_phone, validate_email, validate_birthday

# ----------------- Field classes -----------------

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        super().__init__(validate_phone(value))

class Email(Field):
    def __init__(self, value):
        super().__init__(validate_email(value))

class Birthday(Field):
    def __init__(self, value):
        super().__init__(validate_birthday(value))

# ----------------- Record class -----------------

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None

    # Phone methods
    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def delete_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    # Email methods
    def add_email(self, email):
        self.email = Email(email)

    def change_email(self, new_email):
        if self.email:
            self.email = Email(new_email)
            return True
        return False

    def delete_email(self):
        if self.email:
            self.email = None
            return True
        return False

    # Birthday methods
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday):
        if self.birthday:
            self.birthday = Birthday(birthday)
            return True
        return False

    def delete_birthday(self):
        if self.birthday:
            self.birthday = None
            return True
        return False

    def __str__(self):
        phones_str = ", ".join(p.value for p in self.phones)
        email_str = self.email.value if self.email else ""
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else ""
        return f"Name: {self.name.value}, Phones: {phones_str}, Email: {email_str}, Birthday: {birthday_str}"

# ----------------- AddressBook class -----------------

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    # change_phone

    def save_to_file(self, filename="addressbook.pkl"):
        with open(filename, "wb") as f:
            # pickle.dump(self, f)
            pickle.dump(self.data, f)

    # @staticmethod
    # def load_from_file(filename="addressbook.pkl"):
    #     try:
    #         with open(filename, "rb") as f:
    #             return pickle.load(f)
    #     except FileNotFoundError:
    #         return AddressBook()
    @classmethod
    def load_from_file(cls, filename="addressbook.pkl"):
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                book = cls()
                book.data = data
                return book
        except FileNotFoundError:
            return cls()

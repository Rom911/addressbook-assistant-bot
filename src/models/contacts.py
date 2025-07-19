from collections import UserDict
from datetime import datetime
from src.utils.validators import validate_phone, validate_email, validate_birthday

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not validate_phone(value):
            raise ValueError("Invalid phone number format. It should start with + and contain 10-15 digits.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        if not validate_email(value):
            raise ValueError("Invalid email format.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        date_obj = validate_birthday(value)
        super().__init__(date_obj)


class Address(Field):
    def __init__(self, country="", city="", street="", house="", apartment=""):
        self.country = country
        self.city = city
        self.street = street
        self.house = house
        self.apartment = apartment

    def __str__(self):
        return f"{self.country}, {self.city}, {self.street} {self.house}, Apt {self.apartment}"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        self.address = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p.value
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def add_email(self, email):
        self.email = Email(email)

    def add_address(self, country="", city="", street="", house="", apartment=""):
        self.address = Address(country, city, street, house, apartment)

    def __str__(self):
        phones = '; '.join(p.value for p in self.phones)
        return (f"Name: {self.name.value}, Phones: {phones}, "
                f"Email: {self.email}, Birthday: {self.birthday}, "
                f"Address: {self.address}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact '{name}' deleted."
        return f"Contact '{name}' not found."

    def get_upcoming_birthdays(self, start_date, end_date):
        result = []
        for record in self.data.values():
            if record.birthday:
                if start_date <= record.birthday.value <= end_date:
                    result.append(record)
        return result

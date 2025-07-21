import pickle
from datetime import datetime
from collections import UserDict
from src.utils.validators import validate_phone, validate_email, validate_birthday

FILE_PATH = "addressbook.pkl"

# ----------------- Field classes -----------------

class Field:
    """Base class for all fields."""
    def __init__(self, value):
        self.value = value


class Name(Field):
    """Contact name field."""
    pass


class Phone(Field):
    """Phone field with validation."""
    def __init__(self, value):
        super().__init__(validate_phone(value))


class Email(Field):
    """Email field with validation."""
    def __init__(self, value):
        super().__init__(validate_email(value))


class Birthday(Field):
    """Birthday field with validation."""
    def __init__(self, value):
        super().__init__(validate_birthday(value))

# ----------------- Record class -----------------

class Record:
    """Record represents a single contact with name, phones, email, birthday and address."""

    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.email = None
        self.birthday = None
        #self.address = None

    # Phone methods
    def add_phone(self, phone):
        """Add a phone to the contact."""
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        """Change existing phone to a new one."""
        for idx, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[idx] = Phone(new_phone)
                return True
        return False

    def delete_phone(self, phone):
        """Delete a phone from the contact."""
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    # Email methods
    def add_email(self, email):
        """Add email to contact."""
        self.email = Email(email)

    def change_email(self, new_email):
        """Change existing email."""
        if self.email:
            self.email = Email(new_email)
            return True
        return False

    def delete_email(self):
        """Delete email from contact."""
        if self.email:
            self.email = None
            return True
        return False

    # Birthday methods
    def add_birthday(self, birthday):
        """Add birthday to contact."""
        self.birthday = Birthday(birthday)

    def change_birthday(self, birthday):
        """Change existing birthday."""
        if self.birthday:
            self.birthday = Birthday(birthday)
            return True
        return False

    def delete_birthday(self):
        """Delete birthday from contact."""
        if self.birthday:
            self.birthday = None
            return True
        return False

    # Address methods
    # def add_address(self, country, city, street, building, apartment):
    #     self.address = Address(country, city, street, building, apartment)
    #def add_address(self, country, city):
    #    self.address = Address(country, city)

    # def change_address(self, country, city, street, building, apartment):
    #     if self.address:
    #         self.address = Address(country, city, street, building, apartment)
    #         return True
    #     return False
    # def change_address(self, country, city):
    #     if self.address:
    #         self.address = Address(country, city)
    #         return True
    #     return False

    # def delete_address(self):
    #     if self.address:
    #         self.address = None
    #         return True
    #     return False

    def __str__(self):
        phones_str = ", ".join(p.value for p in self.phones)
        email_str = self.email.value if self.email else ""
        birthday_str = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else ""

        # Format the address if it exists
        # address_str = ""
        # if self.address:
        #     addr = self.address
        #     # address_str = f"{addr.country}, {addr.city}, {addr.street} {addr.building}/{addr.apartment}"
        #     address_str = f"{addr.country}, {addr.city}"

        # return f"Name: {self.name.value}, Phones: {phones_str}, Email: {email_str}, Birthday: {birthday_str}, Address: {address_str}"
        return f"Name: {self.name.value}, Phones: {phones_str}, Email: {email_str}, Birthday: {birthday_str}"
    

# ----------------- AddressBook class -----------------

class AddressBook(UserDict):
    """AddressBook manages multiple Record objects."""

    def add_record(self, record):
        """Add a new record to the address book."""
        self.data[record.name.value] = record

    def find(self, name):
        """Find record by name."""
        return self.data.get(name)

    def delete(self, name):
        """Delete record by name."""
        if name in self.data:
            del self.data[name]
            return True
        return False

    def save_to_file(self, filename=FILE_PATH):
        """Serialize address book to file."""
        with open(filename, "wb") as f:
            pickle.dump(self.data, f)

    @classmethod
    def load_from_file(cls, filename=FILE_PATH):
        """Load address book from file."""
        try:
            with open(filename, "rb") as f:
                data = pickle.load(f)
                book = cls()
                book.data = data
                return book
        except FileNotFoundError:
            return cls()


# class Address:
#     # def __init__(self, country="", city="", street="", building="", apartment=""):
#     def __init__(self, country="", city=""):
#         self.country = country
#         self.city = city
#         # self.street = street
#         # self.building = building
#         # self.apartment = apartment

#     def __str__(self):
#         # parts = [self.country, self.city, self.street, self.building, self.apartment]
#         parts = [self.country, self.city]
#         return ", ".join([p for p in parts if p])

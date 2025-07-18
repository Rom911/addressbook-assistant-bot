from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re

# ------------------------ Serialization ------------------------

def save_data(book, filename="addressbook.pkl"):
    """Save AddressBook object to file using pickle serialization"""
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    """Load AddressBook object from file using pickle deserialization"""
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Return new AddressBook if file not found

# ------------------------ Input Error Decorator ------------------------

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)
        except IndexError:
            return "Not enough arguments provided."
    return inner

# ------------------------ Data Classes ------------------------

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty.")
        super().__init__(value)


class City(Field):
    def __init__(self, value):
        if not value.strip():
            raise ValueError("City cannot be empty.")
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        pattern = r"^\+380\d{9}$"
        if not re.match(pattern, value):
            raise ValueError("Phone number must be in Ukrainian international format: +380XXXXXXXXX")


class Email(Field):
    def __init__(self, value):
        self.validate(value)
        super().__init__(value)

    @staticmethod
    def validate(value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, value):
            raise ValueError("Invalid email format. Example: something@example.com or user.name@mail.com.ua")


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y")
            super().__init__(value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.city = None
        self.phones = []
        self.email = None
        self.birthday = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return f"Phone number {phone_number} has been deleted."
        return f"Phone number {phone_number} was not found."

    def edit_phone(self, old_number, new_number):
        for phone in self.phones:
            if phone.value == old_number:
                Phone.validate(new_number)
                phone.value = new_number
                return True
        raise ValueError(f"Phone number {old_number} not found.")

    def find_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                return phone.value
        return None
    
    def add_city(self, city_str):
        self.city = City(city_str)

    def add_email(self, email_str):
        self.email = Email(email_str)

    def add_birthday(self, birthday_str):
        self.birthday = Birthday(birthday_str)

    def __str__(self):
        name_str = f"Name: {self.name.value}"
        city_str = f"City: {self.city.value}" if self.city else "City: not set"
        phones_str = "Phones: " + (', '.join(p.value for p in self.phones) if self.phones else "not set")
        email_str = f"Email: {self.email.value}" if self.email else "Email: not set"
        bday_str = f"Birthday: {self.birthday.value}" if self.birthday else "Birthday: not set"
        return f"{name_str}, {city_str}, {phones_str}, {email_str}, {bday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return f"Contact '{name}' has been deleted."
        return f"Contact '{name}' was not found."

    def get_upcoming_birthdays(self, upcoming_days = 7):
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday_this_year = bday.replace(year=today.year)
                delta_days = (bday_this_year - today).days

                if 0 <= delta_days <= upcoming_days:
                    upcoming_birthdays.append(f"{record.name.value}: {record.birthday.value}")

        return upcoming_birthdays

# ------------------------ Command Handlers ------------------------

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *optional = args
    record = book.find(name)
    message = "Contact updated."

    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."

    if phone:
        record.add_phone(phone)

    if optional:
        for item in optional:
            if re.match(r"^\+380\d{9}$", item):  # another phone
                record.add_phone(item)
            elif re.match(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", item):  # email
                record.add_email(item)
            elif re.match(r"^\d{2}\.\d{2}\.\d{4}$", item):  # birthday
                record.add_birthday(item)
            else:  # If not phone, email or birthday → city.
                record.add_city(item)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact updated."
    else:
        raise KeyError


@input_error
def delete_contact(args, book: AddressBook):
    name, *_ = args
    return book.delete(name)


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones = '; '.join(p.value for p in record.phones)
        return f"{name}: {phones}"
    else:
        raise KeyError


@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return '\n'.join(str(record) for record in book.data.values())


@input_error
def add_city(args, book: AddressBook):
    name, city_str, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    record.add_city(city_str)
    return f"City added for {name}."


@input_error
def add_email(args, book: AddressBook):
    name, email_str, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    record.add_email(email_str)
    return f"Email added for {name}."


@input_error
def add_birthday(args, book: AddressBook):
    name, birthday_str, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday_str)
        return "Birthday added."
    else:
        raise KeyError


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record and record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    else:
        return "Birthday not set."


@input_error
def birthdays(args, book: AddressBook):
    if args:
        try:
            upcoming_days = int(args[0])
        except ValueError:
            return "Error: Number of days must be an integer."
    else:
        upcoming_days = 7

    upcoming = book.get_upcoming_birthdays(upcoming_days)
    if upcoming:
        return f"Upcoming birthdays in {upcoming_days} days:\n" + '\n'.join(upcoming)
    else:
        return f"No upcoming birthdays in the next {upcoming_days} days."

# ------------------------ Parser and Main ------------------------

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = load_data()  # Load AddressBook from file at startup
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)  # Save AddressBook to file before exit
            print("Good bye!")
            break
        
        elif command == "help":
            print(
                "\nAvailable commands:\n"
        "  add <Name> <Phone>\n"
        "      Add a new contact or update an existing one.\n"
        "      Example: add John +380991234567\n\n"
        "  change <Name> <OldPhone> <NewPhone>\n"
        "      Replace an old phone number with a new one.\n"
        "      Example: change John +380991234567 +380981234567\n\n"
        "  delete <Name>\n"
        "      Delete a contact by name.\n"
        "      Example: delete John\n\n"
        "  phone <Name>\n"
        "      Show all phone numbers for a contact.\n"
        "      Example: phone John\n\n"
        "  all\n"
        "      Show all contacts in the address book.\n"
        "      Example: all\n\n"
        "  add-city <Name> <City>\n"
        "      Add or update city information for a contact.\n"
        "      Example: add-city John Kyiv\n\n"
        "  add-email <Name> <Email>\n"
        "      Add or update an email address for a contact.\n"
        "      Example: add-email John john@example.com\n\n"
        "  add-birthday <Name> <DD.MM.YYYY>\n"
        "      Add or update birthday for a contact.\n"
        "      Example: add-birthday John 15.06.1990\n\n"
        "  show-birthday <Name>\n"
        "      Show the birthday of a contact.\n"
        "      Example: show-birthday John\n\n"
        "  birthdays [Days]\n"
        "      Show all upcoming birthdays in the next N days (default is 7).\n"
        "      Example: birthdays 14\n\n"
        "  close / exit\n"
        "      Save data and exit the program.\n"
        "      Example: exit\n"
            )

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(args, book))

        elif command == "add-city":
            print(add_city(args, book))

        elif command == "add-email":
            print(add_email(args, book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()

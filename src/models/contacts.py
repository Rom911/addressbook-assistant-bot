from collections import UserDict
from datetime import datetime
from src.utils.validators import validate_phone, validate_email, validate_birthday


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
        if not validate_phone(value):
            raise ValueError("Phone number must be in Ukrainian international format: +380XXXXXXXXX")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        if not validate_email(value):
            raise ValueError("Invalid email format. Example: something@example.com or user.name@mail.com.ua")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        if not validate_birthday(value):
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


# class Address(Field):
#     def __init__(self, country="", city="", street="", house="", apartment=""):
#         self.country = country
#         self.city = city
#         self.street = street
#         self.house = house
#         self.apartment = apartment

#     def __str__(self):
#         return f"{self.country}, {self.city}, {self.street} {self.house}, Apt {self.apartment}"


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.city = None
        self.phones = []
        self.email = None
        self.birthday = None
        # self.address = None

    def add_phone(self, phone_number):
        phone = Phone(phone_number)
        if phone not in self.phones:
            self.phones.append(phone)
        # self.phones.append(Phone(phone))

    def remove_phone(self, phone_number):
        for phone in self.phones:
            if phone.value == phone_number:
                self.phones.remove(phone)
                return f"Phone number {phone_number} has been deleted."
        return f"Phone number {phone_number} was not found."
        # self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            validate_phone(new_phone)
            phone.value = new_phone
            return phone
        return "Invalid phone format."
        # for idx, p in enumerate(self.phones):
        #     if p.value == old_phone:
        #         self.phones[idx] = Phone(new_phone)
        #         return True
        # return False

    def find_phone(self, phone_number):
        for p in self.phones:
            if p.value == phone_number:
                return p.value
        return None
    
    def add_city(self, city_str):
        self.city = City(city_str)

    def add_email(self, email):
        self.email = Email(email)
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)


    # def add_address(self, country="", city="", street="", house="", apartment=""):
    #     self.address = Address(country, city, street, house, apartment)

    def __str__(self):
        name_str = f"Name: {self.name.value}"
        city_str = f"City: {self.city.value}" if self.city else "City: not set"
        phones_str = "Phones: " + (', '.join(p.value for p in self.phones) if self.phones else "not set")
        email_str = f"Email: {self.email.value}" if self.email else "Email: not set"
        bday_str = f"Birthday: {self.birthday.value}" if self.birthday else "Birthday: not set"
        return f"{name_str}, {city_str}, {phones_str}, {email_str}, {bday_str}"
    
        # phones = '; '.join(p.value for p in self.phones)
        # return (f"Name: {self.name.value}, Phones: {phones}, "
        #         f"Email: {self.email}, Birthday: {self.birthday}, "
        #         f"Address: {self.address}")


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
        upcoming = []

        for record in self.data.values():
            if record.birthday:
                bday = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                bday_this_year = bday.replace(year=today.year)

                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                delta = (bday_this_year - today).days

                if 0 <= delta <= upcoming_days:
                    upcoming.append(f"{record.name.value}: {bday_this_year.strftime('%d.%m.%Y')}")

        return upcoming

    # def get_upcoming_birthdays(self, start_date, end_date):
    #     result = []
    #     for record in self.data.values():
    #         if record.birthday:
    #             if start_date <= record.birthday.value <= end_date:
    #                 result.append(record)
    #     return result

# ------------------------ Input Error Decorator ------------------------
def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, IndexError, KeyError) as e:
            return f"Error: {e}"
    return wrapper


# ------------------------ Command Handlers ------------------------
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *optional = args
    record = book.find(name)

    if not record:
        record = Record(name)
        book.add_record(record)
        message = f"Added new contact {name} with phone {phone}."
    else:
        message = f"Added phone {phone} to existing contact {name}."
    
    record.add_phone(phone)

    if optional:
        for item in optional:
            if validate_phone(item):  # another phone
                record.add_phone(item)
            elif validate_email(item):  # email
                record.add_email(item)
            elif validate_birthday(item):  # birthday
                record.add_birthday(item)
            else:  # If not phone, email or birthday → city.
                record.add_city(item)
                
    return message


@input_error
def change(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    edited = record.edit_phone(old_phone, new_phone)
    if edited:
        return f"Phone number for {name} updated from {old_phone} to {new_phone}."
    return f"Phone number {old_phone} not found for contact {name}."


@input_error
def delete_contact(args, book: AddressBook):
    name, *_ = args
    return book.delete(name)


@input_error
def phone(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    return f"{name}'s phones: {'; '.join(p.value for p in record.phones)}"


def show_all(book: AddressBook):
    if not book.data:
        return "No contacts found."
    return "\n".join(str(record) for record in book.data.values())


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
    if not record:
        return f"Contact '{name}' not found."
    record.add_birthday(birthday_str)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book: AddressBook):
    name, *_ = args
    record = book.find(name)
    if not record:
        return f"Contact '{name}' not found."
    if record.birthday:
        return f"{name}'s birthday: {record.birthday.value}"
    return f"{name} has no birthday saved."


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

    if not upcoming:
        return f"No birthdays in the next {upcoming_days} days."
    return f"Upcoming birthdays in {upcoming_days} days:\n" + "\n".join(upcoming)

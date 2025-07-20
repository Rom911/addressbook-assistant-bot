from datetime import datetime, date
import re

def validate_phone(phone):
    pattern = re.compile(r"^\+?\d{10,15}$")
    if not pattern.match(phone):
        raise ValueError("Invalid phone format")
    return phone

def validate_email(email):
    pattern = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
    if not pattern.match(email):
        raise ValueError("Invalid email format")
    return email

def validate_birthday(birthday):
    if isinstance(birthday, date):
        return birthday
    try:
        return datetime.strptime(birthday, "%d.%m.%Y").date()
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

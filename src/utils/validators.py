import re
from datetime import datetime

def validate_phone(phone):
    """
    Validates that the phone number is in international format starting with + and 10-15 digits.
    """
    pattern = r"^\+\d{10,15}$"
    return re.fullmatch(pattern, phone)

def validate_email(email):
    """
    Validates the email format.
    """
    pattern = r"[^@]+@[^@]+\.[^@]+"
    return re.fullmatch(pattern, email)

def validate_birthday(birthday):
    """
    Validates that the birthday is in DD.MM.YYYY format and converts it to datetime object.
    """
    try:
        return datetime.strptime(birthday, "%d.%m.%Y")
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

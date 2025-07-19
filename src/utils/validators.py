import re
from datetime import datetime

def validate_phone(phone):
    """
    Validates that the phone number is in international format starting with + and 10-15 digits.
    """
    pattern = r"^\+380\d{9}$"
    return re.fullmatch(pattern, phone)

def validate_email(email):
    """
    Validates the email format.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.fullmatch(pattern, email)

def validate_birthday(birthday):
    """
    Validates that the birthday is in DD.MM.YYYY format and converts it to datetime object.
    """
    pattern = r"^\d{2}\.\d{2}\.\d{4}$"
    return re.fullmatch(pattern, birthday)
    
    # try:
    #     return datetime.strptime(birthday, "%d.%m.%Y")
    # except ValueError:
    #     raise ValueError("Invalid date format. Use DD.MM.YYYY")

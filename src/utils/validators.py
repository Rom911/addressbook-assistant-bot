from datetime import datetime, date
import re

PHONE_PATTERN = re.compile(r"^\+?\d{10,15}$")
EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")

def validate_phone(phone):
    """
    Validate phone number in international format with optional '+'.
    """
    if not PHONE_PATTERN.match(phone):
        raise ValueError("Invalid phone format")
    return phone

def validate_email(email):
    """
    Validate email address with common pattern.
    """
    if not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email format")
    return email

def validate_birthday(birthday):
    """
    Validate birthday in format DD.MM.YYYY and check not in the future.
    """
    if isinstance(birthday, date):
        if birthday > date.today():
            raise ValueError("Birthday cannot be in the future")
        return birthday
    try:
        bday = datetime.strptime(birthday, "%d.%m.%Y").date()
        if bday > date.today():
            raise ValueError("Birthday cannot be in the future")
        return bday
    except ValueError:
        raise ValueError("Invalid date format. Use DD.MM.YYYY")

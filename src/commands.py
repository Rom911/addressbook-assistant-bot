import sys
from datetime import datetime, timedelta

from colorama import Fore
from rich.console import Console
from rich.table import Table
from rich import box

from src.decorators import input_error
from src.models.contacts import Record, AddressBook
from src.models.notes import Notes, Note
from src.utils.validators import validate_phone, validate_email, validate_birthday

console = Console()


def parse_input(user_input):
    """
    Parse user input into command and arguments.
    """
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd, *args = parts
    return cmd.lower(), args


@input_error
def show_help(args=None, book=None, notes=None):
    """
    Show available commands.
    """
    table = Table(title="Available Commands", title_style="bold cyan", box=box.SIMPLE_HEAVY)
    table.add_column("Command", style="bold green", no_wrap=True)
    table.add_column("Description", style="white")

    commands_list = [
        ("hello", "Greets the user"),
        ("add <name> <phone>", "Add new contact and phone"),
        ("change <name> <old_phone> <new_phone>", "Change existing phone number"),
        ("phone <name>", "Show phone numbers for contact"),
        ("delete-contact <name>", "Delete contact"),
        ("add-email <name> <email>", "Add email"),
        ("change-email <name> <new_email>", "Change email"),
        ("delete-email <name>", "Delete email"),
        ("add-birthday <name> <DD.MM.YYYY>", "Add birthday"),
        ("change-birthday <name> <DD.MM.YYYY>", "Change birthday"),
        ("delete-birthday <name>", "Delete birthday"),
        ("birthdays <delta>", "Show birthdays in next N days"),
        ("add-note <title> <content>", "Add note"),
        ("change-note <title> <new_content>", "Change note"),
        ("delete-note <title>", "Delete note"),
        ("find-note <keyword>", "Find note"),
        ("add-tag <title> <tag>", "Add tag to note"),
        ("find-tag <tag>", "Find notes by tag"),
        ("all", "Show all contacts"),
        ("help", "Show available commands"),
        ("exit/close", "Exit bot"),
    ]

    for cmd, desc in commands_list:
        table.add_row(cmd, desc)

    console.print(table)
    return ""


@input_error
def hello(args=None, book=None, notes=None):
    """
    Greet the user.
    """
    return Fore.GREEN + "How can I help you?"


@input_error
def add(args=None, book=None, notes=None):
    name, phone = args
    phone = validate_phone(phone)
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return Fore.GREEN + f"Contact {name} added/updated."


@input_error
def change(args=None, book=None, notes=None):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.change_phone(old_phone, new_phone)
        return Fore.GREEN + f"{name}'s phone updated."
    return Fore.RED + "Contact not found."


@input_error
def phone(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return Fore.CYAN + f"{name}'s phones: {phones}"
    return Fore.RED + "Contact not found."


@input_error
def delete_contact(args=None, book=None, notes=None):
    name = args[0]
    if book.delete(name):
        return Fore.GREEN + f"Contact {name} deleted."
    return Fore.RED + "Contact not found."


@input_error
def add_email(args=None, book=None, notes=None):
    name, email = args
    email = validate_email(email)
    record = book.find(name)
    if record:
        record.add_email(email)
        return Fore.GREEN + f"{name}'s email added."
    return Fore.RED + "Contact not found."


@input_error
def change_email(args=None, book=None, notes=None):
    name, new_email = args
    new_email = validate_email(new_email)
    record = book.find(name)
    if record:
        record.change_email(new_email)
        return Fore.GREEN + f"{name}'s email updated."
    return Fore.RED + "Contact not found."


@input_error
def delete_email(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record and record.delete_email():
        return Fore.GREEN + f"{name}'s email deleted."
    return Fore.RED + "Contact not found or email not set."


@input_error
def add_birthday(args=None, book=None, notes=None):
    name, birthday = args
    birthday = validate_birthday(birthday)
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return Fore.GREEN + f"{name}'s birthday added."
    return Fore.RED + "Contact not found."


@input_error
def change_birthday(args=None, book=None, notes=None):
    name, birthday = args
    birthday = validate_birthday(birthday)
    record = book.find(name)
    if record:
        record.change_birthday(birthday)
        return Fore.GREEN + f"{name}'s birthday updated."
    return Fore.RED + "Contact not found."


@input_error
def delete_birthday(args=None, book=None, notes=None):
    name = args[0]
    record = book.find(name)
    if record and record.delete_birthday():
        return Fore.GREEN + f"{name}'s birthday deleted."
    return Fore.RED + "Contact not found or birthday not set."


@input_error
def birthdays(args=None, book=None, notes=None):
    delta = int(args[0]) if args else 7
    today = datetime.today().date()
    upcoming = []
    for rec in book.data.values():
        if rec.birthday:
            bday = rec.birthday.value.replace(year=today.year)
            if bday < today:
                bday = bday.replace(year=today.year + 1)
            if 0 <= (bday - today).days <= delta:
                upcoming.append(f"{rec.name.value}: {rec.birthday.value.strftime('%d.%m.%Y')}")
    if upcoming:
        return Fore.CYAN + "\n".join(upcoming)
    return Fore.YELLOW + "No upcoming birthdays."


@input_error
def add_note(args=None, book=None, notes=None):
    title, content = args
    note = Note(title, content)
    notes.add_note(note)
    return Fore.GREEN + f"Note '{title}' added."


@input_error
def change_note(args=None, book=None, notes=None):
    title, new_content = args
    if notes.change_note(title, new_content):
        return Fore.GREEN + f"Note '{title}' updated."
    return Fore.RED + "Note not found."


@input_error
def delete_note(args=None, book=None, notes=None):
    title = args[0]
    if notes.delete_note(title):
        return Fore.GREEN + f"Note '{title}' deleted."
    return Fore.RED + "Note not found."


@input_error
def find_note(args=None, book=None, notes=None):
    keyword = args[0]
    found = notes.find_note(keyword)
    if found:
        return "\n".join(f"{n.title}: {n.content}" for n in found)
    return Fore.YELLOW + "No notes found."


@input_error
def add_tag(args=None, book=None, notes=None):
    title, tag = args
    note = notes.find(title)
    if note:
        note.add_tag(tag)
        return Fore.GREEN + f"Tag '{tag}' added to note '{title}'."
    return Fore.RED + "Note not found."


@input_error
def find_tag(args=None, book=None, notes=None):
    tag = args[0]
    found = notes.find_by_tag(tag)
    if found:
        return "\n".join(f"{n.title}: {n.content}" for n in found)
    return Fore.YELLOW + "No notes found with this tag."


@input_error
def all_contacts(args=None, book=None, notes=None):
    table = Table(title="All Contacts", title_style="bold magenta", box=box.MINIMAL_DOUBLE_HEAD)
    table.add_column("Name", style="bold green")
    table.add_column("Phones", style="cyan")
    table.add_column("Email", style="yellow")
    table.add_column("Birthday", style="blue")

    for name, record in book.data.items():
        phones = ', '.join([p.value for p in record.phones])
        email = record.email.value if record.email else ''
        birthday = record.birthday.value.strftime("%d.%m.%Y") if record.birthday else ''
        table.add_row(name, phones, email, birthday)

    console.print(table)
    return ""


@input_error
def exit_bot(args=None, book=None, notes=None):
    """
    Save data and exit the bot.
    """
    print(Fore.YELLOW + "Saving data and exiting... Goodbye!")
    book.save_to_file()
    # notes.save_to_file()  # implement if needed
    sys.exit()


COMMANDS = {
    "help": show_help,
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "delete-contact": delete_contact,
    "add-email": add_email,
    "change-email": change_email,
    "delete-email": delete_email,
    "add-birthday": add_birthday,
    "change-birthday": change_birthday,
    "delete-birthday": delete_birthday,
    "birthdays": birthdays,
    "add-note": add_note,
    "change-note": change_note,
    "delete-note": delete_note,
    "find-note": find_note,
    "add-tag": add_tag,
    "find-tag": find_tag,
    "all": all_contacts,
    "exit": exit_bot,
    "close": exit_bot,
}

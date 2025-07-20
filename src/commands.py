import sys
from src.decorators import input_error
from src.models.contacts import Record, AddressBook
from src.models.notes import NoteBook, Note
from src.utils.validators import validate_phone, validate_email, validate_birthday
from src.storage.persistence import save_data, load_data
from prettytable import PrettyTable
from colorama import Fore, Style
from datetime import datetime, timedelta
from src.services.serialization import save_book
from rich.console import Console
from rich.table import Table
from rich import box

book = AddressBook()
notes = NoteBook()
console = Console()

def parse_input(user_input):
    parts = user_input.split()
    if not parts:
        return "", []
    cmd, *args = user_input.split()
    return cmd.lower(), *args

@input_error
def show_help(*args):
    # table = PrettyTable()
    # table.field_names = ["Command", "Description"] # Fore.CYAN + 
    # table.add_rows([
    #     ["hello", "Greet user"],
    #     ["add [name] [phone]", "Add new contact"],
    #     ["change [name] [old_phone] [new_phone]", "Change phone"],
    #     ["phone [name]", "Show phones"],
    #     ["delete-contact [name]", "Delete contact"],
    #     ["add-email [name] [email]", "Add email"],
    #     ["change-email [name] [new_email]", "Change email"],
    #     ["delete-email [name]", "Delete email"],
    #     ["add-birthday [name] [DD.MM.YYYY]", "Add birthday"],
    #     ["change-birthday [name] [DD.MM.YYYY]", "Change birthday"],
    #     ["delete-birthday [name]", "Delete birthday"],
    #     ["birthdays [delta]", "Show birthdays in next N days"],
    #     ["add-note [title] [content]", "Add note"],
    #     ["change-note [title] [new_content]", "Change note"],
    #     ["delete-note [title]", "Delete note"],
    #     ["find-note [keyword]", "Find note"],
    #     ["add-tag [title] [tag]", "Add tag to note"],
    #     ["find-tag [tag]", "Find notes by tag"],
    #     ["all", "Show all contacts"],
    #     ["exit/close", "Exit bot"]
    # ])
    
    # return table

    console = Console()
    table = Table(title="Available Commands", title_style="bold cyan", box=box.SIMPLE_HEAVY)

    table.add_column("Command", style="bold green", no_wrap=True)
    table.add_column("Description", style="white")

    table.add_row("hello", "Greets the user")
    table.add_row("add [name] [phone]", "Add new contact or phone")
    table.add_row("change [name] [old_phone] [new_phone]", "Change existing phone number")
    table.add_row("phone [name]", "Show phone numbers for contact")
    table.add_row("delete-contact [name]", "Delete contact")
    table.add_row("add-email [name] [email]", "Add email")
    table.add_row("change-email [name] [new_email]", "Change email")
    table.add_row("delete-email [name]", "Delete email")
    table.add_row("add-birthday [name] [DD.MM.YYYY]", "Add birthday")
    table.add_row("change-birthday [name] [DD.MM.YYYY]", "Change birthday")
    table.add_row("delete-birthday [name]", "Delete birthday")
    table.add_row("birthdays [delta]", "Show birthdays in next N days")
    table.add_row("add-note [title] [content]", "Add note")
    table.add_row("change-note [title] [new_content]", "Change note")
    table.add_row("delete-note [title]", "Delete note")
    table.add_row("find-note [keyword]", "Find note")
    table.add_row("add-tag [title] [tag]", "Add tag to note")
    table.add_row("find-tag [tag]", "Find notes by tag")
    table.add_row("all", "Show all contacts")
    table.add_row("help", "Show available commands")
    table.add_row("exit/close", "Exit bot")

    console.print(table)

@input_error
def hello(*args):
    return Fore.GREEN + "How can I help you?"

@input_error
def add(args, book):
    name, phone = args
    phone = validate_phone(phone)
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_phone(phone)
    return Fore.GREEN + f"Contact {name} added/updated."

@input_error
def change(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record:
        record.change_phone(old_phone, new_phone)
        return Fore.GREEN + f"{name}'s phone updated."
    return Fore.RED + "Contact not found."

@input_error
def phone(args, book):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ', '.join(p.value for p in record.phones)
        return Fore.CYAN + f"{name}'s phones: {phones}"
    return Fore.RED + "Contact not found."

@input_error
def delete_contact(args, book):
    name = args[0]
    if book.delete(name):
        return Fore.GREEN + f"Contact {name} deleted."
    return Fore.RED + "Contact deleted."

@input_error
def add_email(args, book):
    name, email = args
    email = validate_email(email)
    record = book.find(name)
    if record:
        record.add_email(email)
        return Fore.GREEN + f"{name}'s email added."
    return Fore.RED + "Contact not found."

@input_error
def change_email(args, book):
    name, new_email = args
    new_email = validate_email(new_email)
    record = book.find(name)
    if record:
        record.change_email(new_email)
        return Fore.GREEN + f"{name}'s email updated."
    return Fore.RED + "Contact not found."

@input_error
def delete_email(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.delete_email():
        return Fore.GREEN + f"{name}'s email deleted."
    return Fore.RED + "Contact not found or email not set."

@input_error
def add_birthday(args, book):
    name, birthday = args
    birthday = validate_birthday(birthday)
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return Fore.GREEN + f"{name}'s birthday added."
    return Fore.RED + "Contact not found."

@input_error
def change_birthday(args, book):
    name, birthday = args
    birthday = validate_birthday(birthday)
    record = book.find(name)
    if record:
        record.change_birthday(birthday)
        return Fore.GREEN + f"{name}'s birthday updated."
    return Fore.RED + "Contact not found."

@input_error
def delete_birthday(args, book):
    name = args[0]
    record = book.find(name)
    if record and record.delete_birthday():
        return Fore.GREEN + f"{name}'s birthday deleted."
    return Fore.RED + "Contact not found or birthday not set."

@input_error
def birthdays(args, book):
    delta = int(args[0]) if args else 7
    today = datetime.today().date()
    upcoming = []
    for rec in book.values():
        if rec.birthday:
            bday = rec.birthday.value.replace(year=today.year)
            if 0 <= (bday - today).days <= delta:
                upcoming.append(f"{rec.name.value}: {rec.birthday.value}")
    if upcoming:
        return Fore.CYAN + "\n".join(upcoming)
    return Fore.YELLOW + "No upcoming birthdays."

@input_error
def add_note(args, notes):
    title, content = args
    note = Note(title, content)
    notes.add_note(note)
    return Fore.GREEN + f"Note '{title}' added."

@input_error
def change_note(args, notes):
    title, new_content = args
    if notes.change_note(title, new_content):
        return Fore.GREEN + f"Note '{title}' updated."
    return Fore.RED + "Note not found."

@input_error
def delete_note(args, notes):
    title = args[0]
    if notes.delete_note(title):
        return Fore.GREEN + f"Note '{title}' deleted."
    return Fore.RED + "Note not found."

@input_error
def find_note(args, notes):
    keyword = args[0]
    found = notes.find_note(keyword)
    if found:
        return "\n".join(f"{n.title}: {n.content}" for n in found)
    return Fore.YELLOW + "No notes found."

@input_error
def add_tag(args, notes):
    title, tag = args
    note = notes.find(title)
    if note:
        note.add_tag(tag)
        return Fore.GREEN + f"Tag '{tag}' added to note '{title}'."
    return Fore.RED + "Note not found."

@input_error
def find_tag(args, notes):
    tag = args[0]
    found = notes.find_by_tag(tag)
    if found:
        return "\n".join(f"{n.title}: {n.content}" for n in found)
    return Fore.YELLOW + "No notes found with this tag."

@input_error
def all_contacts(args, book):
    # table = PrettyTable()
    # table.field_names = ["Name", "Phones", "Email", "Birthday"]
    # for rec in book.values():
    #     table.add_row([
    #         rec.name.value,
    #         ', '.join(p.value for p in rec.phones),
    #         rec.email.value if rec.email else '',
    #         rec.birthday.value.strftime('%d.%m.%Y') if rec.birthday else ''
    #     ])
    # return table
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

@input_error
def exit_bot(args, book):
    # save_book(book)
    print(Fore.YELLOW + "Saving data and exiting... Goodbye!")
    book.save_to_file()
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
    # добавить, удалить адрес
    "add-note": add_note,
    "change-note": change_note,
    "delete-note": delete_note,
    "find-note": find_note,
    "add-tag": add_tag,
    # удалить тег
    # автозаполнение
    "find-tag": find_tag,
    "all": all_contacts,
    "exit": exit_bot,
    "close": exit_bot,
}


def show_all_contacts(book):
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

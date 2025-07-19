from src.models.contacts import AddressBook, Record
from src.models.contacts import (
    add_contact,
    change,
    delete_contact,
    phone,
    show_all,
    add_city,
    add_email,
    add_birthday,
    show_birthday,
    birthdays
)
from src.utils.serializers import save_data, load_data
from colorama import init, Fore
from prettytable import PrettyTable

init(autoreset=True)

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    command = parts[0].lower()
    args = parts[1:]
    return command, args

def main():
    book = load_data()
    print(Fore.GREEN + "Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)
        # command = input("Enter a command: ").strip().lower()

        if command == "exit":
            save_data(book)
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
            print(change(args, book))

        elif command == "delete":
            print(delete_contact(args, book))

        elif command == "phone":
            print(phone(args, book))
    
        elif command == "all":
            table = PrettyTable(["Name", "City", "Phones", "Email", "Birthday"])
            for record in book.data.values():
                table.add_row([record.name.value,
                               record.city,
                               ', '.join(p.value for p in record.phones),
                               record.email,
                               record.birthday])
            print(table)

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
            print(Fore.RED + "Unknown command.")


if __name__ == "__main__":
    main()

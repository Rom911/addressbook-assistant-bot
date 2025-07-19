from src.models.contacts import AddressBook, Record
from src.utils.serializers import save_data, load_data
from colorama import init, Fore
from prettytable import PrettyTable

init(autoreset=True)


def main():
    book = load_data()
    print(Fore.GREEN + "Welcome to the assistant bot!")

    while True:
        command = input("Enter a command: ").strip().lower()

        if command == "exit":
            save_data(book)
            print("Good bye!")
            break

        elif command == "all":
            table = PrettyTable(["Name", "Phones", "Email", "Birthday", "Address"])
            for record in book.data.values():
                table.add_row([record.name.value,
                               ', '.join(p.value for p in record.phones),
                               record.email,
                               record.birthday,
                               record.address])
            print(table)

        else:
            print(Fore.RED + "Unknown command.")


if __name__ == "__main__":
    main()

from src.models.contacts import AddressBook
from src.services.serialization import load_book
from src.commands import *
from colorama import init, Fore, Back, Style
from rich.console import Console

console = Console()

init(autoreset=True)

def main():
    book = AddressBook.load_from_file()

    # print(Fore.CYAN + Style.BRIGHT + "Welcome to the assistant bot!")
    # print(show_help([]))
    console.print("[bold cyan]Welcome to the Assistant Bot![/bold cyan]")
    show_help()

    while True:
        # user_input = input(Fore.YELLOW + "Enter a command: ").strip()
        user_input = input(Fore.YELLOW + "Enter a command: " + Style.RESET_ALL)
        # user_input = input(Fore.WHITE + "Enter a command: ")

        if not user_input:
            continue

        command, *args = parse_input(user_input)

        # if not command:
        #     continue

        if command in ["close", "exit"]:
            save_data(book)
            print(Fore.GREEN + "Good bye! Data saved.")
            break

        elif command in COMMANDS:
            print(COMMANDS[command](args, book))

        # handler = COMMANDS.get(command)
        # if handler:
        #     print(handler(args, book))
        else:
            # print(Fore.RED + "Unknown command. Type 'help' to see available commands.")
            console.print("[bold red]Unknown command. Type 'help' to see available commands.[/bold red]")

if __name__ == "__main__":
    main()


# def main():
#     book = AddressBook.load_from_file()
#     print(Fore.CYAN + "Welcome to the assistant bot!")

#     # Показати help при запуску
#     print(show_help([], book))  # якщо show_help приймає book
#     # або просто
#     # print(show_help([]))

#     while True:
#         user_input = input(Fore.WHITE + "Enter a command: ")
#         command, args = parse_input(user_input)

#         if not command:
#             continue

#         handler = COMMANDS.get(command)
#         if handler:
#             print(handler(args, book))
#         else:
#             print(Fore.RED + "Unknown command. Type 'help' to see available commands.")

# def show_help(*args):
#     table = PrettyTable()
#     table.field_names = ["Command", "Description"]

#     table.add_rows([
#         ["hello", Fore.GREEN + "Greet the user"],
#         ["add [name] [phone]", Fore.GREEN + "Add new contact or phone"],
#         # Додай інші команди аналогічно
#     ])

#     return table

# from rich.console import Console
# console = Console()

# def main():
#     console.print("[bold cyan]Welcome to the Assistant Bot![/bold cyan]")
#     show_help()  # Показываем help сразу при запуске

#     while True:
#         user_input = input(Fore.YELLOW + "Enter a command: " + Style.RESET_ALL)

#         if not user_input:
#             continue

#         command, *args = parse_input(user_input)

#         if command in COMMANDS:
#             result = COMMANDS[command](args, book)
#             if result:
#                 console.print(result)
#         else:
#             console.print("[bold red]Unknown command.[/bold red]")

from src.models.contacts import AddressBook
from src.models.notes import Notes
from src.utils.autocomplete import smart_guess
from src.storage.persistence import load_contacts, save_contacts, load_notes, save_notes
from src.commands import COMMANDS, parse_input, show_help
from colorama import init, Fore, Style
from rich.console import Console

console = Console()
init(autoreset=True)

# Aliases for commands
ALIASES = {
    "quit": "exit",
    "bye": "exit",
    "create": "add",
    "remove": "delete-contact",
}

def main():
    book = load_contacts()
    notes = load_notes()

    console.print("[bold cyan]Welcome to the Assistant Bot![/bold cyan]")
    show_help()

    while True:
        try:
            user_input = input(Fore.YELLOW + "Enter a command: " + Style.RESET_ALL)

            if not user_input:
                continue

            command, args = parse_input(user_input)

            guessed_command = smart_guess(command, COMMANDS, ALIASES)

            if guessed_command in ["close", "exit"]:
                save_contacts(book)
                save_notes(notes)
                print(Fore.GREEN + "Good bye! Data saved.")
                break

            elif guessed_command in COMMANDS:
                result = COMMANDS[guessed_command](args, book, notes)
                if result:
                    print(result)

            else:
                console.print(f"[bold red]Unknown command '{command}'. Type 'help' to see available commands.[/bold red]")

        except Exception as e:
            console.print(f"[bold red]Unexpected error: {e}[/bold red]")

if __name__ == "__main__":
    main()

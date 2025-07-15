
AddressBook Assistant Bot

---

A "Console assistant bot" written in Python to manage your contacts, phone numbers, and birthdays with persistent storage using "pickle serislization".

---

Features

✅ Add, edit, delete contacts  
✅ Store multiple phone numbers per contact  
✅ Add and show birthdays  
✅ View upcoming birthdays within a week  
✅ Persistent storage with `pickle` – data is saved on exit and loaded on start  
✅ Command Line Interface (CLI)

---

Available commands

| Command                                 | Description                                  |
| --------------------------------------- | -------------------------------------------- |
| `hello`                                 | Greets the user                              |
| `add [name] [phone]`                    | Add new contact or phone to existing contact |
| `change [name] [old_phone] [new_phone]` | Change existing phone number                 |
| `phone [name]`                          | Show phone numbers for contact               |
| `all`                                   | Show all contacts                            |
| `add-birthday [name] [DD.MM.YYYY]`      | Add birthday to contact                      |
| `show-birthday [name]`                  | Show birthday of contact                     |
| `birthdays`                             | Show upcoming birthdays within a week        |
| `close` or `exit`                       | Exit and save data                           |

---

Author

[Roman Labonin](https://github.com/Rom911)
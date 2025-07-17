<!-- 
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

[Roman Labonin](https://github.com/Rom911) -->

###############################3

# AddressBook Assistant Bot

## 🇺🇦 Опис

CLI бот-асистент для управління контактами, днями народження, адресами, email та нотатками.

### 🔧 Функціонал:

- Додавання, редагування, видалення контактів
- Збереження номерів телефонів з валідацією міжнародного формату
- Додавання та перегляд email з валідацією
- Додавання адрес (країна, місто, вулиця, будинок, квартира)
- Збереження дня народження та перегляд ДН у межах заданих дат
- Нотатки: створення, редагування, видалення, пошук, теги, сортування
- Серіалізація даних (pickle)
- Кольоровий вивід (colorama)
- Красиві таблиці (prettytable)
- Структура SRC + запуск через pyproject.toml

---

## 🇬🇧 Description

CLI assistant bot for managing contacts, birthdays, addresses, emails, and notes.

### 🔧 Features:

- Add, edit, delete contacts
- Phone validation (international format)
- Email validation
- Add address (country, city, street, building, apartment)
- Save birthdays and view upcoming birthdays within date range
- Notes: create, edit, delete, search, tags, sort
- Data serialization with pickle
- Colorful CLI output (colorama)
- Pretty tables (prettytable)
- SRC project structure + pyproject.toml for easy installation

---

## 🚀 **Installation**

1. Clone the repository:

git clone https://github.com/Rom911/addressbook-assistant-bot
cd addressbook-assistant-bot

2. Install dependencies:

pip install -e .

3. Run:

python src/main.py

---

## 👥 **Authors**

- Roman
- Maksym
- Andriy

---

## 📄 License

This project is licensed under the MIT License.

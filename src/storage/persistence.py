import pickle
from src.models.contacts import AddressBook
from src.models.notes import Notes

CONTACTS_FILE = "addressbook.pkl"
NOTES_FILE = "notes.pkl"

# ------------------------------
# AddressBook persistence
# ------------------------------

def save_contacts(book, filename=CONTACTS_FILE):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_contacts(filename=CONTACTS_FILE):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

# ------------------------------
# Notes persistence
# ------------------------------

def save_notes(notes, filename=NOTES_FILE):
    with open(filename, "wb") as f:
        pickle.dump(notes, f)

def load_notes(filename=NOTES_FILE):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return Notes()

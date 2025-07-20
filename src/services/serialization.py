import pickle
from src.models.contacts import AddressBook

FILENAME = "addressbook.pkl"

def save_book(book, filename=FILENAME):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_book(filename=FILENAME):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

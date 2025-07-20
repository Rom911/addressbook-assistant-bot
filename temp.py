# # import pickle

# # class AddressBook(UserDict):
# #     # твои методы add_record, find, delete, change_phone и тд

# #     def save_to_file(self, filename="addressbook.pkl"):
# #         with open(filename, "wb") as f:
# #             pickle.dump(self.data, f)

# #     @classmethod
# #     def load_from_file(cls, filename="addressbook.pkl"):
# #         try:
# #             with open(filename, "rb") as f:
# #                 data = pickle.load(f)
# #                 book = cls()
# #                 book.data = data
# #                 return book
# #         except FileNotFoundError:
# #             return cls()
# from decorators import input_error
# import sys
# from colorama import Fore

# @input_error
# def exit_bot(args, book):
#     print(Fore.YELLOW + "Saving data and exiting... Goodbye!")
#     book.save_to_file()  # сохраняем данные перед выходом
#     sys.exit()

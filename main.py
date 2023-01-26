import time, json, datetime
from pprint import pprint
import pickle
import os
import traceback
# We declare a singleton metaclass so we can have only one instance of the Catalogue class
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



class Book:
    """ Book class represents a single book in the library """
    def __init__(self, title, author : str, isbn : str):
        self.title : str = title
        self.author : str = author
        self.isbn : str = isbn
        self.category : Category = None

    def assign_category(self, category):
        self.category = category

    def list_all_books(self,title,author,isbn,category):
        """ List all the books in the library """
        print(f"{self.title} by {self.author} in {self.category.name}")
        

    # def load_book_from_json(self, file):
    #     """ Load a book from a json file \n
    #         `file` is the file to load the book from"""
    #     with open(file) as f:
    #         data = json.load(f)
    #         self.title = data["title"]
    #         self.author = data["author"]
    #         self.isbn = data["isbn"]
    #         self.category = data["category"]

class Category:
    """ Category class represents a category of books in the library """
    def __init__(self, name : str):
        self.name : str = name
        self.books : list[Book] = []

    def add_book(self, book : Book):
        """ Add a book to the category \n
            `book` is the book to add to the category"""
        self.books.append(book)
        print(f"{book.title} added to category: {self.name}")
        book.assign_category(self)

    def remove_book(self, book):
        """ Remove a book from the category\n
            `book` is the book to remove from the category"""
        self.books.remove(book)

    def list_books(self):
        """ List all the books in the category """
        for book in self.books:
            print(f"{book.title} by {book.author}")
    

class Catalogue(metaclass=Singleton):
    """ Catalogue class represents the library catalogue, contains all the categories"""
    def __init__(self, categories : list[Category]=[]):
        self.categories : list = categories

    def add_category(self, category):
        """ Add a category to the catalogue \n
            `category` is the category to add to the catalogue"""
        self.categories.append(category)

    def remove_category(self, category):
        """ Remove a category from the catalogue \n
            `category` is the category to remove from the catalogue"""

        self.categories.remove(category)

    def list_categories(self, books=True):
        """ List all the categories in the catalogue \n
            `books` is a boolean that determines whether to list the books in the categories"""
        for category in self.categories:
            print(category.name)
            if books:
                category.list_books()
                print("")

    def save_catalogue(self, file, mkdirs=True, override_if_exists=False) -> bool:
        """ """
        # Check if the file exists
        if os.path.isfile(file) and not override_if_exists:
            print("File already exists")
            return False
        else:
            # Get the file path
            path = os.path.dirname(file)
            if not os.path.isdir(path):
                if mkdirs:
                    os.makedirs(path)
                else:
                    print("Path does not exist and mkdirs is False")
                    return False

            with open(file, "wb") as f:
                pickle.dump(self, f)
    @staticmethod
    def load_catalogue(file) -> "Catalogue":
        if os.path.isfile(file):
            with open(file, "rb") as f:
                try:
                    catalogue = pickle.load(f)
                    return catalogue
                except Exception: # Too broad
                    print("File is not a valid catalogue file")
                    traceback.print_exc()
                    # TODO maybe check if the catalogue is actually a catalogue
                    # self.validate()
                    return None
        else:
            print("File does not exist")
            return None

    def search(self, query, first_occurence=False, search_types : list[str]=["category", "book"]):
        """ Search the catalogue for a book \n
            `query` is the query to search for"""

        for category in self.categories:
            if "category" in search_types:
                if query.lower() in category.name.lower():
                    print(f"Found category {category.name}")
                    if first_occurence:
                        break
            if "book" in search_types:
                for book in category.books:
                    if query.lower() in book.title.lower() or query.lower() in book.author.lower() or query.lower() in book.isbn.lower():
                        print(f"Found {book.title} by {book.author} in {category.name}")
                        if first_occurence:
                            break

class User:
    def __init__(self, name):
        self.name : str = name
        self.orders : list[Order] = []
    # List all the users in the library
    def list_all_users(self):
        print(f"{self.name}")


class Receipt:
    def __init__(self):
        pass

class Order:
    """ Order class represents an order made by a user """
    def __init__(self, book : Book, borrower : User, date_due : float):
        self.book : Book = book
        self.borrower : User = borrower
        self.date_borrowed : datetime.date = time.time()
        self.date_due : float = date_due
    # def create_order(self, book, borrower):
    #     """ Create an order for a book \n
    #         `book` is the book to order \n
    #         `borrower` is the user who is borrowing the book"""
    #     self.book = book
    #     self.borrower = borrower
    #     self.date_borrowed = datetime.date.today()
    #     self.date_due = self.date_borrowed + datetime.timedelta(days=7)
    #     self.borrower.orders.append(self)

    def check_due(self):
        """ Check if the order is due """
        if time.time() >= self.date_due:
            return True
        else:
            return False

    def print_due(self):
        """ Prints the due date in a readable format """
        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.date_due)))

    def print_borrowed(self):
        """ Prints the borrowed date in a readable format """
        print(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime(self.date_borrowed)))

# Subclasses of Book
class Dictionary(Book):
    def __init__(self, title, author, isbn, language):
        super().__init__(title, author, isbn)
        self.language = language

class Encyclopedia(Book):
    def __init__(self, title, author, isbn, subject):
        super().__init__(title, author, isbn)
        self.subject = subject

class Magazine(Book):
    def __init__(self, title, author, isbn, issue):
        super().__init__(title, author, isbn)
        self.issue = issue

class Newspaper(Book):
    def __init__(self, title, author, isbn, issue):
        super().__init__(title, author, isbn)
        self.issue = issue


if __name__ == "__main__":
    # # Create a catalogue
    # catalogue = Catalogue()

    # # Create categories
    # category_fantasy = Category("Fantasy")
    # category_sci_fi = Category("Science fiction")
    # category_mystery = Category("Mystery")
    # category_romance = Category("Romance")

    # # Add the categories to the catalogue
    # catalogue.add_category(category_fantasy)
    # catalogue.add_category(category_sci_fi)
    # catalogue.add_category(category_mystery)
    # catalogue.add_category(category_romance)

    # # Create books
    # book_hp = Book("Harry Potter", "J.K Rowling", "123456789")
    # book_lotr = Book("The Lord of the Rings", "J.R.R. Tolkien", "987654321")
    # book_hgttg = Book("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", "123987654")
    # book_moby = Book("Moby-Dick", "Herman Melville", "2468101214")
    # book_alice = Book("Alice's Adventures in Wonderland", "Lewis Carroll", "1357913579")
    # book_dune = Book("Dune", "Frank Herbert", "123456789")
    # book_neuromancer = Book("Neuromancer", "William Gibson", "987654321")
    # book_enders = Book("Ender's Game", "Orson Scott Card", "123987654")
    # book_agatha = Book("Murder on the Orient Express", "Agatha Christie", "2468101214")
    # book_pride = Book("Pride and Prejudice", "Jane Austen", "1357913579")

    # # Add the books to categories
    # category_fantasy.add_book(book_hp)
    # category_fantasy.add_book(book_lotr)

    # category_sci_fi.add_book(book_hgttg)
    # category_sci_fi.add_book(book_dune)
    # category_sci_fi.add_book(book_neuromancer)
    # category_sci_fi.add_book(book_enders)

    # category_mystery.add_book(book_moby)
    # category_mystery.add_book(book_agatha)

    # category_romance.add_book(book_alice)
    # category_romance.add_book(book_pride)

    # # Create users
    # user_jd = User("John Doe")
    # user_jane = User("Jane Smith")
    # user_alice = User("Alice Johnson")
    # user_bob = User("Bob Williams")


    # order1 = Order(book_hgttg, user_alice, time.time() + 2)
    # order2 = Order(book_dune, user_bob, time.time() + 2)
    # order3 = Order(book_hgttg, user_alice, time.time() + 2)
    # order4 = Order(book_dune, user_bob, time.time() + 2)
    # order5 = Order(book_neuromancer, user_jd, time.time() + 2)
    # order6 = Order(book_agatha, user_jane, time.time() + 2)
    # order7 = Order(book_pride, user_alice, time.time() + 2)
    # order8 = Order(book_enders, user_bob, time.time() + 2)
    my_catalogue = Catalogue.load_catalogue(f"{os.getcwd()}\\saved\\TestCatalogue.catalogue")
# Write a console interface for the library
    print("Welcome to the library!")
    print("Please select an option:")
    print("1. List all categories")
    print("2. List all books in a category")
    print("3. List all users")
    print("4. List all orders")
    print("5. Add a book")
    print("6. Add a category")
    print("7. Add a user")
    print("8. Add an order")
    print("9. Save catalogue")
    print("10. Load catalogue")
    print("11. Exit")
    
    while True:
        option = input("Please select an option: ")
        if option == "2":
            print("Please select a category:")
            my_catalogue.list_categories()
            category = input("Please select a category: ")
            Category.list_books(category)
        elif option == "1":
            my_catalogue.list_categories()
        elif option == "3":
            User.list_all_users()
        elif option == "4":
            Catalogue.list_orders()
        elif option == "5":
            title = input("Please enter the title of the book: ")
            author = input("Please enter the author of the book: ")
            isbn = input("Please enter the ISBN of the book: ")
            book = Book(title, author, isbn)
            Category.add_book(book)
        elif option == "6":
            name = input("Please enter the name of the category: ")
            category = Category(name)
            Catalogue.add_category(category)
        elif option == "7":
            name = input("Please enter the name of the user: ")
            user = User(name)
            Catalogue.add_user(user)
        elif option == "8":
            Catalogue.list_books()
            book_id = input("Please enter the ID of the book: ")
            Catalogue.list_users()
            user_id = input("Please enter the ID of the user: ")
            order = Order(Catalogue.books[int(book_id)], Catalogue.users[int(user_id)], time.time() + 2)
            Catalogue.add_order(order)
        elif option == "9":
            Catalogue.save_catalogue(f"{os.getcwd()}\\saved\\TestCatalogue.catalogue")
        elif option == "10":
            Catalogue.load_catalogue(f"{os.getcwd()}\\saved\\TestCatalogue.catalogue")
        elif option == "11":
            break
        else:
            print("Please enter a valid option")


    # my_catalogue = Catalogue.load_catalogue(f"{os.getcwd()}\\saved\\TestCatalogue.catalogue")
    # my_catalogue.list_categories()
    # my_catalogue.save_catalogue(f"{os.getcwd()}}\\saved\\TestCatalogue.catalogue")
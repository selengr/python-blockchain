# library.py

class Library:
    def __init__(self):
        self.books = []   

    def add_book(self, title, author):
        self.books.append({"title": title, "author": author})

    def remove_book(self, title):
        for book in self.books:
            if book["title"] == title:
                self.books.remove(book)
                return True
        return False

    def search_book(self, title):
        for book in self.books:
            if book["title"] == title:
                return book
        return None

    def show_books(self):
        if not self.books:
            print("هیچ کتابی در کتابخانه وجود ندارد.")
        else:
            for book in self.books:
                print(f"{book['title']} - {book['author']}")

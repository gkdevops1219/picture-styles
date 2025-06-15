import json
import os
from typing import List, Dict, Optional, Callable
from functools import wraps

# Decorator for error handling
def handle_errors(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(f"Error: {e}")
    return wrapper


# Base class for a book
class Book:
    def __init__(self, title: str, author: str, year: int, genre: str):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre

    def __str__(self):
        return f"'{self.title}' by {self.author} ({self.year}) - Genre: {self.genre}"

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "genre": self.genre,
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data["genre"]
        )


# Derived class: SpecialBook with rating
class SpecialBook(Book):
    def __init__(self, title: str, author: str, year: int, genre: str, rating: float):
        super().__init__(title, author, year, genre)
        self.rating = rating

    def __str__(self):
        return super().__str__() + f" | Rating: {self.rating}/5"

    def to_dict(self) -> Dict:
        data = super().to_dict()
        data["rating"] = self.rating
        data["type"] = "SpecialBook"
        return data

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            title=data["title"],
            author=data["author"],
            year=data["year"],
            genre=data["genre"],
            rating=data.get("rating", 0.0)
        )


# Library class to manage books
class Library:
    def __init__(self, data_file: str = "library.json"):
        self.books: List[Book] = []
        self.data_file = data_file
        self.load_books()

    def save_books(self):
        with open(self.data_file, "w") as f:
            json.dump([book.to_dict() for book in self.books], f, indent=4)
        print("📚 Library saved.")

    def load_books(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as f:
                data = json.load(f)
                for book_data in data:
                    if book_data.get("type") == "SpecialBook":
                        self.books.append(SpecialBook.from_dict(book_data))
                    else:
                        self.books.append(Book.from_dict(book_data))
            print("📖 Library loaded.")
        else:
            print("📖 No saved library found. Starting fresh.")

    def add_book(self, book: Book):
        self.books.append(book)
        print(f"✅ Book added: {book}")
        self.save_books()

    def list_books(self):
        if not self.books:
            print("No books in library.")
        for i, book in enumerate(self.books, 1):
            print(f"{i}. {book}")

    def search_by_title(self, keyword: str):
        found = [book for book in self.books if keyword.lower() in book.title.lower()]
        if found:
            print(f"🔍 Found {len(found)} book(s):")
            for book in found:
                print(f"   - {book}")
        else:
            print("🔍 No books matched your search.")

    def delete_book(self, index: int):
        try:
            removed = self.books.pop(index - 1)
            print(f"🗑️ Removed book: {removed}")
            self.save_books()
        except IndexError:
            print("❌ Invalid book index.")


# Main menu
@handle_errors
def main():
    lib = Library()

    while True:
        print("\n=== 📚 Personal Book Library ===")
        print("1. Add Book")
        print("2. List Books")
        print("3. Search Book by Title")
        print("4. Delete Book")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            title = input("Title: ")
            author = input("Author: ")
            year = int(input("Year: "))
            genre = input("Genre: ")
            is_special = input("Is it a special book (with rating)? (y/n): ").strip().lower()

            if is_special == "y":
                rating = float(input("Rating (0-5): "))
                book = SpecialBook(title, author, year, genre, rating)
            else:
                book = Book(title, author, year, genre)

            lib.add_book(book)

        elif choice == "2":
            lib.list_books()

        elif choice == "3":
            keyword = input("Enter title keyword to search: ")
            lib.search_by_title(keyword)

        elif choice == "4":
            lib.list_books()
            index = int(input("Enter book number to delete: "))
            lib.delete_book(index)

        elif choice == "5":
            print("👋 Exiting the library. Bye!")
            break

        else:
            print("❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

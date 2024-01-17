import tkinter as tk
from tkinter import messagebox
import sqlite3

class Library:
    def __init__(self):
        self.conn = sqlite3.connect('library.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                available BOOLEAN NOT NULL
            )
        ''')
        self.conn.commit()

    def add_book(self, title, author):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO books (title, author, available) VALUES (?, ?, ?)', (title, author, True))
        self.conn.commit()
        messagebox.showinfo("Add Book", "Book added successfully.")

    def display_books(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

        book_list = []
        for book in books:
            book_list.append(f"{book[0]}\t{book[1]}\t{book[2]}\t{'Available' if book[3] else 'Borrowed'}")

        messagebox.showinfo("Display Books", "\n".join(book_list))

    def borrow_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
        book = cursor.fetchone()

        if book and book[3]:  # Book exists and is available
            cursor.execute('UPDATE books SET available=? WHERE id=?', (False, book_id))
            self.conn.commit()
            messagebox.showinfo("Borrow Book", f"Book with ID {book_id} borrowed successfully.")
        elif not book:
            messagebox.showerror("Borrow Book", f"Book with ID {book_id} not found.")
        else:
            messagebox.showerror("Borrow Book", f"Book with ID {book_id} is not available for borrowing.")

    def return_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM books WHERE id=?', (book_id,))
        book = cursor.fetchone()

        if book and not book[3]:  # Book exists and is borrowed
            cursor.execute('UPDATE books SET available=? WHERE id=?', (True, book_id))
            self.conn.commit()
            messagebox.showinfo("Return Book", f"Book with ID {book_id} returned successfully.")
        elif not book:
            messagebox.showerror("Return Book", f"Book with ID {book_id} not found.")
        else:
            messagebox.showerror("Return Book", f"Invalid book ID or the book is already available.")

class LibraryManagementSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")

        self.library = Library()

        # Labels
        tk.Label(self.root, text="Title:").grid(row=0, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Author:").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.root, text="Book ID:").grid(row=2, column=0, padx=10, pady=5)

        # Entry widgets
        self.title_entry = tk.Entry(self.root)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)
        self.author_entry = tk.Entry(self.root)
        self.author_entry.grid(row=1, column=1, padx=10, pady=5)
        self.book_id_entry = tk.Entry(self.root)
        self.book_id_entry.grid(row=2, column=1, padx=10, pady=5)

        # Buttons
        tk.Button(self.root, text="Add Book", command=self.add_book).grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Display Books", command=self.display_books).grid(row=4, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Borrow Book", command=self.borrow_book).grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(self.root, text="Return Book", command=self.return_book).grid(row=6, column=0, columnspan=2, pady=10)

    def add_book(self):
        title = self.title_entry.get()
        author = self.author_entry.get()
        self.library.add_book(title, author)

    def display_books(self):
        self.library.display_books()

    def borrow_book(self):
        book_id = self.book_id_entry.get()
        self.library.borrow_book(book_id)

    def return_book(self):
        book_id = self.book_id_entry.get()
        self.library.return_book(book_id)

# Main application loop
if __name__ == "__main__":
    root = tk.Tk()
    app = LibraryManagementSystemGUI(root)
    root.mainloop()

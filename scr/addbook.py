import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql

con = sql.connect('library.db')
cur = con.cursor()

class AddBook(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("450x300+550+200")
        self.title("Add Book")
        self.resizable(False, False)

        # Labels and Entries
        self.lbl_name = tk.Label(self, text='Book Name:', font='Arial 12 bold')
        self.lbl_name.grid(row=0, column=0, padx=20, pady=(20, 5), sticky=tk.E)
        self.ent_name = tk.Entry(self, font='Arial 12')
        self.ent_name.grid(row=0, column=1, padx=20, pady=(20, 5))

        self.lbl_author = tk.Label(self, text='Author:', font='Arial 12 bold')
        self.lbl_author.grid(row=1, column=0, padx=20, pady=5, sticky=tk.E)
        self.ent_author = tk.Entry(self, font='Arial 12')
        self.ent_author.grid(row=1, column=1, padx=20, pady=5)

        # Add Book Button
        self.btn_add_book = tk.Button(self, text='Add Book', font='Arial 12 bold', fg='white', bg='#003f8a', command=self.addBook)
        self.btn_add_book.grid(row=2, columnspan=2, pady=20)
        self.btn_add_book.config(width=20)

    def addBook(self):
        book_name = self.ent_name.get().strip()
        book_author = self.ent_author.get().strip()

        if book_name and book_author:
            try:
                query = "INSERT INTO books (book_name, book_author, book_status) VALUES (?, ?, ?)"
                cur.execute(query, (book_name, book_author, 0))  # Setting book_status to 0 for available
                con.commit()

                messagebox.showinfo("Success", "Book added successfully!", icon='info')
                self.destroy()  # Close the AddBook window after successful operation

            except sql.IntegrityError:
                messagebox.showerror("Error", "Book already exists in the database", icon='warning')

            except Exception as e:
                messagebox.showerror("Error", f"Failed to add book: {str(e)}", icon='warning')

        else:
            messagebox.showerror("Error", "Please enter both book name and author", icon='warning')

if __name__ == '__main__':
    root = tk.Tk()
    app = AddBook()
    root.mainloop()

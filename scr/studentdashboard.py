import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import sqlite3 as sql
from tkinter import messagebox
from datetime import datetime

con = sql.connect('library.db')
cur = con.cursor()

class StudentDashboard(tk.Toplevel):
    def __init__(self, student_id):
        super().__init__()
        self.geometry("1350x750+350+200")
        self.title("Student Dashboard")
        self.student_id = student_id

        # Icon
        self.iconbitmap(r'C:\Users\Admin\Desktop\RAAM\icons\student.ico') 

        # Fetching student name
        self.student_name = cur.execute("SELECT student_name FROM student WHERE student_id=?", (self.student_id,)).fetchone()[0]

        # Main Frame
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=True)

        # Top Frame
        self.topFrame = Frame(mainFrame, bg='#f8f8f8', relief=SUNKEN, bd=2)
        self.topFrame.pack(side=TOP, fill=X)

        # Center Frame
        centerFrame = Frame(mainFrame, bg="#e0f0f0", relief=RIDGE, bd=2)
        centerFrame.pack(fill=BOTH, expand=True)

        # Left Frame
        leftFrame = Frame(centerFrame, bg='#e0f0f0', bd=2)
        leftFrame.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=True)

        # Right Frame
        rightFrame = Frame(centerFrame, bg='#e0f0f0', bd=2)
        rightFrame.pack(side=RIGHT, padx=10, pady=10, fill=Y)

        # Top Frame Widgets
        self.btn_borrow_book = Button(self.topFrame, text='Borrow a Book', font='Arial 12 bold', command=self.borrowBook)
        self.btn_return_book = Button(self.topFrame, text='Return Book', font='Arial 12 bold', command=self.returnBook)

        # Left Frame Widgets
        # Search Bar
        search_bar = LabelFrame(leftFrame, text='', bg='#9bc9ff', font='Arial 12 bold')
        search_bar.pack(fill=X, padx=10, pady=10)

        self.lbl_search = Label(search_bar, text='Search :', bg='#9bc9ff', fg='white', font='Arial 12 bold')
        self.lbl_search.grid(row=0, column=0, padx=10, pady=10)

        self.ent_search = Entry(search_bar, width=30, bd=5, font='Arial 12')
        self.ent_search.grid(row=0, column=1, padx=10, pady=10)

        self.btn_search = Button(search_bar, text='Search', bg='#fcc324', fg='white', font='Arial 12 bold', command=self.searchBooks)
        self.btn_search.grid(row=0, column=2, padx=10, pady=10)

        # Table (Treeview) for displaying books
        self.tree = ttk.Treeview(leftFrame, columns=("Book ID", "Book Name", "Author", "Status"), show="headings", height=25)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True)

        self.tree.heading("Book ID", text="Book ID", anchor=W)
        self.tree.heading("Book Name", text="Book Name", anchor=W)
        self.tree.heading("Author", text="Author", anchor=W)
        self.tree.heading("Status", text="Status", anchor=W)

        self.sb = Scrollbar(leftFrame, orient=VERTICAL, command=self.tree.yview)
        self.sb.pack(side=RIGHT, fill=Y)
        self.tree.config(yscrollcommand=self.sb.set)

        # Right Frame Widgets
        # Image and Title
        image_bar = Frame(rightFrame, width=400, height=300, bd=2, relief=SUNKEN)
        image_bar.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.title_right = Label(image_bar, text=f'Welcome {self.student_name} to our Library', font='Arial 16 bold')
        self.title_right.pack(pady=20)

        try:
            img = Image.open('icons/libr.png')
            img = img.resize((400, 250), Image.LANCZOS)
            self.img_library = ImageTk.PhotoImage(img)

            self.lblImg = Label(image_bar, image=self.img_library)
            self.lblImg.pack()
        except Exception as e:
            print(f"Error loading image: {e}")
            self.lblImg = Label(image_bar, text="Image not available", font='Arial 12')
            self.lblImg.pack()

        # Radio Buttons for Listing Options
        list_options = LabelFrame(rightFrame, text='List Options', bg='#fcc324', font='Arial 12 bold')
        list_options.pack(fill=X, padx=10, pady=10)

        self.listChoice = IntVar()
        self.listChoice.set(1)  # Default to 'All Books'
        rb1 = Radiobutton(list_options, text='All Books', variable=self.listChoice, value=1, bg='#fcc324', font='Arial 12', command=self.updateBooksList)
        rb1.grid(row=0, column=0, padx=10, pady=5)

        rb2 = Radiobutton(list_options, text='In Library', variable=self.listChoice, value=2, bg='#fcc324', font='Arial 12', command=self.updateBooksList)
        rb2.grid(row=0, column=1, padx=10, pady=5)

        rb3 = Radiobutton(list_options, text='Borrowed Books', variable=self.listChoice, value=3, bg='#fcc324', font='Arial 12', command=self.updateBooksList)
        rb3.grid(row=0, column=2, padx=10, pady=5)

        btn_list = Button(list_options, text='List Books', bg='#2488ff', fg='white', font='Arial 12 bold', command=self.listBooks)
        btn_list.grid(row=0, column=3, padx=20, pady=10)

        # Statistics Labels
        statistics_frame = Frame(rightFrame, bd=2, relief=SUNKEN)
        statistics_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.lbl_book_count = Label(statistics_frame, text="", font='Arial 14 bold')
        self.lbl_book_count.pack(pady=10, anchor=W)

        self.lbl_borrowed_count = Label(statistics_frame, text="", font='Arial 14 bold')
        self.lbl_borrowed_count.pack(pady=10, anchor=W)

        # Logout Button
        btn_logout = Button(statistics_frame, text='Logout', bg='red', fg='white', font='Arial 12 bold', command=self.logout)
        btn_logout.pack(pady=10)

        # Initialize the UI
        self.displayBooks()
        self.displayStatistics()
        self.updateButtons()
        self.center_window()

    def center_window(self):
        
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        
        x = (screen_width // 2) - (1350 // 2)  
        y = (screen_height // 2) - (750 // 2)  

        self.geometry(f"1350x750+{x}+{y}")

    def displayBooks(self):
        books = cur.execute("SELECT book_id, book_name, book_author, book_status FROM books").fetchall()
        self.tree.delete(*self.tree.get_children())
        for book in books:
            status = "Available" if book[3] == 0 else "Borrowed"
            self.tree.insert("", "end", values=(book[0], book[1], book[2], status))

    def searchBooks(self):
        value = self.ent_search.get()
        try:
            search = cur.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%' + value + '%',)).fetchall()
            self.tree.delete(*self.tree.get_children())
            for book in search:
                status = "Available" if book[3] == 0 else "Borrowed"
                self.tree.insert("", "end", values=(book[0], book[1], book[2], status))
        except Exception as e:
            print(f"Error searching books: {str(e)}")

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks = cur.execute("SELECT book_id, book_name, book_author, book_status FROM books").fetchall()
            self.tree.delete(*self.tree.get_children())
            for book in allbooks:
                status = "Available" if book[3] == 0 else "Borrowed"
                self.tree.insert("", "end", values=(book[0], book[1], book[2], status))
        elif value == 2:
            books_in_library = cur.execute("SELECT book_id, book_name, book_author, book_status FROM books WHERE book_status=?", (0,)).fetchall()
            self.tree.delete(*self.tree.get_children())
            for book in books_in_library:
                self.tree.insert("", "end", values=(book[0], book[1], book[2], "Available"))
        elif value == 3:
            taken_books = cur.execute("SELECT b.book_id, b.book_name, b.book_author, b.book_status FROM books b JOIN borrows br ON b.book_id = br.book_id WHERE br.student_id=? AND br.return_date IS NULL", (self.student_id,)).fetchall()
            self.tree.delete(*self.tree.get_children())
            for book in taken_books:
                self.tree.insert("", "end", values=(book[0], book[1], book[2], "Borrowed"))

    def borrowBook(self):
        selected_item = self.tree.focus()
        if selected_item:
            book_id = self.tree.item(selected_item, 'values')[0]

            # Check if the book is available
            book = cur.execute("SELECT * FROM books WHERE book_id=?", (book_id,)).fetchone()
            if book and book[3] == 0:  # Book is available
                borrow_date = datetime.today().strftime('%Y-%m-%d')
                cur.execute("INSERT INTO borrows (book_id, student_id, borrow_date, status) VALUES (?, ?, ?, ?)", (book_id, self.student_id, borrow_date, 1))
                con.commit()

                cur.execute("UPDATE books SET book_status=1 WHERE book_id=?", (book_id,))
                con.commit()

                self.displayBooks()
                self.displayStatistics()

                messagebox.showinfo("Book Borrowed", f"Book '{book[1]}' borrowed successfully.")
            else:
                messagebox.showinfo("Unavailable", "The book is currently unavailable.")
        else:
            messagebox.showerror("Error", "Please select a book to borrow.")

    def returnBook(self):
        selected_item = self.tree.focus()
        if selected_item:
            book_id = self.tree.item(selected_item, 'values')[0]

            # Check if the book is borrowed by this student
            borrowed_book = cur.execute("SELECT * FROM borrows WHERE book_id=? AND student_id=? AND return_date IS NULL", (book_id, self.student_id)).fetchone()
            if borrowed_book:
                self.processReturnBook(book_id)
            else:
                messagebox.showerror("Error", "You cannot return a book you haven't borrowed.")
        else:
            messagebox.showerror("Error", "Please select a book to return.")

    def processReturnBook(self, book_id):
        return_date = datetime.today().strftime('%Y-%m-%d')
        try:
            cur.execute("UPDATE borrows SET return_date=? WHERE book_id=? AND return_date IS NULL AND student_id=?", (return_date, book_id, self.student_id))
            con.commit()

            cur.execute("UPDATE books SET book_status=0 WHERE book_id=?", (book_id,))
            con.commit()

            self.displayBooks()
            self.displayStatistics()

            messagebox.showinfo("Book Returned", f"Book '{book_id}' returned successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to return book: {str(e)}")

    def displayStatistics(self):
        count_books = cur.execute("SELECT count(book_id) FROM books").fetchone()[0]
        count_currently_borrowed = cur.execute("SELECT count(*) FROM borrows WHERE student_id=? AND return_date IS NULL", (self.student_id,)).fetchone()[0]

        self.lbl_book_count.config(text='Total Books: ' + str(count_books))
        self.lbl_borrowed_count.config(text="Books Currently Borrowed: " + str(count_currently_borrowed))

    def updateBooksList(self):
        self.listBooks()
        self.updateButtons()

    def updateButtons(self):
        for widget in self.topFrame.winfo_children():
            widget.pack_forget()

        value = self.listChoice.get()
        if value == 2:
            self.btn_borrow_book.pack(side=LEFT, padx=10, pady=10)
        elif value == 3:
            self.btn_return_book.pack(side=LEFT, padx=10, pady=10)

    def logout(self):
        self.destroy()  # Close the StudentDashboard window
        from welcomewindow import WelcomeWindow  
        root = WelcomeWindow()  # Create an instance of WelcomeWindow
        root.mainloop()  

def main():
    root = tk.Tk()
    app = StudentDashboard(student_id="123")
    root.mainloop()

if __name__ == '__main__':
    main()

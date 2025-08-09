import tkinter as tk
from tkinter import *
import tkinter.ttk as ttk
from PIL import Image, ImageTk
import sqlite3 as sql
import addbook
from tkinter import messagebox
from welcomewindow import WelcomeWindow

con = sql.connect('library.db')
cur = con.cursor()

class Main(object):
    def __init__(self, master):
        self.master = master
        self.master.title("Library Management System")
        self.master.geometry("1350x750+350+200")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x = (screen_width // 2) - (1350 // 2)
        y = (screen_height // 2) - (750 // 2)

        # Set the window to be centered
        self.master.geometry(f"1350x750+{x}+{y}")

        # Main Frame
        mainFrame = Frame(self.master)
        mainFrame.pack(fill=BOTH, expand=True)

        # Top Frame
        topFrame = Frame(mainFrame, bg='#f8f8f8', relief=SUNKEN, bd=2)
        topFrame.pack(side=TOP, fill=X)

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
        self.btnbook = Button(topFrame, text='Add Book', font='Arial 12 bold',
                              command=self.addBook)
        self.btnbook.pack(side=LEFT, padx=10, pady=10)

        # Logout Button
        btn_logout = Button(topFrame, text='Logout', bg='red', fg='white', font='Arial 12 bold', command=self.logout)
        btn_logout.pack(side=RIGHT, padx=10, pady=10)

        # Left Frame Widgets
        # Search Bar
        search_bar = LabelFrame(leftFrame, text='Search', bg='#9bc9ff', font='Arial 12 bold')
        search_bar.pack(fill=X, padx=10, pady=10)

        self.lbl_search = Label(search_bar, text='Search :', bg='#9bc9ff', fg='white', font='Arial 12 bold')
        self.lbl_search.grid(row=0, column=0, padx=10, pady=10)

        self.ent_search = Entry(search_bar, width=30, bd=5, font='Arial 12')
        self.ent_search.grid(row=0, column=1, padx=10, pady=10)

        self.btn_search = Button(search_bar, text='Search', bg='#fcc324', fg='white', font='Arial 12 bold', command=self.searchBooks)
        self.btn_search.grid(row=0, column=2, padx=10, pady=10)

        # Treeview for displaying books
        self.tree_books = ttk.Treeview(leftFrame, columns=("ID", "Name", "Author"), show="headings", height=25)
        self.tree_books.heading("ID", text="ID")
        self.tree_books.heading("Name", text="Name")
        self.tree_books.heading("Author", text="Author")
        self.tree_books.pack(fill=BOTH, expand=True)

        # Right Frame Widgets
        # Image and Title
        image_bar = Frame(rightFrame, width=400, height=300, bd=2, relief=SUNKEN)
        image_bar.pack(padx=10, pady=10, fill=BOTH, expand=True)

        self.title_right = Label(image_bar, text='Welcome to our Library', font='Arial 16 bold')
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
        rb1 = Radiobutton(list_options, text='All Books', variable=self.listChoice, value=1, bg='#fcc324', font='Arial 12', command=self.refreshBooks)
        rb1.grid(row=0, column=0, padx=10, pady=5)

        rb2 = Radiobutton(list_options, text='In Library', variable=self.listChoice, value=2, bg='#fcc324', font='Arial 12', command=self.refreshBooks)
        rb2.grid(row=0, column=1, padx=10, pady=5)

        rb3 = Radiobutton(list_options, text='Borrowed Books', variable=self.listChoice, value=3, bg='#fcc324', font='Arial 12', command=self.refreshBooks)
        rb3.grid(row=0, column=2, padx=10, pady=5)

        btn_list = Button(list_options, text='List Books', bg='#2488ff', fg='white', font='Arial 12 bold', command=self.listBooks)
        btn_list.grid(row=0, column=3, padx=20, pady=10)

        # Statistics Labels
        statistics_frame = Frame(rightFrame, bd=2, relief=SUNKEN)
        statistics_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.lbl_book_count = Label(statistics_frame, text="", font='Arial 14 bold')
        self.lbl_book_count.pack(pady=10, anchor=W)

        self.lbl_student_count = Label(statistics_frame, text="", font='Arial 14 bold')
        self.lbl_student_count.pack(pady=10, anchor=W)

        self.lbl_taken_count = Label(statistics_frame, text="", font='Arial 14 bold')
        self.lbl_taken_count.pack(pady=10, anchor=W)

        # Initialize the UI
        self.displayBooks()
        self.displayStatistics()

    def displayBooks(self):
        books = cur.execute("SELECT * FROM books").fetchall()
        self.tree_books.delete(*self.tree_books.get_children())
        for book in books:
            self.tree_books.insert("", "end", values=(book[0], book[1], book[2]))

    def addBook(self):
        add = addbook.AddBook()

    def searchBooks(self):
        value = self.ent_search.get()
        search = cur.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%' + value + '%',)).fetchall()
        self.tree_books.delete(*self.tree_books.get_children())
        for book in search:
            self.tree_books.insert("", "end", values=(book[0], book[1], book[2]))

    def listBooks(self):
        value = self.listChoice.get()
        if value == 1:
            allbooks = cur.execute("SELECT * FROM books").fetchall()
            self.tree_books.delete(*self.tree_books.get_children())
            for book in allbooks:
                self.tree_books.insert("", "end", values=(book[0], book[1], book[2]))
        elif value == 2:
            books_in_library = cur.execute("SELECT * FROM books WHERE book_status=?", (0,)).fetchall()
            self.tree_books.delete(*self.tree_books.get_children())
            for book in books_in_library:
                self.tree_books.insert("", "end", values=(book[0], book[1], book[2]))
        elif value == 3:
            taken_books = cur.execute("SELECT * FROM books WHERE book_status=?", (1,)).fetchall()
            self.tree_books.delete(*self.tree_books.get_children())
            for book in taken_books:
                self.tree_books.insert("", "end", values=(book[0], book[1], book[2]))

    def refreshBooks(self):
        self.listBooks()  # Calls the appropriate listBooks method based on radio button selection

    def displayStatistics(self, event=None):
        count_books = cur.execute("SELECT count(book_id) FROM books").fetchone()[0]
        count_students = cur.execute("SELECT count(student_id) FROM student").fetchone()[0]
        taken_books = cur.execute("SELECT count(book_status) FROM books WHERE book_status=1").fetchone()[0]

        self.lbl_book_count.config(text='Total Books: ' + str(count_books))
        self.lbl_student_count.config(text="Total Students: " + str(count_students))
        self.lbl_taken_count.config(text="Borrowed Books: " + str(taken_books))

    def logout(self):
        self.master.destroy()  # Close the Main window
        root = WelcomeWindow()  # Create an instance of WelcomeWindow
        root.mainloop()  # Start the main loop again

def main():
    root = tk.Tk()
    app = Main(root)
    root.mainloop()

if __name__ == '__main__':
    main()

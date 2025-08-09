import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql

con = sql.connect('library.db')
cur = con.cursor()

class StudentLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("650x300+550+200")
        self.title("Student Login")
        self.resizable(False, False)
        self.parent = parent
        self.logged_in = False  # Tracking login status
        self.create_widgets()

    def create_widgets(self):
        # Top Frame
        top_frame = tk.Frame(self, height=100, bg='#003f8a')
        top_frame.pack(fill=tk.X)

        # Heading
        heading = tk.Label(top_frame, text='Student Login', font='Arial 18 bold', fg='white', bg='#003f8a')
        heading.pack(pady=30)

        # Bottom Frame
        bottom_frame = tk.Frame(self, height=200, bg='#e0f0f0')
        bottom_frame.pack(fill=tk.X)

        # Login ID
        self.lbl_id = tk.Label(bottom_frame, text='ID:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_id.grid(row=0, column=2, padx=10, pady=10, sticky=tk.SE)
        self.ent_id = tk.Entry(bottom_frame, width=30, bd=4, font='Arial 12')
        self.ent_id.grid(row=0, column=3, padx=10, pady=10)

        # Password
        self.lbl_pass = tk.Label(bottom_frame, text='Password:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_pass.grid(row=1, column=2, padx=10, pady=10, sticky=tk.SE)
        self.ent_pass = tk.Entry(bottom_frame, show='*', width=30, bd=4, font='Arial 12')
        self.ent_pass.grid(row=1, column=3, padx=10, pady=10)

        # Login Button
        btn_login = tk.Button(bottom_frame, text='Login', font='Arial 12 bold', fg='white', bg='#003f8a', command=self.validate_login)
        btn_login.grid(row=2, column=3, padx=10, pady=20, sticky=tk.S)

        # Create Account Button
        btn_create_account = tk.Button(bottom_frame, text='Create Account', font='Arial 12 bold', fg='white', bg='#003f8a', command=self.open_create_account)
        btn_create_account.grid(row=3, column=3, padx=10, pady=10, sticky=tk.S)

    #function to check whether id and password is correct
    def validate_login(self):
        student_id = self.ent_id.get().strip()
        password = self.ent_pass.get().strip()

        if student_id == "" or password == "":
            messagebox.showerror("Error", "Fields cannot be empty", icon='warning')
            return False

        try:
            #checking student_id and password
            query = "SELECT * FROM student WHERE student_id=? AND password=?"
            cur.execute(query, (student_id, password))
            student = cur.fetchone()

            if student:
                self.logged_in = True  # Set login status
                self.student_id = student_id  # Store student_id
                self.destroy()  # Close the login window

                # Open StudentDashboard
                self.open_student_dashboard(student_id)

            else:
                messagebox.showerror("Login Failed", "Invalid ID or password", icon='warning')
                return False

        except Exception as e:
            messagebox.showerror("Error", f"Failed to validate login: {str(e)}", icon='warning')
            return False


    def open_create_account(self):
        create_account_window = CreateAccount(self)
        create_account_window.grab_set()

    def open_student_dashboard(self, student_id):
        from studentdashboard import StudentDashboard  # Adjust import as per your project structure
        student_dashboard = StudentDashboard(student_id)
        student_dashboard.mainloop()
#class to make a new student account
class CreateAccount(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("650x400+550+200")
        self.title("Create Account")
        self.resizable(False, False)
        self.parent = parent
        self.create_widgets()
    #creating widgets of register window
    def create_widgets(self):
        # Top Frame
        top_frame = tk.Frame(self, height=100, bg='#003f8a')
        top_frame.pack(fill=tk.X)

        # Heading
        heading = tk.Label(top_frame, text='Register', font='Arial 18 bold', fg='white', bg='#003f8a')
        heading.pack(pady=30)

        # Bottom Frame
        bottom_frame = tk.Frame(self, height=200, bg='#e0f0f0')
        bottom_frame.pack(fill=tk.X)

        # Name
        self.lbl_name = tk.Label(bottom_frame, text='Name:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_name.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)
        self.ent_name = tk.Entry(bottom_frame, width=30, bd=4, font='Arial 12')
        self.ent_name.grid(row=0, column=1, padx=10, pady=10)

        # ID
        self.lbl_id = tk.Label(bottom_frame, text='ID:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_id.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)
        self.ent_id = tk.Entry(bottom_frame, width=30, bd=4, font='Arial 12')
        self.ent_id.grid(row=1, column=1, padx=10, pady=10)

        # Password
        self.lbl_pass = tk.Label(bottom_frame, text='Password:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_pass.grid(row=2, column=0, padx=10, pady=10, sticky=tk.E)
        self.ent_pass = tk.Entry(bottom_frame, show='*', width=30, bd=4, font='Arial 12')
        self.ent_pass.grid(row=2, column=1, padx=10, pady=10)

        # Create Account Button (Centered)
        btn_create = tk.Button(bottom_frame, text='Create Account', font='Arial 12 bold', fg='white', bg='#003f8a', command=self.create_account)
        btn_create.grid(row=3, column=0, columnspan=2, pady=20)

    #function to create new student account
    def create_account(self):
        name = self.ent_name.get().strip()
        student_id = self.ent_id.get().strip()
        password = self.ent_pass.get().strip()

        if name == "" or student_id == "" or password == "":
            messagebox.showerror("Error", "Fields cannot be empty", icon='warning')
            return

        try:
            # Insert  new student into the database
            query = "INSERT INTO student (student_id, student_name, password) VALUES (?, ?, ?)"
            cur.execute(query, (student_id, name, password))
            con.commit()

            messagebox.showinfo("Success", "Account created successfully", icon='info')
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to create account: {str(e)}", icon='warning')

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentLogin(root)
    root.mainloop()

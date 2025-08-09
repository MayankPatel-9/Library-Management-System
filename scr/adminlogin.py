import tkinter as tk
from tkinter import messagebox
import sqlite3 as sql

con = sql.connect('library.db')
cur = con.cursor()

class AdminLogin(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("650x300+550+200")
        self.title("Admin Login")
        self.resizable(False, False)
        self.parent = parent
        self.create_widgets()

    #functions to create widgets
    #topframe - heading
    #bottom frame - butons and input labels
    def create_widgets(self):
        # Main Frame to center everything
        main_frame = tk.Frame(self, bg='#003f8a')
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Top Frame
        top_frame = tk.Frame(main_frame, height=100, bg='#003f8a')
        top_frame.pack(fill=tk.X, expand=True)

        # Heading
        heading = tk.Label(top_frame, text='Admin Login', font='Arial 18 bold', fg='white', bg='#003f8a')
        heading.pack(pady=30)

        # Bottom Frame
        bottom_frame = tk.Frame(main_frame, height=200, bg='#e0f0f0')
        bottom_frame.pack(fill=tk.X, expand=True)

        # Username
        self.lbl_username = tk.Label(bottom_frame, text='Username:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_username.grid(row=0, column=1, padx=10, pady=10, sticky=tk.SE)
        self.ent_username = tk.Entry(bottom_frame, width=30, bd=4, font='Arial 12')
        self.ent_username.grid(row=0, column=2, padx=10, pady=10)

        # Password
        self.lbl_pass = tk.Label(bottom_frame, text='Password:', font='Arial 12 bold', fg='#003f8a', bg='#e0f0f0')
        self.lbl_pass.grid(row=1, column=1, padx=10, pady=10, sticky=tk.SE)
        self.ent_pass = tk.Entry(bottom_frame, show='*', width=30, bd=4, font='Arial 12')
        self.ent_pass.grid(row=1, column=2, padx=10, pady=10)

        # Login Button
        btn_login = tk.Button(bottom_frame, text='Login', font='Arial 12 bold', fg='white', bg='#003f8a', command=self.validate_login)
        btn_login.grid(row=2, column=2, padx=10, pady=20, sticky=tk.S)
       

    #agar password and username match ho gave to admin dashboard nahi to error
    def validate_login(self):
        username = self.ent_username.get().strip()
        password = self.ent_pass.get().strip()

        if username == "" or password == "":
            messagebox.showerror("Error", "Fields cannot be empty", icon='warning')
            return

        try:
            # username and password check krne ke liye
            query = "SELECT * FROM admin WHERE username=? AND password=?"
            cur.execute(query, (username, password))
            admin = cur.fetchone()

            if admin:
                # Close login window
                self.destroy()

                # Open admin dashboard
                self.open_dashboard()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password", icon='warning')

        except Exception as e:
            messagebox.showerror("Error", f"Failed to validate login: {str(e)}", icon='warning')

    def open_dashboard(self):
        self.master.withdraw()  # Hide the login window
        from admindashboard import Main 
        root = tk.Toplevel(self.master)
        app = Main(root)  # opening admin dashboard

if __name__ == '__main__':
    root = tk.Tk()
    app = AdminLogin(root)
    root.mainloop()

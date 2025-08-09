import tkinter as tk
from tkinter import messagebox
from adminlogin import AdminLogin #to access admin login window
from studentlogin import StudentLogin  #to access student login window

class WelcomeWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management System")
        self.geometry("800x600+400+150")  
        self.resizable(False, False)
        self.configure(background='#003f8a')

        # Setting the icon 
        self.iconbitmap(r'C:\Users\Admin\Desktop\RAAM\icons\library.ico')

        self.create_widgets()

    def create_widgets(self):
        # Title Label
        lbl_title = tk.Label(self, text='Welcome to Our Library', font=('Arial', 24, 'bold'), fg='white', bg='#003f8a')
        lbl_title.pack(pady=60)

        # Frame to center buttons
        button_frame = tk.Frame(self, bg='#003f8a')
        button_frame.pack(expand=True)

        # Admin Login Button
        btn_admin = tk.Button(button_frame, text='Login as Admin', font=('Arial', 14), bg='#2488ff', fg='white', width=20, height=2, command=self.open_admin_login)
        btn_admin.pack(pady=20)

        # Student Login Button
        btn_student = tk.Button(button_frame, text='Login as Student', font=('Arial', 14), bg='#2488ff', fg='white', width=20, height=2, command=self.open_student_login)
        btn_student.pack()

        #functions for opening admin and student login page

    def open_admin_login(self):
        admin_login_window = AdminLogin(self)
        admin_login_window.grab_set()  #welcome window close krne ke liye
        self.withdraw()  

    def open_student_login(self):
        student_login_window = StudentLogin(self)
        student_login_window.grab_set()  
        self.withdraw() 

if __name__ == '__main__':
    root = WelcomeWindow()
    root.mainloop()

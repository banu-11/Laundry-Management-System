import tkinter as tk
from tkinter import messagebox
from database import get_user
from PIL import Image, ImageTk
import os

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        # Set up the canvas for the background image
        self.canvas = tk.Canvas(self, width=900, height=600)
        self.canvas.pack(fill="both", expand=True)

        self.add_background()

        # Create a styled frame for the login form
        self.login_frame = tk.Frame(self.canvas, bg="white", bd=2, relief="ridge")
        self.login_frame.configure(highlightbackground="gray", highlightthickness=1)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Add title and welcome
        tk.Label(
            self.login_frame,
            text="WELCOME TO TIP TOP LAUNDRY SERVICE",
            bg="white",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=30)

        tk.Label(
            self.login_frame,
            text="Login",
            bg="white",
            font=("Helvetica", 14, "bold")
        ).grid(row=1, column=0, columnspan=2, pady=(0, 20))

        # Username
        tk.Label(self.login_frame, text="Username", bg="white", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.username_var = tk.StringVar()
        self.username_entry = tk.Entry(self.login_frame, textvariable=self.username_var, width=30)
        self.username_entry.grid(row=2, column=1, padx=10, pady=5)

        # Password
        tk.Label(self.login_frame, text="Password", bg="white", font=("Helvetica", 12)).grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.login_frame, textvariable=self.password_var, show="*", width=30)
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)

        # Buttons
        button_style = {"font": ("Helvetica", 11, "bold"), "fg": "white", "bg": "#0073e6", "width": 12}

        self.signup_button = tk.Button(self.login_frame, text="Signup", command=lambda: self.controller.show_frame("SignupPage"), **button_style)
        self.signup_button.grid(row=4, column=0, padx=10, pady=20)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, **button_style)
        self.login_button.grid(row=4, column=1, padx=10, pady=20)

    def add_background(self):
        try:
            img_path = os.path.join(os.path.dirname(__file__), "lan1.png")
            self.original_img = Image.open(img_path)

            self.bg_image = ImageTk.PhotoImage(self.original_img.resize((900, 600)))
            self.bg_label = self.canvas.create_image(0, 0, image=self.bg_image, anchor="nw")

            # Update image on window resize
            self.controller.bind("<Configure>", self.resize_background)
        except Exception as e:
            print("Error loading background image:", e)

    def resize_background(self, event):
        if event.widget == self.controller:
            resized = self.original_img.resize((event.width, event.height), Image.BICUBIC)
            self.bg_image = ImageTk.PhotoImage(resized)
            self.canvas.itemconfig(self.bg_label, image=self.bg_image)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == "admin" and password == "admin":  # Admin credentials
            self.controller.show_frame("AdminPage")
        else:
            user = get_user(username, password)
            if user:
                self.controller.show_frame("CustomerPage")
                self.controller.frames["InfoPage"].clear_clothes()
            else:
                messagebox.showerror("Error", "Invalid credentials")
        self.clear_inputs()

    def clear_inputs(self):
        self.username_var.set("")
        self.password_var.set("")

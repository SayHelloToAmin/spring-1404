import pygame
import tkinter as tk
from tkinter import messagebox

# Dummy user credentials
VALID_USERNAME = "player1"
VALID_PASSWORD = "password123"

# Function to verify login
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == VALID_USERNAME and password == VALID_PASSWORD:
        root.destroy()  # Close Tkinter window
        start_pygame()  # Launch game window
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password")

# Function to start Pygame window
def start_pygame():
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Pygame Window")

    running = True
    while running:
        screen.fill((30, 30, 30))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()

# Tkinter GUI for login
root = tk.Tk()
root.title("Login")
root.geometry("300x200")

tk.Label(root, text="Username:").pack(pady=5)
username_entry = tk.Entry(root)
username_entry.pack(pady=5)

tk.Label(root, text="Password:").pack(pady=5)
password_entry = tk.Entry(root, show="*")  # Hide password input
password_entry.pack(pady=5)

login_button = tk.Button(root, text="Login", command=login)
login_button.pack(pady=10)

root.mainloop()

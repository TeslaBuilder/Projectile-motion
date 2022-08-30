import tkinter as tk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.state('zoomed')  # full-screen
        self.title("Projectile motion v1.0")
        self.geometry('1360x768+300+20')
        self.iconbitmap('./favicon.ico')
        self.config(bg='gray')

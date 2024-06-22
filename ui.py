import tkinter as tk

import ttkbootstrap as ttk

from typer import TypeTest


class UI:
    def __init__(self, root):
        self.window = root
        self.window.title("Typing Test")
        self.type_test = TypeTest(self.window)
        self.type_test.create_input_text()
        self.add_buttons()
        self.welcome_screen()
        self.window.mainloop()

    def add_buttons(self):
        self.restart_button = ttk.Button(
            self.window,
            text="Try Again",
            bootstyle="primary",  # type: ignore
            command=self.start_test,
        )
        self.restart_button.grid(row=0, column=0, padx=20, pady=(10, 0))

        self.exit_button = ttk.Button(
            self.window,
            text="Exit",
            bootstyle="warning-outline",  # type: ignore
            command=self.exit_game,
        )
        self.exit_button.grid(row=0, column=5, padx=20, pady=(10, 0))

    def start_test(self, first_time=False):
        if first_time:
            self.welcome.destroy()
        else:
            self.type_test.reset_vars()
        # self.restart_button.config(state=tk.DISABLED)

    def exit_game(self):
        self.window.destroy()

    def welcome_screen(self):
        self.welcome = ttk.Toplevel(self.window)
        self.welcome.title("Welcome")
        welcome_txt = (
            "Welcome to the Type Test!\n"
            "You'll have 60 seconds to type as many of the words shown.\n"
            "The countdown will start when you begin typing."
        )
        self.welcome_text = ttk.Text(
            self.welcome,
            width=50,
            height=4,
            font=("Helvetica", 18),
            wrap=tk.WORD,
            highlightthickness=0,
            bd=0,
        )
        self.welcome_text.insert(tk.END, welcome_txt)
        self.welcome_text.configure(state=tk.DISABLED)
        self.welcome_text.grid(row=1, column=1, columnspan=3, padx=20, pady=10)

        self.start_button = ttk.Button(
            self.welcome,
            text="Start",
            bootstyle="primary",  # type: ignore
            command=lambda: self.start_test(first_time=True),
        )
        self.start_button.grid(row=3, column=2, pady=(0, 20))

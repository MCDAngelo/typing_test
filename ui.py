import tkinter as tk

import ttkbootstrap as ttk

from typer import TypeTest


class UI:
    def __init__(self, root):
        self.window = root
        self.window.title("Typing Test")
        self.type_test = TypeTest(self.window)
        self.create_input_widgets()
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
        self.restart_button.grid(row=0, column=1, padx=20, pady=(10, 0))

        self.exit_button = ttk.Button(
            self.window,
            text="Exit",
            bootstyle="warning-outline",  # type: ignore
            command=self.exit_game,
        )
        self.exit_button.grid(row=0, column=2, padx=20, pady=(10, 0))

    def create_input_widgets(self):
        self.input_label = ttk.Label(
            self.window, text="Copy the text above in the space below"
        )
        self.input_label.grid(row=2, column=1, padx=20, pady=(10, 0))
        self.type_test.create_input_text()

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
        self.welcome_text = ttk.Text(self.welcome, width=80, height=10)
        self.welcome_text.insert(tk.END, "Welcome to the Type Test!")
        self.welcome_text.configure(state=tk.DISABLED)
        self.welcome_text.grid(row=1, column=1, columnspan=3, padx=20, pady=10)

        self.start_button = ttk.Button(
            self.welcome,
            text="Start",
            bootstyle="primary",  # type: ignore
            command=lambda: self.start_test(first_time=True),
        )
        self.start_button.grid(row=3, column=1)

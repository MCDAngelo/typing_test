import tkinter as tk

import ttkbootstrap as ttk

from timer import Timekeeper
from typer import TypeTest


class UI:
    def __init__(self, root):
        self.window = root
        self.window.title("Typing Test")
        self.test_texts = ["one word and another and another", "TEXT_B"]
        self.current_text = 0
        self.timekeeper = Timekeeper(self.window)
        self.timekeeper.new_timer(6)
        self.type_test = TypeTest(self.window, self.timekeeper.timer)
        self.type_test.create_original_textbox()
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
            self.current_text += 1
            self.timekeeper.timer.time = 60
            self.type_test.reset_vars(self.timekeeper.timer)
        self.refresh_text()
        self.start_timer()

    def start_timer(self):
        self.timekeeper.timer.start()
        self.window.after(1000, self.timekeeper.tick)
        self.type_test.input_text.config(state=tk.NORMAL)
        self.restart_button.config(state=tk.DISABLED)
        self.run_test()

    def run_test(self):
        if self.timekeeper.timer.running:
            self.window.after(1000, self.run_test)
        else:
            self.type_test.input_text.config(state="disabled")
            self.type_test.check_typing()
            self.restart_button.config(state=tk.NORMAL)

    def exit_game(self):
        self.window.destroy()

    def refresh_text(self):
        self.type_test.input_text.configure(state=tk.NORMAL)
        self.type_test.input_text.delete(0, tk.END)
        try:
            text = self.test_texts[self.current_text]
        except IndexError:
            print("out of range")
            text = self.test_texts[0]
            self.current_text = 0
        finally:
            self.type_test.update_original_textbox(text)

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

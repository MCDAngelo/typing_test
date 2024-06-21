import tkinter as tk

import ttkbootstrap as ttk


class TypeTest:
    def __init__(self, root, timer):
        self.window = root
        self.create_original_textbox()
        self.create_input_text()
        self.test_on = False
        self.window.bind("<Key>", self.key_handler)
        self.reset_vars(timer)

    def reset_vars(self, timer):
        self.timer = timer
        self.key_strokes = []
        self.final_input_words = []
        self.text_to_copy = []
        self.current_word_index = 0
        self.current_word = ""
        self.current_input = ""

    def create_original_textbox(self):
        self.original_textbox = ttk.Text(self.window, width=80, height=10)
        self.original_textbox.insert(tk.END, "Example text")
        self.original_textbox.configure(state=tk.DISABLED)
        self.original_textbox.grid(row=1, column=1, columnspan=3, padx=20, pady=10)

    def update_original_textbox(self, text):
        self.text_to_copy = text.split(" ")
        self.original_textbox.configure(state=tk.NORMAL)
        self.original_textbox.delete("1.0", tk.END)
        self.original_textbox.insert(tk.END, text)
        self.original_textbox.configure(state=tk.DISABLED)

    def create_input_text(self):
        self.input_text = ttk.Entry(self.window, width=30)
        self.input_text.grid(row=3, column=1, columnspan=2, padx=50, pady=(0, 10))

    def get_word_from_input(self):
        word = self.input_text.get()
        self.final_input_words.append(word)
        self.input_text.delete(0, tk.END)

    def key_handler(self, event):
        if self.timer.running:
            # TODO:
            # if the input_text mismatches the current word they are meant to type
            # font of word should be red, otherwise, black
            self.key_strokes.append(event.char)
            if event.keysym == "space":
                self.get_word_from_input()

    def check_typing(self):
        self.get_word_from_input()
        self.total_characters = len(self.key_strokes)
        self.correct_words = []
        for example_word, input_word in zip(self.text_to_copy, self.final_input_words):
            if example_word.lower().strip() == input_word.lower().strip():
                self.correct_words.append(example_word.strip())
        self.total_correct_words = len(self.correct_words)
        # TODO:
        # Calculate wpm, cwpm, kpm etc and surface in a message box or score area in UI
        print(
            f"You typed {self.total_correct_words} /{len(self.text_to_copy)} words correctly"
        )
        print(f"You typed {self.final_input_words} words in total")
        print(f"You typed {self.total_characters} characters in total")

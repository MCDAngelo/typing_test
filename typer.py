import tkinter as tk
from tkinter import messagebox

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
        self.total_words = len(self.final_input_words)
        self.correct_words = []
        for example_word, input_word in zip(self.text_to_copy, self.final_input_words):
            if example_word.lower().strip() == input_word.lower().strip():
                self.correct_words.append(example_word.strip())
        self.total_correct_words = len(self.correct_words)
        self.wpm = self.total_words / self.timer.original_time
        self.kpm = self.total_characters / self.timer.original_time
        self.cwpm = self.total_correct_words / self.timer.original_time
        self.accuracy = self.total_correct_words / len(self.text_to_copy)
        self.show_scores()

    def show_scores(self):
        score_msg = (
            f"Total words: {self.total_words} - Accuracy: {self.accuracy*100:.0f}%\n"
            f"WPM: {self.wpm:.2f} - CWPM: {self.cwpm:.2f}\n"
            f"Total keystrokes: {self.total_characters} - KPM: {self.kpm:.2f}"
        )
        self.score_messagebox = messagebox.showinfo("Final Score", score_msg)

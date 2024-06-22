import tkinter as tk
from functools import reduce
from tkinter import messagebox

import ttkbootstrap as ttk

from paragraphs import generate_random_paragraph
from timer import Timekeeper


class TypeTest:
    def __init__(self, root):
        self.window = root
        self.test_duration = 60
        self.timekeeper = Timekeeper(self.window)
        self.create_original_textbox()
        self.create_input_text()
        self.window.bind("<Key>", self.key_handler)
        self.reset_vars()

    def reset_vars(self):
        if self.timekeeper.timer:
            self.timekeeper.timer.stop()
            self.timekeeper = Timekeeper(self.window)
        self.timekeeper.new_timer(self.test_duration, column=2)
        self.timekeeper.timer.config(font=("Helvetica", 36))
        self.key_strokes = []
        self.final_input_words = []
        self.incorrect_words = []
        self.text_to_copy = generate_random_paragraph()
        self.current_word_index = 0
        self.current_char_index = 0
        self.current_word = ""
        self.highlighted_word = ""
        self.highlighted_start = "1.0"
        self.highlighted_end = "1.0"
        self.current_word_spellcheck_status = None
        self.spell_check_start = "1.0"
        self.spell_check_end = "1.0"
        self.update_original_textbox()
        self.input_text.config(state=tk.NORMAL)
        self.input_text.delete(0, tk.END)

    def start_test(self):
        self.timekeeper.timer.start()
        self.window.after(1000, self.timekeeper.tick)
        self.run_test()

    def run_test(self):
        if self.timekeeper.timer.running:
            self.window.after(1000, self.run_test)
        else:
            if self.timekeeper.timer.time == 0:
                self.input_text.config(state="disabled")
                self.spellcheck_current_input()
                self.get_word_from_input()
                self.check_typing()
            else:
                return

    def create_input_text(self):
        self.input_text = ttk.Entry(self.window, width=20, font=("", 22))
        self.input_text.insert(0, "Start typing here ...")
        self.input_text.bind(
            "<FocusIn>", lambda args: self.input_text.delete("0", "end")
        )
        self.input_text.grid(row=3, column=1, columnspan=6, padx=50, pady=(0, 30))

    def create_original_textbox(self):
        self.original_textbox = ttk.Text(
            self.window, width=50, height=10, wrap=tk.WORD, font=("Helvetica", 32)
        )
        self.original_textbox.insert(tk.END, "Example text")
        self.original_textbox.configure(state=tk.DISABLED)
        self.original_textbox.grid(row=1, column=1, columnspan=3, padx=80, pady=30)
        self.original_textbox.tag_configure("highlight", background="skyblue")
        self.original_textbox.tag_configure("correct_word", foreground="blue")
        self.original_textbox.tag_configure("correct_input", foreground="white")
        self.original_textbox.tag_configure("incorrect_input", foreground="red")

    def update_original_textbox(self):
        self.words_to_copy = self.text_to_copy.split(" ")
        self.original_textbox.configure(state=tk.NORMAL)
        self.original_textbox.delete("1.0", tk.END)
        self.original_textbox.insert(tk.END, self.text_to_copy)
        self.original_textbox.configure(state=tk.DISABLED)
        self.current_word = self.words_to_copy[self.current_word_index]
        self.highlight_current_word()

    def get_word_from_input(self):
        word = self.input_text.get()
        self.final_input_words.append(word)
        self.input_text.delete(0, tk.END)

    def highlight_current_word(self):
        if self.highlighted_word != self.current_word:
            self.original_textbox.tag_remove(
                "highlight", self.highlighted_start, self.highlighted_end
            )
            self.current_end_index = self.current_char_index + len(self.current_word)
            start = f"1.{self.current_char_index}"
            end = f"1.{self.current_end_index}"
            self.original_textbox.tag_add("highlight", start, end)
            self.highlighted_word = self.current_word
            self.highlighted_start = start
            self.highlighted_end = end

    def spellcheck_current_input(self):
        current_input_char_index = len(self.input_text.get())
        partial_original = self.current_word[:current_input_char_index]
        current_input_end_index = min(
            (self.current_char_index + current_input_char_index),
            self.current_end_index,
        )
        start = f"1.{self.current_char_index}"
        end = f"1.{current_input_end_index}"
        spell_check_status = partial_original == self.input_text.get()
        if (self.spell_check_start == self.highlighted_start) & (
            spell_check_status != self.current_word_spellcheck_status
        ):
            if spell_check_status:
                self.original_textbox.tag_remove(
                    "incorrect_input", self.spell_check_start, self.spell_check_end
                )
            else:
                self.original_textbox.tag_remove(
                    "correct_input", self.spell_check_start, self.spell_check_end
                )
        if spell_check_status:
            self.original_textbox.tag_add("correct_input", start, end)
        else:
            self.original_textbox.tag_add("incorrect_input", start, end)
        self.spell_check_start = start
        self.spell_check_end = end
        self.current_word_spellcheck_status = spell_check_status

    def format_final_word(self):
        if self.current_word_spellcheck_status:
            self.original_textbox.tag_remove(
                "correct_input", self.highlighted_start, self.highlighted_end
            )
            self.original_textbox.tag_remove(
                "incorrect_input", self.highlighted_start, self.highlighted_end
            )
            self.original_textbox.tag_add(
                "correct_word", self.highlighted_start, self.highlighted_end
            )
        else:
            self.incorrect_words.append(self.input_text.get())
            self.original_textbox.tag_remove(
                "correct_input", self.highlighted_start, self.highlighted_end
            )
            self.original_textbox.tag_add(
                "incorrect_input", self.highlighted_start, self.highlighted_end
            )

    def key_handler(self, event):
        if len(self.key_strokes) == 0:
            self.start_test()
        if self.timekeeper.timer.running:
            self.highlight_current_word()
            self.key_strokes.append(event.char)
            if event.keysym == "space":
                self.format_final_word()
                self.current_word_index += 1
                self.current_word_spellcheck_status = None
                try:
                    self.current_word = self.words_to_copy[self.current_word_index]
                except IndexError:
                    return
                self.current_char_index = self.current_end_index + 1
                self.get_word_from_input()
            else:
                self.spellcheck_current_input()

    def check_typing(self):
        self.total_characters = len(self.key_strokes)
        self.total_words = len(self.final_input_words)
        self.correct_words = []
        for example_word, input_word in zip(self.words_to_copy, self.final_input_words):
            if example_word.lower().strip() == input_word.lower().strip():
                self.correct_words.append(example_word.strip())
        self.total_correct_words = len(self.correct_words)
        if len(self.incorrect_words) == 0:
            incorrect_chars = 0
        else:
            incorrect_chars = reduce(
                lambda x, y: x + y, map(lambda x: len(x), self.incorrect_words)
            )

        self.raw_cpm = self.total_characters / (self.test_duration // 60)
        self.corrected_cpm = (self.total_characters - incorrect_chars) / (
            self.test_duration // 60
        )
        self.wpm = self.corrected_cpm / 5
        self.show_scores()

    def show_scores(self):
        score_msg = (
            f"Corrected wpm: {self.wpm:.2f}\n"
            f"Corrected cpm: {self.corrected_cpm:.2f}\n"
            f"Raw cpm: {self.raw_cpm:.2f}\n"
        )
        self.score_messagebox = messagebox.showinfo("Final Score", score_msg)

import ttkbootstrap as ttk


class Timer(ttk.Label):
    def __init__(self, parent, seconds):
        super().__init__(parent)
        self.original_time = seconds
        self.time = seconds
        self.running = False
        self.show_time()

    def show_time(self):
        self.config(text=f"{self.time:02}")

    def tick(self):
        self.time -= 1
        if self.time >= 0:
            self.show_time()
        if self.time < 0:
            self.running = False

    def start(self):
        self.running = True

    def stop(self):
        self.running = False


class Timekeeper:
    def __init__(self, window):
        self.window = window
        self.timer = None

    def new_timer(self, seconds, row=0, column=0):
        self.timer = Timer(self.window, seconds)
        self.timer.grid(row=row, column=column, padx=20, pady=(10, 0))

    def tick(self):
        self.window.after(1000, self.tick)
        if (self.timer is not None) and (self.timer.running):
            self.timer.tick()

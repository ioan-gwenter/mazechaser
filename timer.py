import threading
import time


class Timer:
    def __init__(self):
        self.timer_val = 0
        self.timer_running = False
        self.start_time = 0
        self.end_time = time.time()
        self.start_clock()

    def start_clock(self):
        self.timer_val = 0
        self.timer_running = True
        self.start_time += time.time()

    def stop_clock(self):
        self.timer_running = False

    def get_time(self):
        """
        converts time in tenths of seconds into formatted string A:BC.D
        """

        total_secs = self.timer_val
        minute = round(total_secs / 60)
        seconds = round(total_secs % 60)
        miliseconds = round((total_secs % 1)*100)
        s = f"{minute:02d}:{seconds:02d}:{miliseconds:02d}"


        return s

    def count(self):
        if self.timer_running:
            self.end_time = time.time()
            elapsed_time = self.end_time - self.start_time
            self.timer_val += elapsed_time
            self.start_time = time.time()

import tkinter as tk
from src.movie_ticket import choose_theater_window


class MovieTicketBooking(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Mozi program kereső')
        self.geometry('300x500')
        self._current_window = choose_theater_window.ChooseTheaterWindow(self)

    @property
    def current_window(self):
        return self._current_window

    @current_window.setter
    def current_window(self, new_window):
        self._current_window = new_window

    def run(self):
        self.mainloop()

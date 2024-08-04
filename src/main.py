"""Module providing a function loading json files."""
import json
import tkinter as tk

from src.movie_ticket import movie_ticket_booking
from src.watchlist import movies_from_watchlist

with open('src/movie_ticket/utils/movies_data.json', 'r') as f:
    watchlist_data = json.load(f)


class StartWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Kezdőablak')
        self.geometry('300x200')

        tk.Label(self, text="Válasszon egy lehetőséget:").pack()

        self.choice = tk.IntVar(value=1)

        tk.Radiobutton(self, text="Mozi program kereső", variable=self.choice, value=1).pack()
        tk.Radiobutton(self, text="Watchlist", variable=self.choice, value=2).pack()

        tk.Button(self, text="OK", command=self.on_ok).pack()

    def on_ok(self):
        if self.choice.get() == 1:
            self.destroy()
            app = movie_ticket_booking.MovieTicketBooking()
            app.run()
        elif self.choice.get() == 2:
            self.destroy()
            watchlist_app = movies_from_watchlist.MoviesFromWatchList(watchlist_data)
            watchlist_app.mainloop()


if __name__ == "__main__":
    start_window = StartWindow()
    start_window.mainloop()

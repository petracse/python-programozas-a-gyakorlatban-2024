from datetime import datetime
from tkinter import ttk
from tkcalendar import Calendar
from src.movie_ticket import choose_movie_window
from src.movie_ticket import choose_theater_window


class ChooseDateWindow:
    def __init__(self, parent, external_code):

        self.external_code = external_code

        self.parent = parent
        self.label = ttk.Label(parent, text="Válassz dátumot!")
        self.label.pack()

        current_date = datetime.now()
        self.cal = Calendar(parent, mindate=current_date,
                            selectmode='day', year=current_date.year,
                            month=current_date.month,
                            day=current_date.day, date_pattern='y-mm-dd')

        self.cal.pack()

        self.ok_button = ttk.Button(parent, text="OK", command=self.on_ok_button_click)
        self.ok_button.pack()

        self.cancel_button = ttk.Button(parent, text="Cancel", command=self.on_cancel_button_click)
        self.cancel_button.pack()

    def on_ok_button_click(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.parent.current_window = choose_movie_window.ChooseMovieWindow(self.parent, self.external_code,
                                                                           self.cal.get_date())

    def on_cancel_button_click(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parent.current_window = choose_theater_window.ChooseTheaterWindow(self.parent)

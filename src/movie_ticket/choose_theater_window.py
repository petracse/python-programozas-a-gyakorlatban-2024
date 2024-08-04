import tkinter as tk
from tkinter import ttk
from src.movie_ticket import choose_date_window
from src.movie_ticket.utils import movie_theaters_load


class ChooseTheaterWindow:
    def __init__(self, parent):

        self.parent = parent

        self.label = ttk.Label(parent, text='Válassz mozit!')
        self.label.pack()

        self.movie_theaters = movie_theaters_load.load_data()

        self.selected_cinema_name = tk.StringVar()
        self.dropdown = ttk.Combobox(parent, textvariable=self.selected_cinema_name, state="readonly")
        self.dropdown['values'] = [cinema['name'] for cinema in self.movie_theaters]
        self.dropdown.pack()

        self.selected_cinema_name.set(self.movie_theaters[0]['name'])
        self.selected_cinema_address = self.movie_theaters[0]['address']['address1']
        self.selected_cinema_external_code = self.movie_theaters[0]['externalCode']
        self.addressLabel = ttk.Label(parent, text="A mozi címe: " + self.selected_cinema_address)
        self.addressLabel.pack()

        self.dropdown.bind("<<ComboboxSelected>>", self.on_select)

        self.ok_button = ttk.Button(parent, text="OK", command=self.on_ok_button_click)
        self.ok_button.pack()

    def on_select(self, _event):
        selected_cinema_name = self.selected_cinema_name.get()
        selected_cinema = next(
            (cinema for cinema in self.movie_theaters if cinema['name'] == selected_cinema_name), None)
        if selected_cinema:
            self.addressLabel.config(text="A mozi címe: " + selected_cinema["address"]["address1"])
            self.selected_cinema_external_code = selected_cinema["externalCode"]

    def on_ok_button_click(self):
        for widget in self.parent.winfo_children():
            widget.destroy()

        self.parent.current_window = choose_date_window.ChooseDateWindow(self.parent, self.selected_cinema_external_code)

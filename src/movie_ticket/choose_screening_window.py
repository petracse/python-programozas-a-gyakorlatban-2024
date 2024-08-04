import webbrowser
from tkinter import ttk, Listbox
from src.movie_ticket import choose_movie_window


class ChooseScreeningWindow:
    def __init__(self, parent, external_code, movies_data, selected_index):
        self.external_code = external_code
        self.movies_data = movies_data
        self.parent = parent
        self.screenings_data = movies_data[selected_index]['screening-attributes']

        self.screening_listbox = Listbox(self.parent, width=250)
        for key in self.screenings_data:
            (self.screening_listbox.
             insert("end", self.screenings_data[key]
                    .text.strip() + " (" + self.screenings_data[key]['data-attrs'] + ")"))
        self.screening_listbox.pack()

        self.ok_button = ttk.Button(self.parent, text="OK", command=self.on_ok_button_click)
        self.ok_button.pack()
        self.cancel_button = ttk.Button(self.parent, text="Cancel", command=self.on_cancel_button_click)
        self.cancel_button.pack()

    def on_ok_button_click(self):
        selected_index = self.screening_listbox.curselection()
        if selected_index:
            webbrowser.open_new_tab(self.screenings_data[selected_index[0]]['data-url'])

    def on_cancel_button_click(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parent.current_window = choose_movie_window.ChooseMovieWindow(
            self.parent, self.external_code, None, self.movies_data)

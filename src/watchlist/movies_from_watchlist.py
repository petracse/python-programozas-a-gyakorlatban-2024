import tkinter as tk
from tkinter import ttk
import json


class MoviesFromWatchList(tk.Tk):
    def __init__(self, watchlist_data):
        super().__init__()
        self.title('Watchlist Movies')
        self.geometry('800x400')

        self.watchlist_data = watchlist_data

        self.tree = ttk.Treeview(self)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.tree["columns"] = ("length", "releaseYear")

        self.tree.heading("#0", text="Movie Name")
        self.tree.heading("length", text="Length", command=lambda: self.sort_column("length", False))
        self.tree.heading("releaseYear", text="Release Year", command=lambda: self.sort_column("releaseYear", False))

        self.populate_tree()

        search_label = tk.Label(self, text="Címkeresés")
        search_label.pack(side=tk.TOP, fill=tk.X, padx=250)

        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self, textvariable=self.search_var)
        search_entry.pack(side=tk.TOP, fill=tk.X, padx=250)
        search_entry.bind('<KeyRelease>', self.search)

        delete_button = tk.Button(self, text="Törlés", command=self.delete_movie)
        delete_button.pack(side=tk.BOTTOM, padx=10, pady=10)

    def populate_tree(self):
        for movie_id, movie_info in self.watchlist_data.items():
            movie_name = movie_info['name']
            movie_length = movie_info['length']
            movie_release_year = movie_info['releaseYear']
            self.tree.insert("", tk.END, text=movie_name, values=(movie_length, movie_release_year))

    def sort_column(self, col, reverse):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_column(col, not reverse))

    def search(self, _event):
        search_term = self.search_var.get()
        if not search_term:
            self.tree.selection_remove(self.tree.selection())
            return
        for item in self.tree.get_children():
            if search_term.lower() in self.tree.item(item, "text").lower():
                self.tree.selection_set(item)
                self.tree.focus(item)
            else:
                self.tree.selection_remove(item)

    def delete_movie(self):
        selected_items = self.tree.selection()
        if selected_items:
            for selected_item in selected_items:
                movie_name = self.tree.item(selected_item)['text']
                for movie_id, movie_info in self.watchlist_data.items():
                    if movie_info['name'] == movie_name:
                        del self.watchlist_data[movie_id]
                        break
                with open('src/movie_ticket/utils/movies_data.json', 'w') as f:
                    json.dump(self.watchlist_data, f)
                self.tree.delete(selected_item)


with open('src/movie_ticket/utils/movies_data.json', 'r') as f:
    watchlist_data = json.load(f)

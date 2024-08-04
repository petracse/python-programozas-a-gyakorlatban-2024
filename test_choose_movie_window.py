import unittest
from tkinter import Tk, ttk, Listbox
from src.movie_ticket.choose_movie_window import ChooseMovieWindow


class TestChooseMovieWindow(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.window = ChooseMovieWindow(self.root, external_code="12345", date="2024-05-12", movie_data={
            0: {'name': 'Movie 1', 'for-movie': '1', 'screening-attributes': {0: 'Screening 1', 1: 'Screening 2'}},
            1: {'name': 'Movie 2', 'for-movie': '2', 'screening-attributes': {0: 'Screening 3'}}
        })

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertIsInstance(self.window.welcome_label, ttk.Label)
        self.assertIsInstance(self.window.movie_listbox, Listbox)
        self.assertIsInstance(self.window.submit_button, ttk.Button)
        self.assertIsInstance(self.window.save_to_watchlist_button, ttk.Button)
        self.assertIsInstance(self.window.delete_from_watchlist_button, ttk.Button)
        self.assertIsInstance(self.window.cancel_button, ttk.Button)
        self.assertIsInstance(self.window.message_label, ttk.Label)


if __name__ == "__main__":
    unittest.main()

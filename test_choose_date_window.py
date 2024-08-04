import unittest
from unittest.mock import MagicMock
from tkinter import Tk, ttk
from tkcalendar import Calendar
from src.movie_ticket import choose_movie_window, choose_theater_window
from src.movie_ticket.choose_date_window import ChooseDateWindow


class TestChooseDateWindow(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.window = ChooseDateWindow(self.root, external_code="12345")

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertIsInstance(self.window.label, ttk.Label)
        self.assertIsInstance(self.window.cal, Calendar)
        self.assertIsInstance(self.window.ok_button, ttk.Button)
        self.assertIsInstance(self.window.cancel_button, ttk.Button)

    def test_on_ok_button_click(self):
        self.window.cal.get_date = MagicMock(return_value="2024-05-12")
        self.window.parent.current_window = None
        self.window.on_ok_button_click()
        self.assertIsInstance(self.window.parent.current_window, choose_movie_window.ChooseMovieWindow)

    def test_on_cancel_button_click(self):
        self.window.parent.current_window = None
        self.window.on_cancel_button_click()
        self.assertIsInstance(self.window.parent.current_window, choose_theater_window.ChooseTheaterWindow)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import MagicMock
from tkinter import Tk, ttk
from src.movie_ticket.choose_theater_window import ChooseTheaterWindow


class TestChooseTheaterWindow(unittest.TestCase):

    def setUp(self):
        self.root = Tk()
        self.window = ChooseTheaterWindow(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_initialization(self):
        self.assertIsInstance(self.window.label, ttk.Label)
        self.assertIsInstance(self.window.dropdown, ttk.Combobox)
        self.assertIsInstance(self.window.ok_button, ttk.Button)
        self.assertEqual(len(self.window.movie_theaters), 18)

    def test_on_select(self):
        self.window.selected_cinema_name.set("Allee - Budapest")
        self.window.on_select(None)
        self.assertEqual(self.window.selected_cinema_external_code, "1133")

    def test_on_ok_button_click(self):
        self.root.winfo_children = MagicMock(return_value=[MagicMock()])

        choose_date_window_mock = MagicMock()
        choose_date_window_mock.return_value = MagicMock()
        with unittest.mock.patch("src.movie_ticket.choose_date_window.ChooseDateWindow", choose_date_window_mock):
            self.window.on_ok_button_click()

        choose_date_window_mock.assert_called_once_with(self.root, self.window.selected_cinema_external_code)


if __name__ == "__main__":
    unittest.main()

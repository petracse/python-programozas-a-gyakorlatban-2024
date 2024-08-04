import unittest
from tkinter import Tk
from src.watchlist.movies_from_watchlist import MoviesFromWatchList


class TestMoviesFromWatchList(unittest.TestCase):
    def setUp(self):
        self.watchlist_data = {
            "6161d2r": {
                "name": "Imádlak utálni",
                "length": 104,
                "releaseYear": "2023"
            }
        }
        self.app = MoviesFromWatchList(self.watchlist_data)

    def test_initialization(self):
        self.assertIsInstance(self.app, Tk)
        self.assertEqual(self.app.title(), 'Watchlist Movies')
        self.assertIsNotNone(self.app)


if __name__ == '__main__':
    unittest.main()

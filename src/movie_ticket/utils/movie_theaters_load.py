import json
import os
from src.movie_ticket.utils.movie_theaters_parse import movie_theaters_parse


def load_data():
    data_file = 'src/movie_ticket/utils/cinemas_data.json'
    if os.path.exists(data_file):
        with open(data_file, 'r') as f:
            data = json.load(f)
    else:
        movie_theaters_parse()
        with open(data_file, 'r') as f:
            data = json.load(f)

    return data

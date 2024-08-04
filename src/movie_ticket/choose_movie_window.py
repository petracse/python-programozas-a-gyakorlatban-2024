import json
import os
from datetime import datetime, timedelta
from tkinter import ttk, Listbox
from bs4 import BeautifulSoup
from selenium import webdriver
import threading
from src.movie_ticket import choose_date_window
from src.movie_ticket.utils import movie_title_support
from src.movie_ticket.utils import movie_details_parse
from src.movie_ticket import choose_screening_window


class ChooseMovieWindow:
    def __init__(self, parent, external_code, date, movie_data=None):
        self.message_label = None
        self.delete_from_watchlist_button = None
        self.save_to_watchlist_button = None
        self.submit_button = None
        self.movie_listbox = None
        self.welcome_label = None
        self.cancel_button = None
        self.not_found = None

        self.external_code = external_code
        self.parent = parent

        self.movies_data = movie_data if movie_data else {}
        if movie_data:

            self.show_movie_list()
        else:
            self.spinner = ttk.Label(parent, text="Loading...")
            self.spinner.pack()
            self.initialize_choose_movie_window(date)

    def initialize_choose_movie_window(self, date):
        init_thread = threading.Thread(target=self.initialize_selenium, args=(date,))
        init_thread.start()

    def initialize_selenium(self, date):
        try:
            original_url = (f"https://www.cinemacity.hu/#/buy-tickets-by-cinema"
                            f"?in-cinema={self.external_code}&at={date}&view-mode=list")
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--headless")
            driver = webdriver.Chrome(options=chrome_options)
            driver.get(original_url)
            new_url = driver.current_url
            if new_url != original_url:
                self.show_error_message("Erre a napra még nincs műsor.\nJavasolt tartomány:\n"
                                        + datetime.now().strftime('%Y-%m-%d') + " - " +
                                        (datetime.now() + timedelta(days=4)).strftime('%Y-%m-%d'))
            else:
                self.show_movie_list(driver.page_source)

        except Exception as e:
            print("Error occurred:", e)

        finally:
            self.spinner.destroy()

    def show_error_message(self, message):
        self.not_found = ttk.Label(self.parent, text=message)
        self.not_found.pack()
        self.cancel_button = ttk.Button(self.parent, text="Cancel", command=self.on_cancel_button_click)
        self.cancel_button.pack()
        self.message_label.pack()

    def show_movie_list(self, page_source=None):
        self.welcome_label = ttk.Label(self.parent, text="Válassz filmet!")
        self.welcome_label.pack()
        if not self.movies_data:
            self.parse_movie_data(page_source)
        self.movie_listbox = Listbox(self.parent)
        for key in self.movies_data:
            self.movie_listbox.insert("end", self.movies_data[key]['name'])
        self.movie_listbox.pack()
        self.submit_button = ttk.Button(self.parent, text="Submit", command=self.on_submit_button_click)
        self.submit_button.pack()
        self.save_to_watchlist_button = ttk.Button(
            self.parent, text="To Watchlist", command=self.on_save_to_watchlist)
        self.save_to_watchlist_button.pack()
        self.delete_from_watchlist_button = ttk.Button(
            self.parent, text="Remove From Watchlist", command=self.on_delete_from_watchlist)
        self.delete_from_watchlist_button.pack()
        self.cancel_button = ttk.Button(self.parent, text="Cancel", command=self.on_cancel_button_click)
        self.cancel_button.pack()
        self.message_label = ttk.Label(self.parent, text="")
        self.message_label.pack()

    def parse_movie_data(self, page_source):
        soup = BeautifulSoup(page_source, "html.parser")
        i = 0
        qb_movie_details_divs = soup.find_all("div", class_="qb-movie-details")
        for div in qb_movie_details_divs:
            a_tag = div.find(
                lambda tag:
                tag.name == 'a' and tag.get('class') == ['qb-movie-link']
                and not tag.parent.find_next_sibling("div").find("h4"))
            if a_tag:
                screening_links_bs4 = (div.find_all
                                       (lambda tag: tag.name == "a" and tag.parent.name == "div"
                                        and tag.parent.get('class') == ['qb-movie-info-column']))
                for_movie = a_tag['href'].split('for-movie=')[1].split('&')[0]
                self.movies_data[i] = {}
                self.movies_data[i]['for-movie'] = for_movie
                self.movies_data[i]['name'] = a_tag.text.strip()
                self.movies_data[i]['screening-attributes'] = {}
                for j in range(len(screening_links_bs4)):
                    self.movies_data[i]['screening-attributes'][j] = screening_links_bs4[j]
                i += 1

    def on_save_to_watchlist(self):
        selected_index = self.movie_listbox.curselection()
        if selected_index:
            movie_name = self.movies_data[selected_index[0]]['name']
            for_movie = self.movies_data[selected_index[0]]['for-movie']
            try:
                if os.path.exists("src/movie_ticket/utils/movies_data.json"):
                    with open("src/movie_ticket/utils/movies_data.json", "r") as file:
                        data = json.load(file)
                else:
                    data = {}

                data[for_movie] = {}
                slug = movie_title_support.convert_to_slug(movie_name)
                data[for_movie]['slug'] = slug
                details_parse = movie_details_parse.movie_details_parse(for_movie, slug)
                for key in details_parse:
                    data[for_movie][key] = details_parse[key]

                with open("src/movie_ticket/utils/movies_data.json", "w") as file:
                    json.dump(data, file)
                self.message_label.config(text="Successfully added to your watchlist!")
            except Exception as e:
                print("Error occurred while saving to watchlist:", e)
        else:
            print("No movie selected.")
        self.movie_listbox.bind("<<ListboxSelect>>", self.update_message_label_visibility)

    def on_delete_from_watchlist(self):
        selected_index = self.movie_listbox.curselection()
        if selected_index:
            for_movie = self.movies_data[selected_index[0]]['for-movie']
            try:
                if os.path.exists("src/movie_ticket/utils/movies_data.json"):
                    with open("src/movie_ticket/utils/movies_data.json", "r") as file:
                        data = json.load(file)
                    if for_movie in data:
                        del data[for_movie]
                        with open("src/movie_ticket/utils/movies_data.json", "w") as file:
                            json.dump(data, file)
                        self.message_label.config(text="Deleted")
                    else:
                        print("Data not found in watchlist.")
                else:
                    print("Watchlist file not found.")
            except Exception as e:
                print("Error occurred while deleting from watchlist:", e)
        else:
            print("No movie selected.")
        self.movie_listbox.bind("<<ListboxSelect>>", self.update_message_label_visibility)

    def update_message_label_visibility(self, _event):
        self.message_label.config(text="")

    def on_submit_button_click(self):
        selected_index = self.movie_listbox.curselection()
        if selected_index:
            for widget in self.parent.winfo_children():
                widget.destroy()
            self.parent.current_window = choose_screening_window.ChooseScreeningWindow(
                self.parent, self.external_code, self.movies_data, selected_index[0])
        else:
            print("No movie selected.")

    def on_cancel_button_click(self):
        for widget in self.parent.winfo_children():
            widget.destroy()
        self.parent.current_window = choose_date_window.ChooseDateWindow(self.parent, self.external_code)

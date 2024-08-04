import requests
import re
import json


def movie_details_parse(key, slug):
    url = f"https://www.cinemacity.hu/films/{slug}/{key}#/"

    try:
        response = requests.get(url)
        source_code = response.text
        pattern = r'var\s+filmDetails\s*=\s*({.*?});'
        match = re.search(pattern, source_code)
        if match:
            film_details_string = match.group(1)
            film_details_dict = json.loads(film_details_string)

            filtered_details = {}
            for key in ["name", "originalName", "length", "releaseYear", "originalLanguage", "releaseCountry",
                        "directors", "cast", "synopsis", "categoriesAttributes", "ageRestrictionName"]:
                if key in film_details_dict:
                    filtered_details[key] = film_details_dict[key]
                else:
                    filtered_details[key] = None

            return filtered_details
        else:
            print("Nem sikerült megtalálni a film részleteit.")
            return None

    except Exception as e:
        print("Hiba történt a film részleteinek lekérése közben:", e)
        return None

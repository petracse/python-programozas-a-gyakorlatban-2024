import requests


def movie_theaters_parse():
    r = requests.get("https://www.cinemacity.hu/")
    lines = r.text.split('\n')
    apiSitesList = ""
    for line in lines:
        if line.strip().startswith("apiSitesList"):
            apiSitesList = line
            break
    start_index = apiSitesList.find("[")
    end_index = apiSitesList.find("]")
    apiSitesList = "[" + apiSitesList[start_index + 1:end_index] + "]"

    file_path = "src/movie_ticket/utils/cinemas_data.json"

    with open(file_path, "w") as my_file:
        my_file.write(apiSitesList)

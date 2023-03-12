import requests
from bs4 import BeautifulSoup
import json

URL = 'https://myanimelist.net/topanime.php'

page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')

anime_links = soup.select('div.di-ib > h3 > a')
rating = soup.select('td.score > div > span')
info = soup.select('div.information')

titles = [tag.text for tag in anime_links]
ratings = [float(tag.text) for tag in rating]
type = [tag.text.split(' (')[0][9:] for tag in info]
episodes = [tag.text.split(' (')[1].split(' eps')[0] for tag in info]
airing = [tag.text.split(')')[1][9:].split('\n')[0] for tag in info]
urls = [f'https://myanimelist.net{tag["href"]}' for tag in anime_links]

with open("anime.json", "w", encoding='utf-8') as file:
    file.write('[')
    for i in range(0,50):
        row = f'"title": "{titles[i]}", "rating": {ratings[i]}, "type": "{type[i]}", "episodes": {episodes[i]}, "airing": "{airing[i]}", "url": "{urls[i]}"'
        if i == 49:
            row = '{' + row + '} '
        else:
            row = '{' + row + '}, \n'
        print(row)
        file.write(row)
    file.write(']')
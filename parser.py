import requests
import random
import json
from bs4 import BeautifulSoup as bs
import datetime


# парсинг фильмов
date = datetime.datetime.today()
year = date.strftime("%Y")
month = date.strftime("%B").upper()

def parse_films(url='https://kinopoiskapiunofficial.tech/api/v2.2/films/premieres'):
    data = {"year": year, "month": month}   # дынные запроса
    headers = { # служебная информация запроса
        'X-API-KEY': '68f00780-c5bf-4776-b5fa-07ee77223501',    # мой токен
        'Content-Type': 'application/json',
    }
    r = requests.get(url, params=data, headers=headers)     # Response()
    if r:
        datafile = r.json()
        films = datafile['items']
        chosen_film = random.choice(films)
        text_to_return = f"""{chosen_film['nameRu']}. {chosen_film['year']} год.
            Жанры: {', '.join([i['genre'] for i in chosen_film['genres']])}"""
        return text_to_return   # Возвращаю описание фильма


# получаем html-код главной странцы Steam
def parse_games(url='https://store.steampowered.com/?l=russian') -> str:
    global genres, genres_list
    response = requests.get(url)
    if response:
        src = bs(response.content, features='lxml')
        genres = src.find_all('div', class_="popup_menu_subheader popup_genre_expand_header responsive_hidden")
        genres_list = [i.get_text().strip() for i in genres]
        genre_number = random.randint(0, len(genres_list) - 1)
        # функция принимает hmtl-код жанров и превращает его в список из ссылок,
        # переходит на ссылку страницы жанра и ищет там блок данных, из которого выбирает названия игр,
        # и возвращает случайно выбранное название пользоваелю  (использованы random и json)
        genre_link = genres[genre_number].find('a', class_='popup_menu_item')['href']
        genre_response = requests.get(genre_link)
        src = bs(genre_response.content, features='lxml') if genre_response else None
        find_json_tag = src.find('div', id='application_config')['data-ch_broadcasts_data_6']
        finding_dict_list_of_games = json.loads(find_json_tag)['filtered']
        games = list(map(
            lambda x: x['app_name'], finding_dict_list_of_games
        ))
        answer = f"""Советую поиграть в {random.choice(games)},
            она как раз в жанре {genres_list[genre_number - 1]}"""
        return answer




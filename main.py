import time
import requests
import csv
from collections import defaultdict
from typing import Iterator

CATEGORY_TITLE = "Категория:Животные_по_алфавиту"
API_URL = "http://ru.wikipedia.org/w/api.php"
DELAY = 0.3
RUSSIAN_LETTERS = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ')

def fetch_animals_from_wikipedia() -> Iterator[str]:
    """Получает названия страниц из категории 'Животные по алфавиту' на Википедии."""
    params = {
        'action': 'query',
        'format': 'json',
        'list': 'categorymembers',
        'cmtitle': CATEGORY_TITLE,
        'cmlimit': 'max',
        'cmnamespace': '0'
    }
    while True:
        try:
            response = requests.get(API_URL, params=params)
            data = response.json()
        except requests.RequestException as e:
            print(f"Ошибка при запросе: {e}")

        for page in data['query']['categorymembers']:
            yield page['title']

        if 'continue' in data:
            params.update(data['continue'])
        else:
            break
        time.sleep(DELAY)

def count_animals_by_letter(titles: Iterator[str]) -> list[tuple[str, int]]:
    animal_counts = defaultdict(int)
    for title in titles:
        first_char = title[0].upper()
        if first_char in RUSSIAN_LETTERS:
            animal_counts[first_char] += 1

    return sorted(animal_counts.items())

def save_counts_to_csv(counts:list[tuple[str, int]], filename='beasts.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for letter, count in counts:
            writer.writerow([letter, count])

if __name__ == '__main__':
    counts = count_animals_by_letter(fetch_animals_from_wikipedia())
    save_counts_to_csv(counts)


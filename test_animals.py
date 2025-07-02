from main import count_animals_by_letter, fetch_animals_from_wikipedia, save_counts_to_csv
import unittest
from unittest.mock import patch
import tempfile
import csv
import os

class TestCountAnimals(unittest.TestCase):
    def test_basic_case(self):
        titles = ['Акула', 'Бобр', 'Барсук', 'Верблюд', 'Аист']
        result = count_animals_by_letter(titles)
        expected = [('А', 2), ('Б', 2), ('В', 1)]
        self.assertEqual(result, expected)

    def test_non_cyrillic(self):
        titles = ['Aardvark', 'Ёж', 'Zebra']
        result = count_animals_by_letter(titles)
        expected = [('Ё', 1)]
        self.assertEqual(result, expected)

    def test_empty_list(self):
        titles = []
        result = count_animals_by_letter(titles)
        expected = []
        self.assertEqual(result, expected)

class TestFetchAnimals(unittest.TestCase):
    @patch('main.requests.get')
    def test_fetch_animals(self, mock_get):
        mock_get.return_value.json.return_value = {
            'query': {
                'categorymembers': [
                    {'title': 'Акула'},
                    {'title': 'Белка'}
                ]
            }
        }
        mock_get.return_value.status_code = 200

        result = list(fetch_animals_from_wikipedia())
        self.assertEqual(result, ['Акула', 'Белка'])

class TestImportToCsv(unittest.TestCase):
    def test_save_read_csv(self):
        test_data = [('А', 2), ('Б', 1), ('В', 0)]

        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv', mode='w+', encoding='utf-8') as tmpfile:
            filename = tmpfile.name

        try:
            save_counts_to_csv(test_data, filename)
            with open(filename, encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                rows = list(reader)

            expected = [['А', '2'], ['Б', '1'], ['В', '0']]
            self.assertEqual(rows, expected)

        finally:
            os.remove(filename)

if __name__ == '__main__':
    unittest.main()
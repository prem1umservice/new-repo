```py
import os
import requests
import pyautogui as pag
from bs4 import BeautifulSoup
import urllib.parse
import os
import requests
import pyautogui as pag
from bs4 import BeautifulSoup
import urllib.parse
import json  # Импортируем модуль json

# Функция для получения информации о продукте
def get_product_info(url):
    # Установите заголовки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Выполните GET-запрос
    response = requests.get(url, headers=headers)

    # Проверьте ответ
    if response.ok:
        print("Запрос успешен")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлеките название продукта
        title = soup.find('h1')
        print(f"Информация элемента: {title.get_text(strip=True) if title else 'Не найден'}")
    else:
        print(f"Произошла ошибка: {response.status_code}")
        return None, None, None

# Замените на свои данные
GITHUB_TOKEN = "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"
REPO_OWNER = "prem1umservice"
REPO_NAME = "Jarvis"

def create_issue(title, body):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues&quot;
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {
        "title": title,
        "body": body
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    response.raise_for_status()
    return response.json()

# Пример использования
title = "Test issue from Python script"
body = "This is a test issue created using the GitHub API."
issue = create_issue(title, body)
print(f"Issue created: {issue['html_url']}")

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f'Файл {filename} успешно сохранён.')
    except requests.exceptions.RequestException as e:
        print(f'Произошла ошибка при загрузке файла: {e}')

# Функция для получения URL изображений
def get_image_urls(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        images = soup.select('button[data-fancybox="gallery"] img')[:11]
        return [img['src'] for img in images if 'src' in img.attrs]  # Проверка наличия атрибута
    except requests.exceptions.RequestException as e:
        print(f'Ошибка при получении страницы: {e}')
        return []
    except Exception as e:
        print(f'Ошибка: {e}')
        return []

# Функция для получения информации о продукте
def get_product_info(url):
    # Установите заголовки
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    # Выполните GET-запрос
    response = requests.get(url, headers=headers)

    # Проверьте ответ
    if response.ok:
        print("Запрос успешен")
        soup = BeautifulSoup(response.text, 'html.parser')

        # Извлеките название продукта
        title = soup.find('h1')
        print(f"Информация элемента: {title.get_text(strip=True) if title else 'Не найден'}")
    else:
        print(f"Произошла ошибка: {response.status_code}")
        return None, None, None

def post_natal_chart(url):
    # Формируем данные формы
    payload = {
        'fn': '',
        'fd': '1',
        'fm': '1',
        'fy': '1980',
        'fh': '12',
        'fmn': '0',
        'c1': 'Москва, Россия',
        'ttz': '20',
        'tz': 'Europe/Moscow',
        'tm': '3',
        'lt': '55.7522',
        'ln': '37.6155',
        'hs': 'P',
        'sb': '1'  # This simulates clicking the button
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like
Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find('font', {'face': 'Courier New'})
        if element:
            text = element.get_text(strip=True)
            span_element = element.find('span')
            style = span_element.get('style') if span_element else None
            return text, style
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None, None
    except Exception as e:
        print(f"Parsing error: {e}")
        return None, None

# The following block is removed because it is redundant and incorrect.
# If you want to implement a GET version, do it in a separate function.
        return None, None

# Вызов функции post_natal_chart с URL
text, style = post_natal_chart("https://geocult.ru/natalnaya-karta-onlayn-raschet&quot;)
if text and style:
    print(f"Информация элемента: {text}")
    print(f"Цвет элемента: {style}")
else:
    print("Не удалось получить информацию о натальной карте.")

import requests
from bs4 import BeautifulSoup

def get_natal_chart(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find('font', {'face': 'Courier New'})
        if element:
            text = element.get_text(strip=True)
            span_element = element.find('span')
            style = span_element.get('style') if span_element else None
            return text, style
        else:
            return None, None
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None, None
    except Exception as e:
        print(f"Parsing error: {e}")
        return None, None

# Формируем URL с параметрами
base_url = "https://geocult.ru/natalnaya-karta-onlayn-raschet&quot;
params = {
    'fn': '',
    'fd': '1',
    'fm': '2', #изменено на 2
    'fy': '1980',
    'fh': '12',
    'fmn': '0',
    'c1': 'Москва, Россия',
    'ttz': '20',
    'tz': 'Europe/Moscow',
    'tm': '3',
    'lt': '55.7522',
    'ln': '37.6155',
    'hs': 'P',
    'sb': '1'
}
url = f"{base_url}?{urllib.parse.urlencode(params)}"

# Вызываем функцию response = requests.get(url, timeout=10)  # Увеличить таймаут до 10 секунд_natal_chart с URL
text, style = get_natal_chart(url)
if text and style:
    print(f"Информация элемента: {text}")
```

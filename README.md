import os
import shutil
import requests
import pyautogui as pag
from bs4 import BeautifulSoup
import pyperclip  # Для буфера обмена
from IP import API, KEY  # Импорт ключей API и KEY
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import itertools
import time  # Убедитесь, что модуль time импортирован
from PIL import Image  # Импортируем Image из PIL

# Инициализация WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


# Функция для загрузки файла по ссылке
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
        title_text = title.text.strip() if title else "Название отсутствует."  # Обработка NoneType

        # Извлеките цену
        price = soup.find('span', class_='styles_sidebar__main__DaXQC')
        price_text = price.text.strip() if price else 'Цена отсутствует.'  # Обработка NoneType

        # Извлеките описание
        description_div = soup.find('div', class_='styles_description__8_RRa')
        description_text = description_div.text.strip() if description_div else 'Описание отсутствует.'  # Обработка NoneType
        print("Информация скопирована в буфер обмена:\n", title_text, price_text, description_text)
        return title_text, price_text, description_text
    else:
        print(f"Произошла ошибка: {response.status_code}")
        return None, None, None

# Инициализация WebDriver
driver = webdriver.Chrome()  # Убедитесь, что у вас правильно установлен ChromeDriver
try:
    # Переход к странице профиля
    profile_url = "https://999.md/ru/profile/EgorCeban"
    driver.get(profile_url)

    conf = pag.confirm("Продолжить?", "Confirmation")
    if conf == "OK":
        # Получение обновленного URL
        updated_url = driver.current_url  # Получаем текущий URL из браузера

        print(f"Используемый URL: {updated_url}")

        # Получаем данные о продукте
        title_text, price_text, description_text = get_product_info(updated_url)

        if title_text is None or price_text is None or description_text is None:
            print("Не удалось получить информацию о продукте.")

        # Получение изображений
        image_urls = get_image_urls(updated_url)

        if image_urls:
            print(f'Найдено {len(image_urls)} изображений.')
            directory = '/Users/egorceban/downloads'

            if os.path.exists(directory):
                shutil.rmtree(directory)
            os.makedirs(directory)
            for i, img_url in enumerate(image_urls):
                # Преобразуем относительный путь к абсолютному URL, если нужно
                if not img_url.startswith('http'):
                    base_url = updated_url.rsplit('/', 1)[0] + "/"
                    img_url = base_url + img_url

                filename = os.path.join(directory, f'image_{i + 1}.jpg')
                download_file(img_url, filename)
        else:
            print('Изображения не найдены.')
        clipboard_text = pyperclip.paste()  # Получаем текст из буфера обмена

    # Получаем текст из буфера обмена для вставки
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Current URL:", driver.current_url)

# Функция для обработки объявления для стиральных машин
def process_washing(title_text, description_text, price_text):
    try:
        washing_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/washing-machines')]//span[@itemprop='name' and text()='Стиральные и сушильные машины']"
            ))
        )
        if washing_link:
            print("Объявление для стиральных машин выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fwashing-machines"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Wash")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Wash")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Wash:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Wash найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Wash:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Wash")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())

                # Навигация с помощью TAB и стрелок
                tab_counts = [1, 2, 1, 2]
                down_counts = [3, 2, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
                    print("Элемент выбран через pag для Wash")
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Wash:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Wash")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Wash")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Wash:", e)
        else:
            print("Кнопка для Wash не найдена.")
    except Exception as e:
        print("Ошибка в операции для Wash:", e)

# Функция для обработки объявления для холодильников
def process_refrigerators(title_text, description_text, price_text):
    try:
        refrigerators_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/refrigerators')]//span[@itemprop='name' and text()='Холодильники']"
            ))
        )
        if refrigerators_link:
            print("Объявление для холодильников выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Frefrigerators"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Фризера")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Фризера")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
                # Навигация для выбора с помощью TAB и стрелок
                tab_counts = [2, 2, 1]
                down_counts = [14, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
                    print("Элемент выбран через pag для Фризера")
            except Exception as e:
                print("Ошибка при вводе заголовка для Фризера:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Фризера найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Фризера:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Фризера")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                                                # Навигация для выбора с помощью TAB и стрелок
                tab_counts = [1]
                down_counts = [3]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Фризера:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Фризера")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Фризера")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Фризера:", e)
        else:
            print("Кнопка для Фризера не найдена.")
    except Exception as e:
        print("Ошибка в операции для Фризера:", e)

# Функция для обработки объявления для духовок и газовых плит
def process_stove_oven(title_text, description_text, price_text):
    try:
        stove_oven_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/stove-oven')]//span[@itemprop='name' and text()='Газовые и электроплиты']"
            ))
        )
        if stove_oven_link:
            print("Объявление для духовок и газовых плит выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fstove-oven"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Stove/Oven")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Stove/Oven")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Stove/Oven:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Stove/Oven найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Stove/Oven:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Stove/Oven")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                # Навигация с помощью TAB и стрелок
                tab_counts = [1, 3, 1, 3]
                down_counts = [4, 3, 4, 3]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)

            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Stove/Oven:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Stove/Oven")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Stove/Oven")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Stove/Oven:", e)
        else:
            print("Кнопка для Stove/Oven не найдена.")
    except Exception as e:
        print("Ошибка в операции для Stove/Oven:", e)

# Функция для обработки объявления для микроволновых печей
def process_microwaves(title_text, description_text, price_text):
    try:
        microwaves_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/microwaves')]//span[@itemprop='name' and text()='Микроволновые печи']"
            ))
        )
        if microwaves_link:
            print("Объявление для микроволновых печей выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fmicrowaves"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Microwaves")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Microwaves")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Microwaves:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Microwaves найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Microwaves:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Microwaves")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())

                # Навигация с помощью TAB и стрелок
                tab_counts = [1, 2, 1, 2]
                down_counts = [3, 2, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)

            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Microwaves:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Micроволновых печей")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Micроволновых печей")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Micроволновых печей:", e)
        else:
            print("Кнопка для Micроволновых печей не найдена.")
    except Exception as e:
        print("Ошибка в операции для Micроволновых печей:", e)

# Функция для обработки объявления для пароварок
def process_steam_cookers(title_text, description_text, price_text):
    try:
        steam_cookers_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/steam-cookers')]//span[@itemprop='name' and text()='Пароварки']"
            ))
        )
        if steam_cookers_link:
            print("Объявление для пароварок выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fsteam-cookers"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Steam Cookers")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Steam Cookers")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Steam Cookers:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Steam Cookers найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Steam Cookers:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Steam Cookers")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                # Навигация с помощью TAB и стрелок
                tab_counts = [1, 2, 3]
                down_counts = [3, 7, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Steam Cookers:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Steam Cookers")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Steam Cookers")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Steam Cookers:", e)
        else:
            print("Кнопка для Steam Cookers не найдена.")
    except Exception as e:
        print("Ошибка в операции для Steam Cookers:", e)

# Функция для обработки объявления для посудомоечных машин
def process_dishwashers(title_text, description_text, price_text):
    try:
        dishwashers_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/dishwashers')]//span[@itemprop='name' and text()='Посудомоечные машины']"
            ))
        )
        if dishwashers_link:
            print("Объявление для посудомоечных машин выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fdishwashers"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Dishwashers")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Dishwashers")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Dishwashers:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Dishwashers найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Dishwashers:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Dishwashers")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                tab_counts = [1, 1, 3]
                down_counts = [3, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Dishwashers:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Dishwashers")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Dishwashers")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Dishwashers:", e)
        else:
            print("Кнопка для Dishwashers не найдена.")
    except Exception as e:
        print("Ошибка в операции для Dishwashers:", e)

# Функция для обработки объявления для кофемашин
def process_coffee_machines(title_text, description_text, price_text):
    try:
        coffee_machines_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/household-appliances/coffee-machines')]//span[@itemprop='name' and text()='Кофемашины']"
            ))
        )
        if coffee_machines_link:
            print("Объявление для кофемашин выбрано.")
            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fcoffee-machines"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Coffee Machines")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Coffee Machines")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Coffee Machines:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Coffee Machines найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Coffee Machines:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Coffee Machines")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                tab_counts = [1, 2, 1, 2]
                down_counts = [3, 2, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Coffee Machines:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Coffee Machines")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Coffee Machines")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Coffee Machines:", e)
        else:
            print("Кнопка для Coffee Machines не найдена.")
    except Exception as e:
        print("Ошибка в операции для Coffee Machines:", e)

# Функция для обработки объявления для стерео компонентов
def process_stereo_components(title_text, description_text, price_text):
    try:
        stereo_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/audio-video-photo/stereo-components')]//span[@itemprop='name' and text()='Стерео компоненты']"
            ))
        )
        if stereo_link:
            print("Объявление для стерео компонентов выбрано.")
            url = "https://999.md/ru/add?category=audio-video-photo&subcategory=audio-video-photo%2Fstereo-components"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Stereo Components")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Stereo Components")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Stereo Components:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Stereo Components найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Stereo Components:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Stereo Components")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                tab_counts = [1, 2, 1, 2]
                down_counts = [3, 2, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Stereo Components:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Stereo Components")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Stereo Components")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Stereo Components:", e)
        else:
            print("Кнопка для Stereo Components не найдена.")
    except Exception as e:
        print("Ошибка в операции для Stereo Components:", e)

# Функция для обработки объявления для акустики, колонок
def process_acoustics_columns(title_text, description_text, price_text):
    try:
        acoustics_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//a[@itemprop='item' and contains(@href, '/ru/list/audio-video-photo/acoustics-columns')]//span[@itemprop='name' and text()='Акустика, колонки']"
            ))
        )
        if acoustics_link:
            print("Объявление для акустики, колонок выбрано.")
            url = "https://999.md/ru/add?category=audio-video-photo&subcategory=audio-video-photo%2Facoustics-columns"
            driver.get(url)
            pag.sleep(2)

            try:
                close_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                )
                close_button.click()
                driver.refresh()
                pag.sleep(2)
                print("Закрыто окно 'Понятно' для Acoustics Columns")
            except Exception:
                pass

            try:
                title_input = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                )
                print("Поле ввода заголовка найдено для Acoustics Columns")
                driver.execute_script("arguments[0].click();", title_input)
                title_input.send_keys(title_text)
                title_input.send_keys(Keys.TAB)
                pyperclip.copy(description_text)
                driver.switch_to.active_element.send_keys(pyperclip.paste())
            except Exception as e:
                print("Ошибка при вводе заголовка для Acoustics Columns:", e)

            try:
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()
                print("Выпадающий список для Acoustics Columns найден и открыт.")
            except Exception as e:
                print("Ошибка при открытии выпадающего списка для Acoustics Columns:", e)

            try:
                select_elem = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                )
                dropdown_select = Select(select_elem)
                dropdown_select.select_by_visible_text("Кишинёв мун.")
                print("Выбран пункт 'Кишинёв мун.' для Acoustics Columns")
                select_elem.send_keys(Keys.TAB)
                active = driver.switch_to.active_element
                pyperclip.copy(price_text)
                active.send_keys(pyperclip.paste())
                tab_counts = [1, 2, 1, 2]
                down_counts = [3, 2, 2, 4]
                for tab_count, down_count in zip(tab_counts, down_counts):
                    pag.press('tab', presses=tab_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('down', presses=down_count, interval=0.1)
                    pag.sleep(0.1)
                    pag.press('enter')
                    pag.sleep(0.1)
            except Exception as e:
                print("Ошибка при выборе из выпадающего списка для Acoustics Columns:", e)

            try:
                upload_label_ac = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                )
                ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                print("Клик по upload-label через ActionChains для Acoustics Columns")
                pag.press('down', presses=1, interval=0.1)
                pag.press('enter')
                pag.keyDown('shift')
                pag.press('down', presses=3, interval=0.1)
                pag.keyUp('shift')
                pag.press('enter')
                pag.sleep(1)
                agreement_checkbox = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "input#agreement"))
                )
                agreement_checkbox.click()
                print("Поставлена галочка согласия для Acoustics Columns")
                ActionChains(driver).send_keys(Keys.TAB * 3 + Keys.SPACE).perform()
                conf = pag.confirm("Продолжить?", "Confirmation")
            except Exception as e:
                print("Ошибка при загрузке фото для Acoustics Columns:", e)
        else:
            print("Кнопка для Acoustics Columns не найдена.")
    except Exception as e:
        print("Ошибка в операции для Acoustics Columns:", e)
try:
    # Получаем текст из буфера обмена для вставки
    clipboard_text = pyperclip.paste()
    # Переходим на страницу логина
    driver.get("https://v2.simpalsid.com/sid/ru/user/login")
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Введите логин или e-mail']"))
    )
    username_input.send_keys(API)
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Введите от 6 символов']"))
    )
    password_input.send_keys(KEY)
    pag.sleep(4)
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_solid__gEcaH"))
    )
    login_button.click()
    driver.execute_script("arguments[0].click();", login_button)
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.styles_redirectBtn__o_7FD"))
    )
    link.click()
    WebDriverWait(driver, 20).until(EC.url_contains("999.md"))
except Exception as e:
    print("Ошибка при логине:", e)
    print("Current URL:", driver.current_url)
# Создаём цикл для чередования объявлений
def main():
    advertisement_cycle = itertools.cycle([
        "washing", "refrigerators", "stove_oven", "microwaves", "steam_cookers",
        "dishwashers", "coffee_machines", "stereo_components", "acoustics_columns"
    ])
    first_run = True
    while True:
        ad_type = next(advertisement_cycle)
        print(f"Запуск цикла для: {ad_type}")
        if first_run:
            url_to_use = updated_url  # Первый раз используем обновленный URL
        else:
            url_to_use = driver.current_url  # Далее используем текущий URL (вы можете вручную открыть нужную страницу)
        driver.get(url_to_use)
        pag.sleep(0.01)
        title_text, price_text, description_text = get_product_info(driver.current_url)
        if not (title_text and price_text and description_text):
            print("Не удалось получить информацию о продукте, повтор цикла.")
            continue
        if ad_type == "coffee_machines" and first_run:
            process_coffee_machines(title_text, description_text, price_text)
            first_run = False  # После первого объявления переключаемся на обычный режим
            continue
        if ad_type == "washing":
            process_washing(title_text, description_text, price_text)
        elif ad_type == "refrigerators":
            process_refrigerators(title_text, description_text, price_text)
        elif ad_type == "stove_oven":
            process_stove_oven(title_text, description_text, price_text)
        elif ad_type == "microwaves":
            process_microwaves(title_text, description_text, price_text)
        elif ad_type == "steam_cookers":
            process_steam_cookers(title_text, description_text, price_text)
        elif ad_type == "dishwashers":
            process_dishwashers(title_text, description_text, price_text)
        elif ad_type == "coffee_machines":
            process_coffee_machines(title_text, description_text, price_text)
        elif ad_type == "stereo_components":
            process_stereo_components(title_text, description_text, price_text)
        elif ad_type == "acoustics_columns":
            process_acoustics_columns(title_text, description_text, price_text)
        else:
            print("Неизвестный тип объявления")
        pag.sleep(0.01)
if __name__ == "__main__":
    main()

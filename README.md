import os
import shutil
import requests
import pyautogui as pag
from bs4 import BeautifulSoup
import pyperclip  #Для буферa
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

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
            directory = 'downloaded_images'

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

try:
    # Получаем текст из буфера обмена для вставки
    clipboard_text = pyperclip.paste()  # Получаем текст из буфера обмена
    # Open the login page of the website
    driver.get("https://www.facebook.com")  # Replace with actual login URL if needed

    # Wait for the login input field and enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='royal-email']"))
    )

    API = "+37379503566"
    KEY = "angeles1"
    username_input.send_keys(API)

    # Wait for the password input field and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[data-testid='royal-pass']"))
    )

    password_input.send_keys(KEY)
    pag.sleep(5)  # Ждем, чтобы устранить возможные задержки

    # Wait for the "Вход" button and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[name='login'][data-testid='royal-login-button']"))
    )
    login_button.click()
    conf = pag.confirm("Продолжить?", "Confirmation")
    if conf == "OK":

        print("Продолжить URL")
    # Optionally, wait for the page to load after login
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a.styles_redirectBtn__o_7FD"))
    )
    
  
    # Wait for the redirect to the 999.md URL
    WebDriverWait(driver, 20).until(EC.url_contains("https://www.facebook.com"))

    # Navigate to the profile page
except Exception as e:
    print(f"An error occurred: {str(e)}")

path = ["wash.png", "freeze.png", "/Users/egorceban/PycharmProjects/pythonProject/brave3690/oven.png", "micro.png", "dish.png", "coffee.png"] # Картинки
Wash = r"C:\Program Files\JetBrains\PyCharm 2023.3.4\FB.create\wash.png"
Freeze, Oven, Micro, Dish, Coffee = "freeze.png", "oven.png", "micro.png", "dish.png", "coffee.png" # Картинки
def find_and_click(image_path):
    try:
        location = pag.locateOnScreen(image_path, confidence=0.75)
        pag.sleep(1)
        if location is not None:
            print(f"Кнопка найдена!")
        else:
            print(f"Кнопка '{image_path}' не найдена.")
    except Exception as e:
        print(f"Ошибка: {e}")
        return False  # Возвращаем False, если произошла ошибка

# Основная функция
def main():
    while True:
        try:
            location = pag.locateOnScreen(Wash, confidence=0.11)
            pag.sleep(1)
            if location is not None:
                print(f"Кнопка Wash найдена")
                # Переход к странице добавления объявления
                url = "https://www.facebook.com/marketplace/create/item"
                driver.get(url)
                pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                # Wait for the page containing the input field for the title
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.xtpw4lu.x1tutvks.x1s3xk63.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3"))
                )
                title_input = driver.find_element(By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.xtpw4lu.x1tutvks.x1s3xk63.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3")
                title_input.send_keys(title_text)
                print("Название вставлено в поле ввода.")

                pag.sleep(1)

                pag.sleep(1)

                # Получаем активный элемент после TAB
                active_element = driver.switch_to.active_element
                try:
                    element_id = active_element.get_attribute("id")
                    element_name = active_element.get_attribute("name")
                    element_placeholder = active_element.get_attribute("placeholder")
                    print(f"Атрибуты активного элемента: id={element_id}, name={element_name}, placeholder={element_placeholder}")
                except Exception as e:
                    print(f"Не удалось получить атрибуты активного элемента: {e}")

                # Теперь можно использовать active_element для ввода текста
                active_element.click()
                pag.sleep(0.5)
                pag.press('enter')

                pag.sleep(1)

                pag.sleep(1)

                # Получаем активный элемент после TAB
                active_element = driver.switch_to.active_element
                try:
                    element_id = active_element.get_attribute("id")
                    element_name = active_element.get_attribute("name")
                    element_placeholder = active_element.get_attribute("placeholder")
                    print(f"Атрибуты активного элемента: id={element_id}, name={element_name}, placeholder={element_placeholder}")
                except Exception as e:
                    print(f"Не удалось получить атрибуты активного элемента: {e}")

                # Теперь можно использовать active_element для ввода текста
                active_element.click()
                pag.sleep(0.5)
                pag.press('enter')
                button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Дополнительная информация']/ancestor::div[@role='button']"))
                )
                button.click()

                # Wait for the dropdown element and click it
                dropdown_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.xjyslct.xjbqb8w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.xzsf02u.x78zum5.x1jchvi3.x1fcty0u.x132q4wb.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x1a2a7pz.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.x1n2onr6.x16tdsg8.xh8yej3.x1ja2u2z"))
                )
                dropdown_button.click()

                # Wait for the desired option in the dropdown and select it
                desired_option = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Техника')]"))
                )
                desired_option.click()
                print("Текст кнопки:", button.text)
                button.click()

                # Нажатие на кнопку "Добавить фото"
                add_photo_button = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "div.x1i10hfl.x1qjc9v5.xjbqb8w.xjqpnuy.xa49m3k.xqeqjp1.x2hbi6w.x13fuv20.xu3j5b3.x1q0q8m5.x26u7qi.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x1ypdohk.xdl72j9.x2lah0s.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.x2lwn1j.xeuugli.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x16tdsg8.x1hl2dhg.xggy1nq.x1ja2u2z.x1t137rt.x1o1ewxj.x3x9cwd.x1e5q0jg.x13rtm0m.x1q0g3np.x87ps6o.x1lku1pv.x1a2a7pz.x78zum5.x1iyjqo2[role='button'][tabindex='0']"))
                )
                print("Текст кнопки 'Добавить фото':", add_photo_button.text)
                add_photo_button.click()
                print("Нажата кнопка: 'Дополнительная информация'")
                pag.sleep(10)

                # Нажатие на кнопку "Далее" с проверкой кликабельности
                next_button = WebDriverWait(driver, 50).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'x1lliihq') and text()='Далее']/ancestor::div[@role='none']"))
                )
                next_button.click()
                print("Кнопка 'Далее' нажата.")
                print("Описание вставлено в поле через буфер обмена и pag.")
                conf = pag.confirm("Продолжить?", "Confirmation")

                # Ожидание и клик по кнопке для открытия списка
                dropdown_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.ID, "«r28»"))  # Замените на правильный ID или локатор
                )
                dropdown_button.click()

                # Ожидание и выбор нужного пункта в списке
                desired_option = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[text()='Техника']"))  # Замените на правильный текст или локатор
                )
                desired_option.click()

            else:
                print(f"Кнопка найдена?")
                return True

        except Exception:

            try:
                location = pag.locateOnScreen(Wash, confidence=0.11)
                if location is not None:
                    print(f"Кнопка Wash найдена")
                    # Переход к странице добавления объявления
                    url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fwashing-machines"
                    driver.get(url)
                    pag.sleep(2)

                    # Automatically close the "Понятно" button if it appears
                    try:
                        close_button = WebDriverWait(driver, 50).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                        )
                        close_button.click()
                        print("Закрыто окно 'Понятно'.")
                    except Exception as e:
                        print("Кнопка 'Понятно' не найдена или произошла ошибка:", str(e))  

                    driver.refresh()  # Автоматическое обновление браузера
                    pag.sleep(1)  # Задержка после обновления  

                    # Попробуем кликнуть по элементу перед вводом текста
                    title_input = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                    )
                    title_input.click()  # Кликаем по элементу

                    title_input.send_keys(title_text)  # Вставляем текст

                    # Нажимаем на кнопку добавить фото
                    photo_upload_button = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "label.style_upload__label__7Jg1M[for='upload-photo']"))
                    )
                    photo_upload_button.click()  # Кликаем на кнопку добавить фото

                    # Нажимаем на кнопку выбора валюты и выбираем MDL
                    currency_select = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "select[name='#2.value.unit']"))
                    )
                    currency_select.click()  # Кликаем по элементу

                    # Выбираем MDL из выпадающего списка
                    mdl_option = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "option[value='UNIT_MDL']"))
                    )
                    mdl_option.click()  # Кликаем на MDL
                    print("Название вставлено в поле ввода.")

                    conf = pag.confirm("Продолжить?", "Confirmation")

                else:
                    print(f"Кнопка найдена?")
                    return True


            except Exception:
                try:

                    profile_url = "https://999.md/ru/profile/EgorCeban"
                    driver.get(profile_url)
                    pag.sleep(5)
                    location = pag.locateOnScreen(Oven, confidence=0.11)
                    pag.sleep(1)
                    if location is not None:
                        print(f"Кнопка Oven найдена")
                        # Переход к странице добавления объявления на Marketplace
                        url = "https://www.facebook.com/marketplace/create/item"
                        driver.get(url)
                        pag.sleep(1)

                        # Ждем поле для названия и вставляем название
                        WebDriverWait(driver, 20).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.xtpw4lu.x1tutvks.x1s3xk63.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3"))
                        )
                        title_input = driver.find_element(By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.xtpw4lu.x1tutvks.x1s3xk63.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3")
                        title_input.send_keys(title_text)
                        print("Название вставлено в поле ввода.")

                        pag.sleep(1)

                        button = WebDriverWait(driver, 30).until(
                            EC.element_to_be_clickable((By.XPATH, "//span[text()='Дополнительная информация']/ancestor::div[@role='button']"))
                        )
                        print("Текст кнопки:", button.text)
                        button.click()
                        print("Нажата кнопка: 'Дополнительная информация'")
                        try:
                            desc_input_locator = (By.ID, "«rfp»")
                            desc_input_field = WebDriverWait(driver, 50).until(
                                EC.element_to_be_clickable(desc_input_locator)
                            )
                            print("Поле описания найдено и кликабельно.")

                            # Шаг 3: Вставка текста в поле описания
                            desc_input_field.send_keys(description_text)
                            print(f"Текст '{description_text}' вставлен в поле описания.")

                        except Exception as e:
                            print(f"Ошибка при взаимодействии с полем описания: {e}")
                            # Здесь можно добавить логику для повторной попытки или завершения скрипта
                        print("Текст поля описания:", desc_input.get_attribute("aria-label") or desc_input.get_attribute("placeholder") or desc_input.get_attribute("id"))
                        desc_input.click()
                        pag.press('enter')
                        print("Фокус установлен на поле описания через TAB и ENTER. Вставляем текст через pag...")

                        pyperclip.copy(description_text)
                        pag.sleep(0.5)
                        pag.hotkey('command', 'v')
                        print("Описание вставлено в поле через буфер обмена и pag.")

                        # Кишинёв мун.(pag.sleep(0.1),
                        pag.keyDown('shift')
                        pag.press('tab', presses=1)
                        pag.keyUp('shift')
                        pag.press('down', presses=19, interval=0.01)
                        pag.press('enter')
                        # MDL
                        (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                         pag.press('down', presses=3, interval=0.01), pag.press('enter'))

                        (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                         pag.press('down', presses=2, interval=0.01), pag.press('enter'))  # Изменено на 2

                        (pag.sleep(1), pag.keyDown('shift'),
                         pag.press('tab', presses=2), pag.keyUp('shift'),
                         pag.sleep(1), pag.press('space'))
                        (pag.sleep(1),
                         pag.press('tab', presses=3), pag.keyDown('shift'),
                         pag.press('tab', presses=2), pag.keyUp('shift'),
                         pag.sleep(1), pag.press('space'))
                        (pag.sleep(2),
                         pag.click(), pag.sleep(2),
                         pag.press('down', presses=1, interval=0.01), pag.press('down', presses=1, interval=0.01),
                         pag.keyDown('shift'), pag.press('up', presses=1, interval=0.01),
                         pag.keyUp('shift'), pag.press('enter'))
                        pag.sleep(2)
                        (pag.sleep(1), pag.press('tab', presses=9),
                         pag.keyDown('shift'), pag.press('tab', presses=1),
                         pag.keyUp('shift'), pag.sleep(0.1),
                         pag.press('space'))
                        (pag.sleep(0.1), pag.press('tab', presses=3),
                         pag.sleep(0.1), pag.press('space'))
                        conf = pag.confirm("Продолжить?", "Confirmation")

                        # === Micro ===
                        location = pag.locateOnScreen(Micro, confidence=0.11)
                        pag.sleep(1)
                        if location is not None:
                            print(f"Кнопка Micro найдена")
                            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fmicrowaves"
                            driver.get(url)
                            pag.sleep(1)
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']"))
                            )
                            title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                            title_input.send_keys(title_text)
                            print("Название вставлено в поле ввода.")
                            pag.sleep(1)
                            description_input = driver.find_element(By.CSS_SELECTOR, "textarea[name='#13.value']")
                            description_input.send_keys(description_text)
                            print("Описание вставлено в поле ввода.")
                            price_input = driver.find_element(By.CSS_SELECTOR, "input[name='#2.value.value']")
                            price_input.send_keys(price_text)
                            print("Цена вставлена в поле ввода.")
                            # ...дальнейшие действия по заполнению формы, как выше...
                            conf = pag.confirm("Продолжить?", "Confirmation")
                        else:
                            print(f"Кнопка Micro не найдена.")

                        # === Dish ===
                        location = pag.locateOnScreen(Dish, confidence=0.11)
                        pag.sleep(1)
                        if location is not None:
                            print(f"Кнопка Dish найдена")
                            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fdishwashers"
                            driver.get(url)
                            pag.sleep(1)
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']"))
                            )
                            title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                            title_input.send_keys(title_text)
                            print("Название вставлено в поле ввода.")
                            pag.sleep(1)
                            description_input = driver.find_element(By.CSS_SELECTOR, "textarea[name='#13.value']")
                            description_input.send_keys(description_text)
                            print("Описание вставлено в поле ввода.")
                            price_input = driver.find_element(By.CSS_SELECTOR, "input[name='#2.value.value']")
                            price_input.send_keys(price_text)
                            print("Цена вставлена в поле ввода.")
                            # ...дальнейшие действия по заполнению формы, как выше...
                            conf = pag.confirm("Продолжить?", "Confirmation")
                        else:
                            print(f"Кнопка Dish не найдена.")

                        # === Coffee ===
                        location = pag.locateOnScreen(Coffee, confidence=0.11)
                        pag.sleep(1)
                        if location is not None:
                            print(f"Кнопка Coffee найдена")
                            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances/coffee-machines"
                            driver.get(url)
                            pag.sleep(1)
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']"))
                            )
                            title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                            title_input.send_keys(title_text)
                            print("Название вставлено в поле ввода.")
                            pag.sleep(1)
                            description_input = driver.find_element(By.CSS_SELECTOR, "textarea[name='#13.value']")
                            description_input.send_keys(description_text)
                            print("Описание вставлено в поле ввода.")
                            price_input = driver.find_element(By.CSS_SELECTOR, "input[name='#2.value.value']")
                            price_input.send_keys(price_text)
                            print("Цена вставлена в поле ввода.")
                            # ...дальнейшие действия по заполнению формы, как выше...
                            conf = pag.confirm("Продолжить?", "Confirmation")
                        else:
                            print(f"Кнопка Coffee не найдена.")
                except Exception as error:
                    print(f"Произошла ошибка: {error}")
                    continue

if __name__ == "__main__":
    main()

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
    driver.get("https://v2.simpalsid.com/sid/ru/user/login")  # Replace with actual login URL if needed

    # Wait for the login input field and enter the username
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Введите логин или e-mail']"))
    )
    username_input.send_keys(API)

    # Wait for the password input field and enter the password
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder='Введите от 6 символов']"))
    )
    password_input.send_keys(KEY)
    pag.sleep(0.5)  # Ждем, чтобы устранить возможные задержки

    # Wait for the "Войти" button and click it
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.Button_solid__gEcaH"))
    )
    login_button.click()

    # Проверяем и нажимаем кнопку входа
    driver.execute_script("arguments[0].click();", login_button)

    # Опционально, ждём появления элемента после входа (например, главной страницы)

    # Ждем, пока не появится нужная ссылка на странице
    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "a.styles_redirectBtn__o_7FD"))
    )
    link.click()

    # Wait for the redirect to the 999.md URL
    WebDriverWait(driver, 20).until(EC.url_contains("999.md"))

    # Navigate to the profile page
except Exception as e:
    print(f"An error occurred: {str(e)}")

path = ["wash.png", "freeze.png", "/Users/egorceban/PycharmProjects/pythonProject/brave3690/oven.png", "micro.png", "dish.png", "coffee.png"] # Картинки
Wash = r"/Users/egorceban/PycharmProjects/pythonProject/wash.png"
def find_and_click(image_path):
    try:
        location = pag.locateOnScreen(image_path, confidence=0.11)
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
            location = pag.locateOnScreen(Wash, confidence=0.12)
            if location is not None:
                print("Кнопка Wash найдена")
                # Переход к странице добавления объявления
                url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fwashing-machines"
                driver.get(url)

                # Закрываем всплывающее окно, если оно появляется
                try:
                    close_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton")
                        )
                    )
                    close_button.click()
                    print("Закрыто окно 'Понятно'.")
                except Exception:
                    print("Popup не найден, продолжаем.")

                # Далее выполняем действия для заполнения формы
                actions = ActionChains(driver)
                actions.pause(1)
                # Навигация с помощью TAB и ввод цены
                for _ in range(3):
                    actions.send_keys(Keys.TAB)
                actions.send_keys(Keys.TAB)
                actions.send_keys(price_text)
                actions.send_keys(Keys.TAB)
                for _ in range(3):
                    actions.send_keys(Keys.ARROW_DOWN)
                actions.send_keys(Keys.ENTER)

                actions.pause(1)
                for _ in range(2):
                    actions.send_keys(Keys.TAB)
                for _ in range(2):
                    actions.send_keys(Keys.ARROW_DOWN)
                actions.send_keys(Keys.ENTER)

                actions.pause(1)
                for _ in range(3):
                    actions.send_keys(Keys.TAB)
                for _ in range(4):
                    actions.send_keys(Keys.ARROW_DOWN)
                actions.send_keys(Keys.ENTER)
                actions.pause(1)

                # Выбор из выпадающего списка "Кишинёв мун." с проверкой
                try:
                    select_elem = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']")
                        )
                    )
                    dropdown = Select(select_elem)
                    dropdown.select_by_visible_text("Кишинёв мун.")
                    print("Выбран пункт 'Кишинёв мун.' из выпадающего списка")
                except Exception as e:
                    print("Ошибка при выборе из выпадающего списка:", e)

                # Отметка галочкой, используя TAB, SHIFT+TAB и SPACE
                for _ in range(8):
                    actions.send_keys(Keys.TAB)
                # Используем SHIFT+TAB для перехода назад
                actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
                actions.send_keys(Keys.SPACE)
                actions.send_keys(Keys.SPACE)
                for _ in range(3):
                    actions.send_keys(Keys.TAB)
                actions.pause(0.1)
                actions.send_keys(Keys.SPACE)
                actions.perform()

                # Кликаем по выпадающему списку для продолжения
                dropdown = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                )
                dropdown.click()

                conf = pag.confirm("Продолжить?", "Confirmation")
            else:
                print("Кнопка не найдена.")
                return True
        except Exception as e:
            print("Ошибка в main:", e)

        except Exception:

            try:
                location = pag.locateOnScreen(Wash, confidence=0.12)
                if location is not None:
                    print(f"Кнопка Wash найдена")
                    # Переход к странице добавления объявления
                    url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fwashing-machines"
                    driver.get(url)

                    try:
                        close_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, "a.introjs-button.introjs-nextbutton.introjs-donebutton"))
                        )
                        close_button.click()
                        driver.refresh()  # Автоматическое обновление браузера
                        pag.sleep(1)  # Задержка после обновления  
                        print("Закрыто окно 'Понятно'.")
                    except Exception:
                        pass
                        dropdown = WebDriverWait(driver, 10).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, ".style_select__input__h0wAV"))
                        )
                        dropdown.click()
                        try:
                            upload_label = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='upload-photo']"))
                            )
                            # Первая попытка: JavaScript click
                            try:
                                driver.execute_script("arguments[0].click();", upload_label)
                                print("Сработал метод: JavaScript click на upload-label")
                            except Exception as js_e:
                                print("Метод click через JavaScript не удался, пробуем ActionChains:", js_e)
                                # Вторая попытка: ActionChains click
                                try:
                                    ActionChains(driver).move_to_element(upload_label).click().perform()
                                    print("Сработал метод: ActionChains click на upload-label")
                                except Exception as ac_e:
                                    print("Метод ActionChains click не удался:", ac_e)
                        except Exception as e:
                            print("Не удалось найти элемент upload-photo:", e)

                        # Выбор из выпадающего списка "Кишинёв мун." с проверкой
                        try:
                            select_elem = WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "select.style_select__input__h0wAV[name='#7.value']"))
                            )
                            dropdown = Select(select_elem)
                            dropdown.select_by_visible_text("Кишинёв мун.")
                            print("Выбран пункт 'Кишинёв мун.' из выпадающего списка")
                        except Exception as e:
                            print("Ошибка при выборе из выпадающего списка:", e)
                        # Попытка 1: Click через JavaScript
                        # Ждем поле для названия и вставляем название
                        # Попытка 2: Click через ActionChains
                        try:
                            upload_label_ac = WebDriverWait(driver, 10).until(
                                EC.element_to_be_clickable((By.CSS_SELECTOR, "label[for='upload-photo']"))
                            )
                            ActionChains(driver).move_to_element(upload_label_ac).click().perform()
                            print("Сработал метод: ActionChains click на upload-label")
                        except Exception as e:
                            print("Метод ActionChains click не удался:", e)
                    # Попробуем кликнуть по элементу перед вводом текста
                    title_input = WebDriverWait(driver, 50).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='#12.value.ru']"))
                    )
                    title_input.click()  # Кликаем по элементу

                    title_input.send_keys(title_text)  # Вставляем текст

                    conf = pag.confirm("Продолжить?", "Confirmation")

                else:
                    print(f"Кнопка найдена?")
                    return True


            except Exception:
                try:

                    location = pag.locateOnScreen(Wash, confidence=0.13)
                    if location is not None:
                        print(f"Кнопка Wash найдена")
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

                        actions = ActionChains(driver)

                        # MDL
                        actions.pause(1)
                        for _ in range(2):
                            actions.send_keys(Keys.TAB)
                        for _ in range(3):
                            actions.send_keys(Keys.ARROW_DOWN)
                        actions.send_keys(Keys.ENTER)

                        actions.pause(1)
                        for _ in range(2):
                            actions.send_keys(Keys.TAB)
                        for _ in range(2):
                            actions.send_keys(Keys.ARROW_DOWN)
                        actions.send_keys(Keys.ENTER)

                        actions.pause(1)
                        actions.key_down(Keys.SHIFT)
                        for _ in range(2):
                            actions.send_keys(Keys.TAB)
                        actions.key_up(Keys.SHIFT)
                        actions.pause(1)
                        actions.send_keys(Keys.SPACE)

                        actions.pause(1)
                        for _ in range(3):
                            actions.send_keys(Keys.TAB)
                        actions.key_down(Keys.SHIFT)
                        for _ in range(2):
                            actions.send_keys(Keys.TAB)
                        actions.key_up(Keys.SHIFT)
                        actions.pause(1)
                        actions.send_keys(Keys.SPACE)

                        actions.pause(2)
                        actions.click()  # Проводим клик в текущей позиции, если требуется
                        actions.pause(2)
                        for _ in range(2):
                            actions.send_keys(Keys.ARROW_DOWN)
                        actions.key_down(Keys.SHIFT).send_keys(Keys.ARROW_UP).key_up(Keys.SHIFT)
                        actions.send_keys(Keys.ENTER)

                        actions.pause(2)
                        for _ in range(9):
                            actions.send_keys(Keys.TAB)
                        actions.key_down(Keys.SHIFT).send_keys(Keys.TAB).key_up(Keys.SHIFT)
                        actions.pause(0.1)
                        actions.send_keys(Keys.SPACE)

                        actions.pause(1)
                        for _ in range(3):
                            actions.send_keys(Keys.TAB)
                        actions.pause(0.1)
                        actions.send_keys(Keys.SPACE)

                        actions.perform()
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

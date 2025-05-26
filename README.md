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

# Пример использования
try:
    driver.get("https://999.md/ru/profile/EgorCeban")
    print("Страница успешно открыта!")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    driver.quit()

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
    print("Current URL:", driver.current_url)

path = ["wash.png", "/Users/egorceban/PycharmProjects/pythonProject/brave3690/freeze.png", "/Users/egorceban/PycharmProjects/pythonProject/brave3690/oven.png", "micro.png", "dish.png", "coffee.png"] # Картинки
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

            location = pag.locateOnScreen(Wash, confidence=0.69)
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
                # Вставляем название в поле для названия
                title_input = driver.find_element(By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.xtpw4lu.x1tutvks.x1s3xk63.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w.x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb.x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3")
                title_input.send_keys(title_text)  # Вставляем текст
                print("Название вставлено в поле ввода.")

                pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                # Вставляем описание в соответствующее поле
                description_input = driver.find_element(By.CSS_SELECTOR,
                                                        "textarea[name='#13.value']")  # Предполагается, что это текстовая область
                description_input.send_keys(description_text)
                print("Описание вставлено в поле ввода.")

                # Вставляем цену в поле для цены
                price_input = driver.find_element(By.CSS_SELECTOR,
                                                  "input[name='#2.value.value']")  # Убедитесь, что здесь правильный селектор!
                price_input.send_keys(price_text)
                print("Цена вставлена в поле ввода.")
                

                # Допустим, у вас есть идентификатор фрейма, в котором находится кнопка "Регион"
                # Если фрейма нет, просто удалите этот блок и связанный с ним switch_to
                frame_id = "12900" # Замените на фактический ID вашего фрейма, если он есть

                # Переключаемся на фрейм (если он есть)
                # Если фрейма нет, закомментируйте или удалите следующие 2 строки
                WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, frame_id)))

                # Находим кнопку, которая открывает список городов (это твоя кнопка "select-style__input" с name "7")
                # Я использую CSS_SELECTOR, так как ты упомянула "select-style__input" и "name='7'"
                region_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, "button.select-style__input[name='7']"))
                )
                region_button.click()

                # Ждем, пока появится список городов.
                # Предполагаем, что список городов тоже имеет какой-то уникальный селектор.
                # Если это не всплывающий список, а просто новые элементы на странице,
                # то ожидание может быть по наличию одного из городов.
                # Здесь я использую общий селектор для списка, тебе нужно будет его уточнить
                city_list_container = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(@class, [@value='12900'])]"))  # Замените на актуальный селектор списка городов
                )

                # Теперь выбираем Кишинёв. Мы знаем его value='12900'.
                # Если Кишинёв отображается как <option value="12900">Кишинёв</option>
                # то используем By.XPATH с value.
                chisinau_option = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//option[@value='12900']"))
                )
                chisinau_option.click()

                # Проверяем, был ли выбор успешным (например, по изменению текста кнопки или по появлению нового элемента)
                # Этот блок может быть более специфичным для твоего сайта.
                # Здесь я проверяю, изменился ли текст на кнопке выбора региона на "Кишинёв".
                # Тебе нужно будет адаптировать это под фактический способ отображения выбранного города.
                try:
                    WebDriverWait(driver, 5).until(
                        EC.text_to_be_present_in_element((By.CSS_SELECTOR, "button.select-style__input[name='7']"), "Кишинёв")
                    )
                    print("Город Кишинёв выбран успешно.")
                except:
                    print("Не удалось подтвердить выбор города Кишинёв. Попробуем кликнуть ещё раз.")
                    chisinau_option.click() # Попробуем кликнуть еще раз

                # Возвращаемся к основному контексту страницы (если до этого переключались на фрейм)
                # Если фрейма нет, закомментируйте или удалите эту строку
                driver.switch_to.default_content()
                print("Успешное заполнение формы!")

                # Кишинёв мун.(pag.sleep(0.1),
                pag.keyDown('shift')
                pag.press('tab', presses=1)
                pag.keyUp('shift')
                pag.sleep(0.1)
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


            else:
                print(f"Кнопка найдена?")
                return True

        except Exception:

            try:
                profile_url = "https://999.md/ru/profile/EgorCeban"
                driver.get(profile_url)
                pag.sleep(5)

                location = pag.locateOnScreen(Freeze, confidence=0.75)
                pag.sleep(1)
                if location is not None:
                    print(f"Кнопка Freeze найдена")
                    # Переход к странице добавления объявления
                    url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Frefrigerators"
                    driver.get(url)
                    pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                    # Wait for the page containing the textarea
                    WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']")))

                    # Вставляем название в поле для названия
                    title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                    title_input.send_keys(title_text)  # Вставляем текст
                    print("Название вставлено в поле ввода.")

                    pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                    # Вставляем цену в поле для цены
                    price_input = driver.find_element(By.CSS_SELECTOR,
                                                      "input[name='#2.value.value']")  # Убедитесь, что здесь правильный селектор!
                    price_input.send_keys(price_text)
                    print("Цена вставлена в поле ввода.")

                    # Вставляем описание в соответствующее поле
                    description_input = driver.find_element(By.CSS_SELECTOR,
                                                            "textarea[name='#13.value']")  # Предполагается, что это текстовая область
                    description_input.send_keys(description_text)
                    print("Описание вставлено в поле ввода.")
                    # Используем frame_id из ввода
                    frame_id = "#708.value"
                    input_element = driver.find_element(By.CSS_SELECTOR, f"input[name='{frame_id}']")  # Убедитесь, что здесь правильный селектор!

                    # Переключаемся на фрейм, если требуется (обычно для input не нужен фрейм, но если нужен, используйте frame_id)
                    # WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.ID, frame_id)))

                    # Находим кнопку "Марка" и кликаем по ней (замените селектор на актуальный)
                    region_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, frame_id)))
                    region_button.click()

                    # Ждем, пока появится список городов (замените селектор на актуальный)
                    city_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, frame_id)))

                    # Выбираем нужный город из списка (замените селектор на актуальный)
                    city = city_list.find_element(By.CSS_SELECTOR, "option[value='18097']")
                    city.click()

                    # Проверяем, был ли выбор успешным
                    if city.is_selected():
                        print("Город выбран успешно")
                    else:
                        print("Не удалось выбрать город")
                        city.click()  # Попробуем кликнуть еще раз
                        pag.press('enter')  # Добавлен enter после повторного клика

                    # Возвращаемся к основному контексту страницы, если переключались на фрейм
                    # driver.switch_to.default_content()

                    select = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "select[name='#708.value']"))
                    )
                    select = Select(select)
                    select.select_by_value("18097")

                    # Новый блок, который нужно добавить перед MDL. Поменять местами блок цена с текстом
                    (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                     pag.press('down', presses=2, interval=0.01),
                     pag.press('enter'),  # Добавлено нажатие Enter
                     pag.keyDown('shift'), pag.press('tab', presses=1, interval=0.01),
                     pag.keyUp('shift'), pag.sleep(0.1),
                     pag.press('space'), pag.sleep(0.1),
                     pag.press('tab', presses=5, interval=0.01))

                    # Блок MDL
                    (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                     pag.press('down', presses=3, interval=0.01), pag.press('enter'))

                    # Остальной код
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

                else:
                    print(f"Кнопка найдена?")
                    return True
                #

            except Exception:
                try:

                    profile_url = "https://999.md/ru/profile/EgorCeban"
                    driver.get(profile_url)
                    pag.sleep(5)
                    location = pag.locateOnScreen(Oven, confidence=0.75)
                    pag.sleep(1)
                    if location is not None:
                        print(f"Кнопка Oven найдена")
                        location = pag.locateOnScreen(Oven, confidence=0.75)
                        pag.sleep(1)
                        if location is not None:
                            print(f"Кнопка Micro найдена")
                            # Переход к странице добавления объявления
                            url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fstove-oven"
                            driver.get(url)
                            pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                            # Wait for the page containing the textarea
                            WebDriverWait(driver, 20).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']")))

                            # Вставляем название в поле для названия
                            title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                            title_input.send_keys(title_text)  # Вставляем текст
                            print("Название вставлено в поле ввода.")

                            pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                            # Вставляем описание в соответствующее поле
                            description_input = driver.find_element(By.CSS_SELECTOR,
                                                                    "textarea[name='#13.value']")  # Предполагается, что это текстовая область
                            description_input.send_keys(description_text)
                            print("Описание вставлено в поле ввода.")

                            # Вставляем цену в поле для цены
                            price_input = driver.find_element(By.CSS_SELECTOR,
                                                              "input[name='#2.value.value']")  # Убедитесь, что здесь правильный селектор!
                            price_input.send_keys(price_text)
                            print("Цена вставлена в поле ввода.")
                            print("Успешное заполнение формы!")

                            (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                             pag.press('down', presses=3, interval=0.01), pag.press('enter'))

                            (pag.sleep(1), pag.press('tab', presses=3, interval=0.01),
                             # Блок, следующий за MDL - 3 нажатия Tab
                             pag.press('down', presses=3, interval=0.01),  # 3 нажатия вниз
                             pag.press('enter'))  # Добавлено нажатие Enter
                            pag.press('tab', presses=1, interval=0.01),  # 1 нажатие Tab
                            pag.press('down', presses=4, interval=0.01),  # 4 нажатия вниз
                            pag.press('enter')  # Добавлено нажатие Enter

                            pag.press('tab', presses=15)  # Изменено с 9 на 15 нажатий Tab после указанного блока
                            # Добавлено нажатие enter.
                            pag.press('enter')

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
                            (pag.sleep(1), pag.press('tab', presses=15),
                            pag.keyDown('shift'), pag.press('tab', presses=1),
                            pag.keyUp('shift'), pag.sleep(0.1),
                            pag.press('space'))
                            (pag.sleep(0.1), pag.press('tab', presses=3),
                            pag.sleep(0.1), pag.press('space'))

                            conf = pag.confirm("Продолжить?", "Confirmation")

                    else:
                        print(f"Кнопка не найдена.")

                except Exception:  # 
                    try:

                        profile_url = "https://999.md/ru/profile/EgorCeban"
                        driver.get(profile_url)
                        pag.sleep(5)
                        location = pag.locateOnScreen(Micro, confidence=0.75)
                        pag.sleep(1)
                        if location is not None:
                            print(f"Кнопка Micro найдена")
                            location = pag.locateOnScreen(Micro, confidence=0.75)
                            pag.sleep(1)
                            if location is not None:
                                print(f"Кнопка Micro найдена")
                                # Переход к странице добавления объявления
                                url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fmicrowaves"
                                driver.get(url)
                                pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                                # Wait for the page containing the textarea
                                WebDriverWait(driver, 20).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']")))

                                # Вставляем название в поле для названия
                                title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                                title_input.send_keys(title_text)  # Вставляем текст
                                print("Название вставлено в поле ввода.")

                                pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                                # Вставляем описание в соответствующее поле
                                description_input = driver.find_element(By.CSS_SELECTOR,
                                                                        "textarea[name='#13.value']")  # Предполагается, что это текстовая область
                                description_input.send_keys(description_text)
                                print("Описание вставлено в поле ввода.")

                                # Вставляем цену в поле для цены
                                price_input = driver.find_element(By.CSS_SELECTOR,
                                                                  "input[name='#2.value.value']")  # Убедитесь, что здесь правильный селектор!
                                price_input.send_keys(price_text)
                                print("Цена вставлена в поле ввода.")
                                print("Успешное заполнение формы!")

                                # MDL
                                (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                                 pag.press('down', presses=3, interval=0.01), pag.press('enter'))

                                (pag.sleep(1), pag.press('tab', presses=1, interval=0.01),  # Блок, следующий за MDL
                                 pag.press('down', presses=2, interval=0.01), pag.press('enter'))  #

                                pag.press('tab', presses=14)  # Добавлено 14 нажатий Tab после указанного блока

                                (pag.sleep(1), pag.keyDown('shift'),
                                 pag.press('tab', presses=2), pag.keyUp('shift'),
                                 pag.sleep(1), pag.press('space'))
                                (pag.sleep(1),
                                 pag.press('tab', presses=3), pag.keyDown('shift'),
                                 pag.press('tab', presses=2), pag.keyUp('shift'),
                                 pag.sleep(1), pag.press('space'))
                                (pag.sleep(2),
                                 pag.click(), pag.sleep(2),
                                 pag.press('down', presses=1, interval=0.01),
                                 pag.press('down', presses=1, interval=0.01),
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

                        else:
                            print(f"Кнопка Micro не найдена.")

                    except Exception:
                        try:

                            profile_url = "https://999.md/ru/profile/EgorCeban"
                            driver.get(profile_url)
                            pag.sleep(5)
                            location = pag.locateOnScreen(Dish, confidence=0.75)
                            pag.sleep(1)
                            if location is not None:
                                print(f"Кнопка Dish найдена")
                                # Переход к странице добавления объявления
                                url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances%2Fdishwashers"
                                driver.get(url)
                                pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                                # Wait for the page containing the textarea
                                WebDriverWait(driver, 20).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, "textarea[name='#13.value']")))

                                # Вставляем название в поле для названия
                                title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                                title_input.send_keys(title_text)  # Вставляем текст
                                print("Название вставлено в поле ввода.")

                                pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                                # Вставляем описание в соответствующее поле
                                description_input = driver.find_element(By.CSS_SELECTOR,
                                                                        "textarea[name='#13.value']")  # Предполагается, что это текстовая область
                                description_input.send_keys(description_text)
                                print("Описание вставлено в поле ввода.")

                                # Вставляем цену в поле для цены
                                price_input = driver.find_element(By.CSS_SELECTOR,
                                                                  "input[name='#2.value.value']")  # Убедитесь, что здесь правильный селектор!
                                price_input.send_keys(price_text)
                                print("Цена вставлена в поле ввода.")
                                print("Успешное заполнение формы!")

                                # MDL
                                (pag.sleep(1), pag.press('tab', presses=2, interval=0.01),
                                 pag.press('down', presses=3, interval=0.01), pag.press('enter'))

                                (pag.sleep(1), pag.press('tab', presses=1, interval=0.01),  # Блок, следующий за MDL
                                 pag.press('down', presses=2, interval=0.01), pag.press('enter'))  #

                                pag.press('tab', presses=9)  # Изменено с 14 на 9 нажатий Tab после указанного блока

                                (pag.sleep(1), pag.keyDown('shift'),
                                 pag.press('tab', presses=2), pag.keyUp('shift'),
                                 pag.sleep(1), pag.press('space'))
                                (pag.sleep(1),
                                 pag.press('tab', presses=3), pag.keyDown('shift'),
                                 pag.press('tab', presses=2), pag.keyUp('shift'),
                                 pag.sleep(1), pag.press('space'))
                                (pag.sleep(2),
                                 pag.click(), pag.sleep(2),
                                 pag.press('down', presses=1, interval=0.01),
                                 pag.press('down', presses=1, interval=0.01),
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

                            else:
                                print(f"Кнопка не найдена.")
                                # Переход к странице профиля




                        except Exception:
                            try:

                                profile_url = "https://999.md/ru/profile/EgorCeban"
                                driver.get(profile_url)
                                pag.sleep(5)
                                location = pag.locateOnScreen(Coffee, confidence=0.75)
                                pag.sleep(1)
                                if location is not None:
                                    print(f"Кнопка Coffee найдена")
                                    location = pag.locateOnScreen(Coffee, confidence=0.75)
                                    pag.sleep(1)
                                    if location is not None:
                                        print(f"Кнопка найдена и нажата!")
                                        url = "https://999.md/ru/add?category=household-appliances&subcategory=household-appliances/coffee-machines"
                                        driver.get(url)
                                        pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                                        # Wait for the page containing the textarea
                                        WebDriverWait(driver, 20).until(
                                            EC.presence_of_element_located(
                                                (By.CSS_SELECTOR, "textarea[name='#13.value']")))

                                        # Вставляем название в поле для названия
                                        title_input = driver.find_element(By.CSS_SELECTOR, "input[name='#12.value.ru']")
                                        title_input.send_keys(title_text)  # Вставляем текст
                                        print("Название вставлено в поле ввода.")

                                        pag.sleep(1)  # Задержка 1 секунда перед следующим элементом

                                        # Вставляем описание в соответствующее поле
                                        description_input = driver.find_element(By.CSS_SELECTOR,
                                                                                "textarea[name='#13.value']")  # Предполагается, что это текстовая область
                                        description_input.send_keys(description_text)
                                        print("Описание вставлено в поле ввода.")

                                        # Вставляем цену в поле для цены
                                        price_input = driver.find_element(By.CSS_SELECTOR,
                                                                          "input[name='#2.value.value']")  # Убедитесь, что здесь правильный селектор!
                                        price_input.send_keys(price_text)
                                        print("Цена вставлена в поле ввода.")
                                        print("Успешное заполнение формы!")

                                        # Кишинёв мун.
                                        (pag.sleep(0.1),
                                         pag.keyDown('shift'),
                                         pag.press('tab', presses=1),
                                         pag.keyUp('shift'),
                                         pag.sleep(0.1),
                                         pag.press('down', presses=19, interval=0.01),
                                         pag.press('enter'))

                                        # MDL
                                        (pag.sleep(1),
                                         pag.press('tab', presses=2, interval=0.01),
                                         pag.press('down', presses=3, interval=0.01),
                                         pag.press('enter'))

                                        (pag.sleep(1),
                                         pag.press('tab', presses=2, interval=0.01),
                                         pag.press('down', presses=6, interval=0.01),
                                         pag.press('enter'))

                                        (pag.sleep(1),
                                         pag.press('tab', presses=1, interval=0.01),
                                         pag.press('down', presses=8, interval=0.01),
                                         pag.press('enter'))

                                        (pag.sleep(1),
                                         pag.keyDown('shift'),
                                         pag.press('tab', presses=2),
                                         pag.keyUp('shift'),
                                         pag.sleep(1),
                                         pag.press('space'))

                                        (pag.sleep(1),
                                         pag.press('tab', presses=3),
                                         pag.keyDown('shift'),
                                         pag.press('tab', presses=2),
                                         pag.keyUp('shift'),
                                         pag.sleep(1),
                                         pag.press('space'))

                                        (pag.sleep(2),
                                         pag.click(),
                                         pag.sleep(2),
                                         pag.press('down', presses=1, interval=0.01),
                                         pag.press('down', presses=1, interval=0.01),
                                         pag.keyDown('shift'),
                                         pag.press('up', presses=1, interval=0.01),
                                         pag.keyUp('shift'),
                                         pag.press('enter'))
                                        pag.sleep(2),

                                        (pag.sleep(1),
                                         pag.press('tab', presses=9),
                                         pag.keyDown('shift'),
                                         pag.press('tab', presses=1),
                                         pag.keyUp('shift'),
                                         pag.sleep(0.1),
                                         pag.press('space'))

                                        (pag.sleep(0.1),
                                         pag.press('tab', presses=3),
                                         pag.sleep(0.1),
                                         pag.press('space'))
                                        conf = pag.confirm("Продолжить?", "Confirmation")

                                else:
                                    print(f"Кнопка Coffee не найдена.")
                                    return True

                            except Exception:
                                return False  # Возвращаем False, если произошла ошибка

if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test_frontend():
    # Налаштування Chrome у headless-режимі
    options = Options()
    options.add_argument("--headless=new")  # headless режим Chrome 109+
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # додатково (іноді потрібно в контейнері)
    options.add_argument("--disable-gpu")

    # Створюємо драйвер (потрібно, щоб у контейнері був chromedriver і браузер)
    driver = webdriver.Chrome(options=options)

    try:
        # Відкриваємо сторінку -- http та порт frontend-react-test.
        url = "http://host.docker.internal:3000/api/tasks/public"
        driver.get(url)

        # Чекаємо поки з'явиться елемент з текстом або просто body
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        page_source = driver.page_source

        # ✅ Перевірка, що сторінка відображає заголовок
        assert "Список задач" in page_source, "На сторінці немає тексту 'Список задач'"

        # ✅ Перевірка, що є дві задачі зі статусами
        assert "Перша задача - невиконана" in page_source, "Немає 'Першої задачі - невиконаної'"
        assert "Друга задача - виконана" in page_source, "Немає 'Другої задачі - виконаної'"

        print("✅ Тести пройшли: сторінка містить усі потрібні задачі та заголовок!")

    except AssertionError as e:
        print(f"❌ Тест не пройшов: {e}")

    finally:
        driver.quit()


if __name__ == "__main__":
    test_frontend()

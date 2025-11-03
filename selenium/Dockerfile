# Базовий образ Selenium із Chrome
FROM selenium/standalone-chrome:100.0

# Оновлюємо пакети та встановлюємо потрібні для Python 3 інструменти
USER root
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Робоча директорія
WORKDIR /tests

# Копіюємо файл інтеграційного тесту
COPY test_integration.py /tests/test_integration.py

# Встановлюємо Python-залежності
COPY requirements.txt /tests/requirements.txt
RUN python3 -m pip install --upgrade pip setuptools wheel \
 && python3 -m pip install --no-cache-dir -r /tests/requirements.txt

# Виконання тесту при старті контейнера
CMD ["python3", "test_integration.py"]
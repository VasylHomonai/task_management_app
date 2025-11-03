# Використовуємо базовий образ python
FROM python:3.12-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо requirements.txt для встановлення залежностей
COPY requirements.txt ./

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо інші файли проєкту
COPY . .

# Робимо entrypoint виконуваним
RUN chmod +x /app/app/entrypoint.sh

# Задаємо порт 5000
EXPOSE 5000

# Використовуємо entrypoint для ініціалізації
ENTRYPOINT ["/app/app/entrypoint.sh"]

# Запускаємо додаток
CMD ["python", "run.py"]
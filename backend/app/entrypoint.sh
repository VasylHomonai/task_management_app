#!/bin/bash
set -e

# Зчитуємо пароль із секрету
LIMITED_PASS=$(cat /run/secrets/limited_user_password)

# Формуємо DATABASE_URL
export DATABASE_URL="postgresql://limited_user:${LIMITED_PASS}@database:5432/app_db"

echo "Starting backend with DATABASE_URL=${DATABASE_URL}"

# Запускаємо бекенд
exec "$@"
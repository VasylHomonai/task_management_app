#!/usr/bin/env bash
set -euo pipefail

echo "=== 🔧 Ініціалізація користувачів та бази даних ==="

# Отримуємо паролі з Docker secrets (якщо вони є)
if [ -f /run/secrets/db_password ]; then
    DB_PASS=$(cat /run/secrets/db_password)
else
    DB_PASS=${POSTGRES_PASSWORD:-postgres}
fi

if [ -f /run/secrets/limited_user_password ]; then
    LIMITED_PASS=$(cat /run/secrets/limited_user_password)
else
    LIMITED_PASS="limited_default"
fi

# Підключаємось як суперкористувач postgres
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    -- Змінюємо пароль суперкористувача postgres
    ALTER USER postgres WITH PASSWORD '${DB_PASS}';
EOSQL

# Створюємо роль limited_user, якщо її ще немає
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
    DO
    \$do\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = 'limited_user') THEN
            CREATE USER limited_user WITH PASSWORD '${LIMITED_PASS}';
        END IF;
    END
    \$do\$;
EOSQL

# Створюємо базу app_db, якщо ще немає
DB_EXISTS=$(psql -U postgres -tAc "SELECT 1 FROM pg_database WHERE datname='app_db'")
if [ -z "$DB_EXISTS" ]; then
    echo "Створюємо базу даних app_db..."
    createdb -U postgres -O limited_user app_db
else
    echo "База даних app_db вже існує, пропускаємо створення."
fi

# Видаємо права користувачу limited_user на роботу з базою
psql -v ON_ERROR_STOP=1 --username "postgres" --dbname "app_db" <<-EOSQL
    GRANT CONNECT ON DATABASE app_db TO limited_user;
    GRANT USAGE ON SCHEMA public TO limited_user;
    GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO limited_user;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO limited_user;
EOSQL

echo "✅ Ініціалізація користувачів і бази даних завершена."

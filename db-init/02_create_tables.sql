-- Підключення до бази app_db
\c app_db postgres;

-- Створення таблиць
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    owner_id INT REFERENCES users(id),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Видаємо права користувачу limited_user
GRANT CONNECT ON DATABASE app_db TO limited_user;
GRANT USAGE ON SCHEMA public TO limited_user;

-- Права на таблиці
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO limited_user;

-- Права на майбутні таблиці
ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT SELECT, INSERT, UPDATE, DELETE ON TABLES TO limited_user;

-- Права на послідовності (щоб INSERT працював з SERIAL)
GRANT USAGE, SELECT, UPDATE ON ALL SEQUENCES IN SCHEMA public TO limited_user;

ALTER DEFAULT PRIVILEGES IN SCHEMA public
    GRANT USAGE, SELECT, UPDATE ON SEQUENCES TO limited_user;
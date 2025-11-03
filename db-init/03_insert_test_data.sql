-- Підключаємося до бази як limited_user
\c app_db limited_user;

-- Додаємо тестового користувача лише якщо база порожня
DO
$$
DECLARE
    user1_id INT;
BEGIN
    -- Якщо таблиця users порожня — додаємо користувача
    IF NOT EXISTS (SELECT 1 FROM users) THEN
        INSERT INTO users (username, password)
        VALUES
            ('testuser', 'scrypt:32768:8:1$1sBMD9JiAbCRiPUD$2829dac94bb959651503d3ee9d9bc194bb5caf8df50da4f5b5aaadfdfed3d29c7a08d54f642e99c51bec447c7ff095ae629d8f90f861fbc01a41087aa36612cc');
    END IF;

    -- Отримуємо ID користувача для зв’язку з таблицею tasks
    SELECT id INTO user1_id FROM users WHERE username = 'testuser' LIMIT 1;

    -- Якщо таблиця tasks порожня — додаємо задачі
    IF NOT EXISTS (SELECT 1 FROM tasks) THEN
        INSERT INTO tasks (title, description, owner_id, status)
        VALUES
            ('Перша задача', 'Тестова задача', user1_id, 'невиконана'),
            ('Друга задача', 'Ще одна тестова', user1_id, 'виконана');
    END IF;
END
$$;
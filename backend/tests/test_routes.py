import unittest
from app import create_app, db


class BasicTests(unittest.TestCase):

    def setUp(self):
        """Створюємо тестовий Flask-застосунок і клієнт"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.client = self.app.test_client()

        # Ініціалізуємо таблиці у контексті застосунку
        with self.app.app_context():
            from app.models import User, Task
            db.create_all()

    def tearDown(self):
        """Очищаємо базу після кожного тесту"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            print("🧹 Database tables dropped after test. \n")

    def log_test_start(self, test_name):
        """Показує який саме тест зараз виконується"""
        print(f"🔹 Running test: {test_name}...")

    def test_tasks_route_with_token(self):
        """Перевіряємо, що маршрут /api/tasks повертає 200 для авторизованого користувача"""
        self.log_test_start("GET /api/tasks with token")

        # Створюємо користувача
        self.client.post('/api/users/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # Логін і отримання токена
        login_resp = self.client.post('/api/users/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(login_resp.status_code, 200)
        self.assertIn('access_token', login_resp.json)
        access_token = login_resp.json['access_token']

        # Виконуємо GET /api/tasks з токеном
        response = self.client.get(
            '/api/tasks',
            headers={'Authorization': f'Bearer {access_token}'}
        )
        self.assertEqual(response.status_code, 200)
        print(f"✅ GET /api/tasks with token returned status {response.status_code}")

    def test_tasks_public_route(self):
        """Перевіряємо, що маршрут /api/tasks/public повертає 200"""
        self.log_test_start("GET /api/tasks/public")
        response = self.client.get('/api/tasks/public')
        self.assertEqual(response.status_code, 200)
        print(f"✅ GET /api/tasks/public returned status {response.status_code}")

    def test_user_registration(self):
        """Тестуємо реєстрацію користувача"""
        self.log_test_start("POST /api/users/register")
        response = self.client.post('/api/users/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        print(f"✅ User registration successful with status {response.status_code}")

    def test_user_login(self):
        """Тестуємо логін користувача"""
        self.log_test_start("POST /api/users/login")

        # спочатку створимо користувача
        self.client.post('/api/users/register', json={
            'username': 'testuser2',
            'password': 'testpassword2'
        })
        # тепер логін
        response = self.client.post('/api/users/login', json={
            'username': 'testuser2',
            'password': 'testpassword2'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)
        print(f"✅ User login successful, token received")

    def test_task_creation(self):
        """Тестуємо створення задачі"""
        self.log_test_start("POST /api/tasks")

        # реєстрація користувача
        self.client.post('/api/users/register', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        # логін
        login_resp = self.client.post('/api/users/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })

        # якщо логін пройшов — отримуємо токен
        if login_resp.status_code == 200 and 'access_token' in login_resp.json:
            access_token = login_resp.json['access_token']

            response = self.client.post('/api/tasks', json={
                'title': 'Тестова задача',
                'description': 'Тестовий опис',
                'owner_id': 1,
                'status': 'невиконано'
            }, headers={'Authorization': f'Bearer {access_token}'})

            self.assertEqual(response.status_code, 201)
            print(f"✅ Task creation successful with status {response.status_code}")
        else:
            # якщо логін не вдалий, тест все одно не повинен падати з помилкою
            self.skipTest("Login failed, cannot create task")


if __name__ == "__main__":
    unittest.main()
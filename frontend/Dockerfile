# Використовуємо офіційний Node.js образ
FROM node:18-alpine

# Робоча директорія всередині контейнера
WORKDIR /app

# Копіюємо package.json та package-lock.json у робочий каталог для встановлення залежностей
COPY package*.json ./

# Встановлюємо залежності
RUN npm install --legacy-peer-deps

# Копіюємо решту коду застосунку в робочий каталог
COPY . .

# Відкриваємо порт 3000 для React server
EXPOSE 3000

# Команда для запуску застосунку
CMD ["npm", "start"]
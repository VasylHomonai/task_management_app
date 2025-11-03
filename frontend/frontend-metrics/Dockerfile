# Базовий образ Node.js
FROM node:18-alpine

WORKDIR /app

# Копіюємо package.json і встановлюємо залежності
COPY package.json ./
RUN npm install --omit=dev

# Копіюємо код сервера
COPY index.js ./

# Порт, на якому буде слухати сервер
EXPOSE 3001

# Запуск сервера
CMD ["npm", "start"]



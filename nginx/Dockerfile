# Stage 1: build frontend
FROM node:18-alpine AS frontend-build
WORKDIR /app

# Копіюємо тільки package.json і package-lock.json для npm install
COPY frontend/package*.json ./
RUN npm install --legacy-peer-deps

# Копіюємо тільки потрібні каталоги для збірки React та виконуємо збірку
COPY frontend/src ./src
COPY frontend/public ./public
RUN npm run build


# Stage 2: nginx
FROM nginx:alpine

# Встановимо openssl для генерації сертифіката
RUN apk add --no-cache openssl bash

# Створюємо папку для сертифікатів
RUN mkdir -p /etc/nginx/certs

# Копіюємо build з попереднього stage
COPY --from=frontend-build /app/build /usr/share/nginx/html/

# Копіюємо nginx.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Копіюємо та виконуємо крипт для генерації self-signed сертифіката
COPY nginx/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Запускаємо через наш entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
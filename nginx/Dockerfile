FROM nginx:alpine

# Встановимо openssl для генерації сертифіката
RUN apk add --no-cache openssl bash

# Створюємо папку для сертифікатів
RUN mkdir -p /etc/nginx/certs

# Копіюємо React build
COPY /frontend/build/ /usr/share/nginx/html/

# Копіюємо nginx.conf
COPY nginx/nginx.conf /etc/nginx/nginx.conf

# Копіюємо та виконуємо крипт для генерації self-signed сертифіката
COPY nginx/entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Запускаємо через наш entrypoint
ENTRYPOINT ["/docker-entrypoint.sh"]
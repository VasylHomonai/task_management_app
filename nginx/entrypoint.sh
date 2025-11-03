#!/bin/sh
set -e

if [ ! -f /etc/nginx/certs/cert.pem ] || [ ! -f /etc/nginx/certs/key.pem ]; then
  echo "Generating self-signed SSL certificate..."
  openssl req -x509 -nodes -days 365 \
    -subj "/CN=localhost" \
    -newkey rsa:2048 \
    -keyout /etc/nginx/certs/key.pem \
    -out /etc/nginx/certs/cert.pem
fi

exec nginx -g "daemon off;"
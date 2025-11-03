# Базовий образ Logstash
FROM docker.elastic.co/logstash/logstash:9.1.5

# Копіюємо конфігураційний файл всередину контейнера
COPY logstash.conf /usr/share/logstash/pipeline/logstash.conf

# Встановлюємо права конфігу
USER root
RUN chown logstash:logstash /usr/share/logstash/pipeline/logstash.conf

# Повертаємося до користувача logstash
USER logstash

# Логування у stdout
CMD ["logstash", "-f", "/usr/share/logstash/pipeline/logstash.conf"]
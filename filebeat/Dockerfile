# Базовий офіційний образ Filebeat
FROM docker.elastic.co/beats/filebeat:9.1.5

# Копіюємо конфігураційний файл всередину контейнера
COPY filebeat.yml /usr/share/filebeat/filebeat.yml

# Встановлюємо root права для файла, як вимагає Filebeat
USER root
RUN chown root:root /usr/share/filebeat/filebeat.yml

# Запускаємо Filebeat від користувача filebeat
# USER filebeat

# Запускаємо Filebeat
CMD ["filebeat", "-e", "-c", "/usr/share/filebeat/filebeat.yml"]
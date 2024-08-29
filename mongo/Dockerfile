# Используем официальный образ MongoDB
FROM mongo:7.0.12

# Создаем директорию для логов и устанавливаем права доступа
RUN mkdir -p /var/log/mongodb && touch /var/log/mongodb/mongod.log && chmod -R 777 /var/log/mongodb

# Копируем конфигурационный файл в контейнер
COPY mongo/mongod.conf /etc/mongod.conf

# Открываем порт MongoDB
EXPOSE 27017

# Указываем команду для запуска MongoDB с конфигурационным файлом
# CMD ["mongod", "--config", "/etc/mongod.conf"]
CMD ["sleep","infinity"]

# ClickHouse Database

> База для хранения показаний датчиков  

## Развертывание  

После развертывания основного репозитория 

1. Перейти в папку clickhouse

```bash
cd clickhouse
```

2. Создайте файл .env и настроить его под свои данные по примеру env.example

3.Используйте Docker и Docker Compose 
```
docker-compose up -d
```

4. После запуска контейнера, ClickHouse автоматически выполнит скрипт инициализации init-db.sql, который создаст таблицу sensor_data

## Тестирование  
1. Настроить config.py по примеру config_example.py
2. Выполнить скрипт:
```bash
python db_connect.py
```
Будут получены данные из таблицы sensor_data.

from clickhouse_connect import get_client
import config 

# Подключение к ClickHouse
client = get_client(
    host=config.DB_HOST,
    username=config.DB_USERNAME,
    password=config.DB_PASSWORD,
)

# SQL-запрос для получения данных из таблицы
query = "SELECT * FROM sensor_data"

# Выполнение запроса
try:
    result = client.query(query).result_rows
    for row in result:
        print(row)
except Exception as e:
    print(f"Ошибка при запросе данных: {e}")
finally:
    client.close()

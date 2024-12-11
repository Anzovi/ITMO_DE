import utils
import config
from datetime import datetime
import requests
import logging
import urllib3


# Адрес ClickHouse DB
url = config.URL

# Заголовок Post запрос
headers = {
        "accept": "application/json",
        "X-API-Key": config.X_API_KEY,
        "Content-Type": "application/json"
        }

# Конфигурация логирования
logging.basicConfig(
    filename='data_transfer.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Основная программа
if __name__ == "__main__":
    try:
        client = utils.connect_to_modbus(config.IP_ADDRESS, config.PORT)
        logging.info("Modbus connection started")

        data_list = []
        # Обрабатываем результаты

        while True:
            for device_name, device_id in config.DEVICES.items():
                registers = utils.read_registers(client, config.REGISTER_ADDRESS, config.NUMBER_OF_REGISTERS, device_id)
                float_value = utils.convert_to_float32(registers)
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                device_data = {
                            "timestamp": timestamp, 
                            "device": device_name, 
                            "amperage": float_value
                            }

                data_list.append(device_data)

                # Отправка POST-запроса
            try:
                # Отправляем запрос
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) # отключаем предупреждение от verify=False
                response = requests.post(url, json=data_list, headers=headers, verify=False)

                data_list = []
                # Проверяем статус ответа
                if response.status_code == 200:
                    print(f"{timestamp}, {response.json()}")
                    logging.info(f"{response.json()}")

                else:
                    print(f"{timestamp}, {response.status_code}: {response.text}")
                    logging.error(f"{response.status_code}, {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"Exception when sent: {e}")
                logging.error(f"Exception when sent: {e}")

    finally:
        client.close()
        print("Modbus connection closed.")
        logging.info("Modbus connection closed.")
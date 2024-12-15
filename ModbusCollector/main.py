import logging
import sys
import threading
import time
from datetime import datetime
from logging.handlers import RotatingFileHandler

import requests
import urllib3

import utils
from config import settings

url = settings.API_URL

headers = {"accept": "application/json", "X-API-Key": settings.API_KEY, "Content-Type": "application/json"}

log_name = "data_transfer.log"
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = RotatingFileHandler(log_name, maxBytes=5 * 1024 * 1024, backupCount=1)
handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
log.addHandler(handler)
logging.getLogger("pymodbus").setLevel(logging.ERROR)

devices = {}


def update_devices():
    global devices  # noqa: PLW0603
    while True:
        devices = utils.fetch_devices(settings.APPWRITE_API_URL, settings.APPWRITE_PROJECT, settings.APPWRITE_API_KEY)
        time.sleep(60)


if __name__ == "__main__":
    try:
        client = utils.connect_to_modbus(settings.IP_ADDRESS, settings.PORT)

        if not client:
            logging.error("Unable connect to Modbus")
            print("Unable connect to Modbus")
            sys.exit(1)

        logging.info("Modbus connection started")
        print("Modbus connection started")

        threading.Thread(target=update_devices, daemon=True).start()

        register_address = settings.REGISTER_ADDRESS
        number_of_registers = settings.NUMBER_OF_REGISTERS

        data_list = []

        while True:
            if not devices:
                logging.warning("No devices available")
                time.sleep(10)
                continue

            for device_name, device_id in devices.items():
                registers = utils.read_registers(client, register_address, number_of_registers, device_id)

                if not registers or len(registers) != settings.NUMBER_OF_REGISTERS:
                    logging.error(f"Failed to read registers for device {device_name} (ID {device_id})")
                    continue

                float_value = utils.convert_to_float32(registers)
                timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

                device_data = {"timestamp": timestamp, "device": device_name, "amperage": float_value}

                data_list.append(device_data)
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                response = requests.post(url, json=data_list, headers=headers, verify=False)

                data_list = []

                if response.status_code == 200:  # noqa: PLR2004
                    print(f"{timestamp}, {response.json()}")
                    logging.info(f"{response.json()}")
                else:
                    print(f"{timestamp}, {response.status_code}: {response.text}")
                    logging.error(f"{response.status_code}, {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"Exception when sent: {e}")
                logging.error(f"Exception when sent: {e}")
    finally:
        if client:
            client.close()
            print("Modbus connection closed")
            logging.info("Modbus connection closed")

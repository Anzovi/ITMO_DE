import logging
import struct

import requests
from pymodbus.client import ModbusTcpClient


def connect_to_modbus(ip, port):
    """Создание подключения к Modbus-устройству."""
    client = ModbusTcpClient(ip, port=port, timeout=1)
    if client.connect():
        return client
    else:
        return None


def read_registers(client, register_address, number_of_registers, device_id):
    """Чтение регистров из Modbus-устройства."""
    try:
        response = client.read_input_registers(address=register_address, count=number_of_registers, slave=device_id)
        return response.registers
    except:  # noqa: E722
        return None


def convert_to_float32(registers):
    """Преобразование списка регистров в список float32."""
    if registers is not None:
        return struct.unpack(">f", struct.pack(">HH", *registers))[0]
    else:
        return 0.0


def fetch_devices(api_url, project_id, api_key):
    """Получение списка устройств из API Appwrite."""
    headers = {"X-Appwrite-Project": project_id, "X-Appwrite-Key": api_key, "Content-Type": "application/json"}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        devices = response.json()["documents"]
        logging.info("Devices fetched successfully")
        return {device["name"]: device["device_id"] for device in devices}
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch devices: {e}")
        return {}

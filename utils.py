from pymodbus.client import ModbusTcpClient # Для связи с Modbus драйвером
import struct # Для преобразования регистров в float переменные


def connect_to_modbus(ip, port):
    """Создание подключения к Modbus-устройству."""
    client = ModbusTcpClient(ip, port=port, timeout=1)
    if client.connect():
        print("Успешное подключение к устройству.")
        return client
    else:
        print("Не удалось подключиться к устройству.")
        return None


def read_registers(client, register_address, number_of_registers, device_id):
    """Чтение регистров из Modbus-устройства."""
    try:
        response = client.read_input_registers(
                                        address=register_address, 
                                        count=number_of_registers,
                                        slave=device_id)
        return response.registers
    except:
        return None


def convert_to_float32(registers):
    """Преобразование списка регистров в список float32."""
    if registers is not None:
        return struct.unpack('>f', struct.pack('>HH', *registers))[0]
    else:
        return 0.0

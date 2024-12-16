# Modbus Collector

> Модуль сбора данных с датчиков

## Развертывание  

Установка данного модуля производится непосредственно на ПК, который подключен к сенсорам через Modbus протокол/

1. Перейти в папку ModbusCollector  

```bash  
cd ../ModbusCollector  
```  

2. Установить Poetry. Используйте Poetry для установки всех зависимостей, указанных в pyproject.toml
```bash
poetry install
```  
3. Создайте файл .env по примеру env.example  

## Тестирование  
1. Запуск приложения  
```bash  
poetry run python main.py  
```  
2. Логирование:  
Проверьте файл data_transfer.log для мониторинга работы модуля  

# Инжиниринг управления данными
## Определение области проекта:

- Домен: Производство и техническое обслуживание оборудования.
- Конкретная бизнес-проблема: Автоматизация процесса диагностики состояния машин и оборудования с целью выявления отклонений от нормальных режимов работы и своевременного уведомления о необходимости проведения технического обслуживания. Это позволит снизить количество непредвиденных поломок, оптимизировать график обслуживания и, в конечном итоге, повысить эффективность работы оборудования.

Дополнительная информация о проекте содержится в [ML sys design document](https://github.com/Anzovi/ITMO_DE/blob/main/docs/ml_system_design_doc.md)  

## Детали для документации:
- Описание проекта: Проект направлен на разработку системы предиктивного технического обслуживания (ТО) с использованием методов машинного обучения для анализа данных, полученных с сенсоров оборудования. Система будет осуществлять мониторинг состояния оборудования в реальном времени и предсказывать необходимость проведения технического обслуживания на основе собранных данных.
- Цели проекта:
    - Обеспечение автоматизированного мониторинга состояния оборудования.
    - Выявление аномалий и прогнозирование необходимости ТО.
    - Оптимизация графиков ТО для снижения простоев оборудования.
- Методы и подходы:
    - Использование методов исследовательского анализа данных (EDA) для анализа собранных данных.
    - Применение алгоритмов машинного обучения для обнаружения аномалий и изменения точек состояния (определения разладок процесса).
    - Разработка MVP системы для тестирования и валидации подхода.

## Схема решения  
![](https://github.com/Anzovi/ITMO_DE/blob/main/imgs/UvelkaAPI.png)  

ETL процесс состоит из двух сегментов:
1. Сбор данных непосредственно с датчиков по протоколу Modbus и частичная обработка (ModbusCollector).
    - Через фреймворк PyModbus производится подключение и опрос доступных устройств. Затем считывание с регистров датчиков в формате двух 16-битных чисел. Эти числа преобразуются в одно 32-битное.
    - Снятые значения отправляются в виде json на API сервиса (analyzer).
2. Загрузка данных из сегмента (ModbusCollector) на сервер проекта через API (analyzer), затем передача данных в базу данных ClickHouse (clickhouse) через прокси Traefik.

## Пример данных:
| Timestamp           | Device                     | Amperage    |
|---------------------|----------------------------|-------------|
| 2024-12-01 0:00:01  | Токовый ремни Афл3.2      | 16.304153   |
| 2024-12-01 0:00:02  | Токовый ремни Афл3.3      | 3.9494066   |
| 2024-12-01 0:00:03  | Токовый нипроллер Афл3.3  | 0           |
| 2024-12-01 0:00:04  | Токовый губки Афл3.3      | 0           |
| 2024-12-01 0:00:05  | Токовый нипроллер Афл3.4  | 0           |
| 2024-12-01 0:00:06  | Токовый ремни Афл3.4      | 0           |
| 2024-12-01 0:00:08  | Токовый губки Афл3.4      | 0           |

Представлен sample данных в sensor_data.csv  

## Структура проекта
```
project_root/
│
├── ModbusCollector              # Модуль сбора данных с датчиков
├── analyzer                     # API для получения данных с датчиков и последующей обработки
├── clickhouse                   # База для хранения показаний датчиков
├── docs                         # Дизайн документ ML системы
├── imgs                         # Изображения для вставки
├── traefik                      # Прокси для управления доступом к сервисам ML Uvelka
├── dashboard-metabase           # Реализация BI dashboard на платформе Metabase
└── 
```
## Развертывание и тестирование 

Склонировать репозиторий
```bash
git clone https://github.com/Anzovi/ITMO_DE.git <directory>
```
Далее установка отдельных модулей содержится в соответствующих одноименных папках. 

## Дашборд и метрики качества данных
В качестве метрики качества данных принята доля значений, превышающих номинальное значение датчика (30 Ампер) (Датчик измеряет в диапазоне от 0 до 30 Ампер, все что выше - за пределом нормальной работы датчика) .
Ссылка на дашборд: https://datalens.yandex/2rcp6ry0fx0go

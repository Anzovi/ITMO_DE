from typing import Literal

import clickhouse_connect

from src.config import settings
from src.models.sensor_data import SensorData


def insert_sensor_data(data: list[SensorData]):
    client = clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_HOST,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
    )

    values = [(d.timestamp, d.device, d.amperage) for d in data]
    client.insert(table="sensor_data", data=values, column_names=["timestamp", "device", "amperage"])
    client.close()


def get_all_sensors_data(depth: Literal["second", "minute", "hour"], value: int, devices: list[str] | None = None):
    client = clickhouse_connect.get_client(
        host=settings.CLICKHOUSE_HOST,
        username=settings.CLICKHOUSE_USER,
        password=settings.CLICKHOUSE_PASSWORD,
    )

    devices_filter = ""
    if devices:
        devices_list = ", ".join([f"'{d}'" for d in devices])
        devices_filter = f"AND device IN ({devices_list})"

    query = f"""
            SELECT *
            FROM sensor_data
            WHERE timestamp >= toDateTime(toString(toTimeZone(now(), 'Asia/Yekaterinburg'))) - INTERVAL {value} {depth}
            {devices_filter}
            ORDER BY timestamp ASC
        """
    data = client.query(query).result_rows
    client.close()
    return {"data": [{"timestamp": row[0], "device": row[1], "amperage": row[2]} for row in data]}

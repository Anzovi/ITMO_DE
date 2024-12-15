import asyncio
import json
from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, WebSocket

from src.database.crud import get_all_sensors_data, insert_sensor_data
from src.models.sensor_data import SensorData
from src.utils.security import verify_api_key
from src.utils.ws_connection_manager import ConnectionManager

router = APIRouter(
    prefix="/data",
    tags=["Data"],
)


# Загрузить данные
@router.post("/upload", dependencies=[Depends(verify_api_key)])
async def upload_data(data: list[SensorData]):
    insert_sensor_data(data)
    return {"message": "Data successfully inserted into ClickHouse"}


# Данные для графиков мониторинга
@router.get("/monitoring")
def get_monitoring_data(depth: Literal["minute", "hour"], value: int, devices: str = Query(default=None)):
    # Ограничение на глубину
    max_interval = {"minute": 60, "hour": 24}
    if value > max_interval.get(depth, 1):
        raise HTTPException(status_code=400, detail=f"Max depth: {max_interval[depth]} {depth}")

    return get_all_sensors_data(depth, value, devices.split(","))


# Сокет для новых данных мониторинга
manager = ConnectionManager()


@router.websocket("/monitoring/ws")
async def get_monitoring_data_ws(websocket: WebSocket):
    client_key = str(websocket.client)
    await manager.connect(websocket)
    while manager.is_connected(client_key):
        data = get_all_sensors_data("second", 100)
        await manager.broadcast(json.dumps(data, ensure_ascii=False, default=str).encode("utf8").decode())
        await asyncio.sleep(10)

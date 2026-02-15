from celery import shared_task
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.nas_device import NASDevice
from app.models.nas_status_history import NASStatusHistory
from app.nas import MikrotikNAS, OpenWrtNAS, UbiquitiNAS
from app.core.config import settings
import asyncio
import socket
from datetime import datetime, timedelta

async def check_tcp_port(host: str, port: int, timeout: float = 5) -> bool:
    try:
        loop = asyncio.get_event_loop()
        fut = loop.create_connection(lambda: asyncio.Protocol(), host, port)
        await asyncio.wait_for(fut, timeout=timeout)
        return True
    except:
        return False

def get_nas_instance(device: NASDevice):
    if device.type == 'mikrotik':
        return MikrotikNAS(host=device.ip_address, username=device.api_username or '', password='', port=8728)
    elif device.type == 'openwrt':
        return OpenWrtNAS(host=device.ip_address, username=device.api_username or '', password='', port=22)
    elif device.type == 'ubiquiti':
        return UbiquitiNAS(host=device.ip_address, username=device.api_username or '', password='', port=8443)
    return None

@shared_task
def check_nas_devices():
    db = SessionLocal()
    try:
        devices = db.query(NASDevice).filter(
            NASDevice.is_active == True,
            NASDevice.deleted_at.is_(None)
        ).all()

        for device in devices:
            # Определяем, какой порт проверять в зависимости от типа
            if device.type == 'mikrotik':
                port = 8728
            elif device.type == 'openwrt':
                port = 22
            elif device.type == 'ubiquiti':
                port = 8443
            else:
                continue

            # Используем WireGuard IP, если он есть, иначе обычный IP
            target_ip = device.wireguard_ip or device.ip_address

            # Запускаем асинхронную проверку синхронно
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                reachable = loop.run_until_complete(check_tcp_port(target_ip, port))
            finally:
                loop.close()

            status = 'online' if reachable else 'offline'

            # Обновляем статус и last_seen
            device.last_check = datetime.utcnow()
            if reachable:
                device.last_seen = datetime.utcnow()
            device.status = status
            db.add(device)

            # Записываем историю
            history = NASStatusHistory(
                nas_device_id=device.id,
                status=status
            )
            db.add(history)

            db.commit()
    finally:
        db.close()
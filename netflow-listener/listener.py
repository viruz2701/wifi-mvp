import asyncio
import socket
import httpx
import os
import json

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/api/v1/netflow/records")

async def send_to_backend(record):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(BACKEND_URL, json=record, timeout=2)
            if resp.status_code != 200:
                print(f"Error sending flow: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Exception sending flow: {e}")

async def handle_flow_datagram(data, addr):
    # Заглушка: вместо парсинга отправляем тестовые данные
    print(f"Received {len(data)} bytes from {addr}")
    # Создаём фиктивную запись (в реальности здесь будет парсинг)
    record = {
        "src_ip": "192.168.1.1",
        "dst_ip": "10.0.0.1",
        "bytes": 1024,
        "packets": 1,
        "src_port": 12345,
        "dst_port": 80,
        "protocol": 6,
        "flow_start": None,
        "flow_end": None
    }
    asyncio.create_task(send_to_backend(record))

async def main():
    loop = asyncio.get_event_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        local_addr=('0.0.0.0', 20002)
    )
    print("NetFlow listener started on UDP port 20002 (mock mode)")
    while True:
        data, addr = await transport.recvfrom(65535)
        await handle_flow_datagram(data, addr)

if __name__ == "__main__":
    asyncio.run(main())
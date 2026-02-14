import asyncio
import socket
import struct
import json
import httpx
import os
from py_netflow import NetFlowV9Parser

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000/api/v1/netflow/records")

def parse_netflow_packet(data):
    """Парсит пакет NetFlow v9 и возвращает список записей."""
    parser = NetFlowV9Parser()
    flows = parser.parse(data)
    return flows

async def send_to_backend(flow):
    """Отправляет запись в backend."""
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(BACKEND_URL, json=flow, timeout=2)
            if resp.status_code != 200:
                print(f"Error sending flow: {resp.status_code} {resp.text}")
        except Exception as e:
            print(f"Exception sending flow: {e}")

async def handle_flow_datagram(data, addr):
    flows = parse_netflow_packet(data)
    for flow in flows:
        # Преобразуем в нужный формат (подгоняем под схему NetFlowRecordCreate)
        record = {
            "src_ip": flow.get("IPV4_SRC_ADDR"),
            "dst_ip": flow.get("IPV4_DST_ADDR"),
            "bytes": flow.get("IN_BYTES", 0),
            "packets": flow.get("IN_PKTS", 0),
            "src_port": flow.get("L4_SRC_PORT"),
            "dst_port": flow.get("L4_DST_PORT"),
            "protocol": flow.get("PROTOCOL"),
            "flow_start": flow.get("FIRST_SWITCHED"),
            "flow_end": flow.get("LAST_SWITCHED"),
            # session_id будет определен позже в backend
        }
        # Отправляем асинхронно
        asyncio.create_task(send_to_backend(record))

async def main():
    loop = asyncio.get_event_loop()
    transport, _ = await loop.create_datagram_endpoint(
        lambda: asyncio.DatagramProtocol(),
        local_addr=('0.0.0.0', 20002)
    )
    print("NetFlow listener started on UDP port 20002")
    while True:
        data, addr = await transport.recvfrom(65535)
        await handle_flow_datagram(data, addr)

if __name__ == "__main__":
    asyncio.run(main())
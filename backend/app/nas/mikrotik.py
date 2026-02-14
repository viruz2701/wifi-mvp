import librouteros
from .interface import NASInterface

class MikrotikNAS(NASInterface):
    def __init__(self, host: str, username: str, password: str, port: int = 8728):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.api = None

    async def connect(self):
        """Устанавливаем соединение (синхронное, но можно обернуть в поток)."""
        # librouteros синхронный, для асинхронности используем asyncio.to_thread
        import asyncio
        self.api = await asyncio.to_thread(
            librouteros.connect,
            host=self.host,
            username=self.username,
            password=self.password,
            port=self.port
        )

    async def get_client_name(self, mac: str) -> str | None:
        if not self.api:
            await self.connect()
        # Ищем в DHCP-сервере
        leases = await asyncio.to_thread(
            self.api, '/ip/dhcp-server/lease/print',
            {'?mac-address': mac}
        )
        if leases:
            return leases[0].get('host-name')
        return None

    async def disconnect_session(self, mac: str) -> bool:
        if not self.api:
            await self.connect()
        # Находим активное соединение и удаляем его (или отключаем)
        # Например, можно сбросить соединение через /ip/firewall/connection/remove
        connections = await asyncio.to_thread(
            self.api, '/ip/firewall/connection/print',
            {'?src-mac-address': mac}
        )
        if connections:
            for conn in connections:
                await asyncio.to_thread(self.api, '/ip/firewall/connection/remove', {
                    '.id': conn['.id']
                })
            return True
        return False
import asyncio
import asyncssh
from .interface import NASInterface

class OpenWrtNAS(NASInterface):
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.conn = None

    async def reboot(self) -> bool:
        """Перезагрузка устройства через SSH."""
        if not self.conn:
            await self.connect()
        try:
            result = await self.conn.run('reboot', check=False)
            return result.exit_status == 0
        except Exception as e:
            print(f"Reboot failed: {e}")
            return False

    async def disconnect_all_sessions(self) -> bool:
        """Завершить все сессии через CoovaChilli."""
        if not self.conn:
            await self.connect()
        try:
            # Вариант 1: через chilli_query
            result = await self.conn.run('chilli_query list | while read line; do mac=$(echo $line | cut -d" " -f1); chilli_query logout $mac; done', check=False)
            # Вариант 2: перезапуск службы chilli (более грубо)
            # result = await self.conn.run('/etc/init.d/chilli restart', check=False)
            return result.exit_status == 0
        except Exception as e:
            print(f"Disconnect all sessions failed: {e}")
            return False
        
    async def connect(self):
        self.conn = await asyncssh.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            known_hosts=None
        )

    async def get_client_name(self, mac: str) -> str | None:
        if not self.conn:
            await self.connect()
        # Читаем файл dhcp.leases
        result = await self.conn.run('cat /tmp/dhcp.leases')
        if result.exit_status == 0:
            for line in result.stdout.splitlines():
                parts = line.split()
                if len(parts) >= 2 and parts[1].upper() == mac.upper():
                    return parts[3] if len(parts) > 3 else None
        return None

    async def disconnect_session(self, mac: str) -> bool:
        if not self.conn:
            await self.connect()
        # Используем chilli_query для CoovaChilli
        result = await self.conn.run(f'chilli_query logout {mac}')
        return result.exit_status == 0
import asyncio
import asyncssh
from typing import Optional, Dict, Any
from .interface import NASInterface

class OpenWrtOpenNDS(NASInterface):
    """Управление OpenNDS на OpenWrt через SSH."""

    def __init__(self, host: str, username: str, password: str, port: int = 22, config: Dict[str, Any] = None):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.config = config or {}
        self.conn = None

    async def connect(self):
        self.conn = await asyncssh.connect(
            host=self.host,
            port=self.port,
            username=self.username,
            password=self.password,
            known_hosts=None
        )

    async def reboot(self) -> bool:
        if not self.conn:
            await self.connect()
        result = await self.conn.run('reboot', check=False)
        return result.exit_status == 0

    async def disconnect_all_sessions(self) -> bool:
        if not self.conn:
            await self.connect()
        result = await self.conn.run('/etc/init.d/opennds restart', check=False)
        return result.exit_status == 0

    async def configure_opennds(self, fashost: str, fasport: int = 443, faspath: str = '/portal/opennds') -> bool:
        """Настройка OpenNDS для работы с внешним FAS."""
        if not self.conn:
            await self.connect()

        # Читаем текущий конфиг
        result = await self.conn.run('cat /etc/config/opennds', check=False)
        config_lines = result.stdout.splitlines() if result.exit_status == 0 else []

        new_config = []
        for line in config_lines:
            if line.startswith("option fashost") or line.startswith("option fasport") or line.startswith("option faspath"):
                continue
            new_config.append(line)

        # Добавляем новые параметры после enabled
        if not any("option enabled 1" in line for line in new_config):
            new_config = [
                "config opennds",
                "        option enabled 1",
                f"        option fashost '{fashost}'",
                f"        option fasport '{fasport}'",
                f"        option faspath '{faspath}'",
                "        option dhcpstart 100",
                "        option dhcpend 200",
                "        option network 'lan'"
            ]
        else:
            # Вставляем после enabled
            for i, line in enumerate(new_config):
                if "option enabled 1" in line:
                    new_config.insert(i+1, f"        option fashost '{fashost}'")
                    new_config.insert(i+2, f"        option fasport '{fasport}'")
                    new_config.insert(i+3, f"        option faspath '{faspath}'")
                    break

        config_str = "\n".join(new_config)
        await self.conn.run(f"cat > /etc/config/opennds << 'EOF'\n{config_str}\nEOF", check=True)
        result = await self.conn.run('/etc/init.d/opennds restart', check=False)
        return result.exit_status == 0

    async def get_client_name(self, mac: str) -> Optional[str]:
        if not self.conn:
            await self.connect()
        result = await self.conn.run(f"cat /tmp/dhcp.leases | grep -i '{mac}'", check=False)
        if result.exit_status == 0:
            parts = result.stdout.split()
            return parts[3] if len(parts) >= 4 else None
        return None

    async def disconnect_session(self, mac: str) -> bool:
        if not self.conn:
            await self.connect()
        result = await self.conn.run(f"openndsctl logout {mac}", check=False)
        return result.exit_status == 0

    async def authorize_client(self, clientip: str, token: str) -> bool:
        """Открыть доступ клиенту после успешной авторизации."""
        if not self.conn:
            await self.connect()
        cmd = f'curl -s "http://localhost/opennds_auth/?tok={token}"'
        result = await self.conn.run(cmd, check=False)
        return result.exit_status == 0
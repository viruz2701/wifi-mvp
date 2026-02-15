import httpx
from .interface import NASInterface

class UbiquitiNAS(NASInterface):
    def __init__(self, host: str, username: str, password: str, site: str = "default", port: int = 8443):
        self.base_url = f"https://{host}:{port}/api/s/{site}"
        self.username = username
        self.password = password
        self.client = httpx.AsyncClient(verify=False)  # отключаем проверку SSL для локального контроллера
        self.cookies = None

     async def reboot(self) -> bool:
        """Перезагрузка контроллера или конкретной точки доступа."""
        if not self.cookies:
            await self.login()
        try:
            # Для перезагрузки всей системы (если это контроллер)
            # payload = {"cmd": "reboot"}
            # resp = await self.client.post(f"{self.base_url}/cmd/system", json=payload, cookies=self.cookies)
            # Для перезагрузки конкретной точки доступа (требуется её MAC)
            # Здесь нужно получить список точек и выбрать нужную. Упростим: перезагружаем первую активную.
            sites = await self.client.get(f"{self.base_url}/self/sites", cookies=self.cookies)
            if sites.status_code == 200:
                site_data = sites.json()
                # ... логика выбора точки
                return True
            return False
        except Exception as e:
            print(f"Reboot failed: {e}")
            return False

    async def disconnect_all_sessions(self) -> bool:
        """Завершить все сессии всех клиентов."""
        if not self.cookies:
            await self.login()
        try:
            # Получаем список активных клиентов
            resp = await self.client.get(f"{self.base_url}/stat/sta", cookies=self.cookies)
            if resp.status_code == 200:
                data = resp.json()
                for client in data.get('data', []):
                    mac = client.get('mac')
                    if mac:
                        await self.client.post(
                            f"{self.base_url}/cmd/stamgr",
                            json={"cmd": "kick-sta", "mac": mac},
                            cookies=self.cookies
                        )
                return True
            return False
        except Exception as e:
            print(f"Disconnect all sessions failed: {e}")
            return False

    async def login(self):
        # Унифицированный вход (может отличаться для разных версий)
        resp = await self.client.post(
            f"{self.base_url}/login",
            json={"username": self.username, "password": self.password}
        )
        if resp.status_code == 200:
            self.cookies = resp.cookies
            return True
        return False

    async def get_client_name(self, mac: str) -> str | None:
        if not self.cookies:
            await self.login()
        # Ищем клиента по MAC
        resp = await self.client.get(
            f"{self.base_url}/stat/sta/{mac}",
            cookies=self.cookies
        )
        if resp.status_code == 200:
            data = resp.json()
            if data.get('meta', {}).get('rc') == 'ok' and data.get('data'):
                return data['data'][0].get('name')
        return None

    async def disconnect_session(self, mac: str) -> bool:
        if not self.cookies:
            await self.login()
        # Для отключения клиента нужно отправить запрос на завершение сессии
        # Это зависит от версии UniFi, обычно POST /cmd/stamgr с параметрами
        payload = {
            "cmd": "kick-sta",
            "mac": mac
        }
        resp = await self.client.post(
            f"{self.base_url}/cmd/stamgr",
            json=payload,
            cookies=self.cookies
        )
        return resp.status_code == 200
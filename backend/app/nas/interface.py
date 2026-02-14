from abc import ABC, abstractmethod

class NASInterface(ABC):
    """Абстрактный класс для взаимодействия с NAS."""

    @abstractmethod
    async def get_client_name(self, mac: str) -> str | None:
        """Получить имя клиента по MAC (например, из DHCP leases)."""
        pass

    @abstractmethod
    async def disconnect_session(self, mac: str) -> bool:
        """Принудительно разорвать сессию клиента."""
        pass
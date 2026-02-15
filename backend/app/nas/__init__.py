from .mikrotik import MikrotikNAS
from .openwrt import OpenWrtNAS
from .ubiquiti import UbiquitiNAS
from app.core.security import decrypt_secret

__all__ = ["MikrotikNAS", "OpenWrtNAS", "UbiquitiNAS", "get_nas_instance"]

def get_nas_instance(device):
    """
    Возвращает экземпляр класса NAS в зависимости от типа устройства.
    :param device: объект NASDevice (из базы данных)
    :return: экземпляр одного из классов NAS
    """
    # Расшифровываем пароль, если он есть
    api_password = None
    if device.api_password:
        api_password = decrypt_secret(device.api_password)

    if device.type == 'mikrotik':
        return MikrotikNAS(
            host=device.ip_address,
            username=device.api_username or '',
            password=api_password or '',
            port=8728
        )
    elif device.type == 'openwrt':
        return OpenWrtNAS(
            host=device.ip_address,
            username=device.api_username or '',
            password=api_password or '',
            port=22
        )
    elif device.type == 'ubiquiti':
        return UbiquitiNAS(
            host=device.ip_address,
            username=device.api_username or '',
            password=api_password or '',
            port=8443
        )
    else:
        raise ValueError(f"Unsupported NAS type: {device.type}")
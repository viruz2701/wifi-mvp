from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.nas_device import NASDevice
from app.schemas.nas_device import NASDeviceCreate, NASDeviceUpdate
from app.core.security import encrypt_secret, decrypt_secret
from app.core.wireguard import generate_keypair  # функция будет в core/wireguard.py
from typing import Any, Dict
import subprocess

def generate_keypair() -> tuple[str, str]:
    """Генерирует пару ключей WireGuard. Возвращает (private_key, public_key)."""
    private = subprocess.check_output(["wg", "genkey"]).decode().strip()
    public = subprocess.check_output(["wg", "pubkey"], input=private.encode()).decode().strip()
    return private, public

class CRUDNASDevice(CRUDBase[NASDevice, NASDeviceCreate, NASDeviceUpdate]):
    def create(self, db: Session, *, obj_in: NASDeviceCreate) -> NASDevice:
        obj_in_data = obj_in.model_dump()
        # Шифруем секреты
        obj_in_data['secret'] = encrypt_secret(obj_in_data.pop('secret'))
        if obj_in_data.get('api_password'):
            obj_in_data['api_password'] = encrypt_secret(obj_in_data['api_password'])
        
        # Генерация WireGuard ключей
        generate_keys = obj_in_data.pop('generate_wireguard_keys', False)
        if generate_keys:
            priv, pub = generate_keypair()
            obj_in_data['wireguard_private_key'] = encrypt_secret(priv)
            obj_in_data['wireguard_pubkey'] = pub
            obj_in_data['wireguard_generated'] = True
        else:
            obj_in_data['wireguard_generated'] = False
        
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: NASDevice, obj_in: NASDeviceUpdate | Dict[str, Any]) -> NASDevice:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        # Если передан secret, шифруем
        if 'secret' in update_data and update_data['secret']:
            update_data['secret'] = encrypt_secret(update_data['secret'])
        if 'api_password' in update_data and update_data['api_password']:
            update_data['api_password'] = encrypt_secret(update_data['api_password'])
        
        # Обработка генерации ключей
        if update_data.get('generate_wireguard_keys'):
            priv, pub = generate_keypair()
            update_data['wireguard_private_key'] = encrypt_secret(priv)
            update_data['wireguard_pubkey'] = pub
            update_data['wireguard_generated'] = True
        # В любом случае удаляем служебный флаг, чтобы не пытаться записать его в модель
        update_data.pop('generate_wireguard_keys', None)

        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

nas_device = CRUDNASDevice(NASDevice)
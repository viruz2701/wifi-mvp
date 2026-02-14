from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.nas_device import NASDevice
from app.schemas.nas_device import NASDeviceCreate, NASDeviceUpdate
from app.core.security import encrypt_secret
from typing import Any, Dict

class CRUDNASDevice(CRUDBase[NASDevice, NASDeviceCreate, NASDeviceUpdate]):
    def create(self, db: Session, *, obj_in: NASDeviceCreate) -> NASDevice:
        obj_in_data = obj_in.model_dump()
        # Шифруем секреты
        obj_in_data['secret'] = encrypt_secret(obj_in_data.pop('secret'))
        if obj_in_data.get('api_password'):
            obj_in_data['api_password'] = encrypt_secret(obj_in_data['api_password'])
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
        # Если переданы секреты, шифруем
        if 'secret' in update_data and update_data['secret']:
            update_data['secret'] = encrypt_secret(update_data['secret'])
        if 'api_password' in update_data and update_data['api_password']:
            update_data['api_password'] = encrypt_secret(update_data['api_password'])
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

nas_device = CRUDNASDevice(NASDevice)
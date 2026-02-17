from app.crud.base import CRUDBase
from app.models.setting import Setting
from app.schemas.setting import SettingCreate, SettingUpdate

class CRUDSetting(CRUDBase[Setting, SettingCreate, SettingUpdate]):
    def get_by_key(self, db, key: str):
        return db.query(self.model).filter(self.model.key == key).first()

setting = CRUDSetting(Setting)
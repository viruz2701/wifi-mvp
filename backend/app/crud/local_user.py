from sqlalchemy.orm import Session as DbSession
from app.crud.base import CRUDBase
from app.models.local_user import LocalUser
from app.schemas.local_user import LocalUserCreate, LocalUserUpdate
from app.core.security import get_password_hash

class CRUDLocalUser(CRUDBase[LocalUser, LocalUserCreate, LocalUserUpdate]):
    def get_by_username(self, db: DbSession, username: str, venue_id: int):
        return db.query(self.model).filter(
            self.model.username == username,
            self.model.venue_id == venue_id,
            self.model.deleted_at.is_(None)
        ).first()

    def create(self, db: DbSession, *, obj_in: LocalUserCreate) -> LocalUser:
        obj_in_data = obj_in.model_dump()
        password = obj_in_data.pop("password")
        obj_in_data["password_hash"] = get_password_hash(password)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: DbSession, *, db_obj: LocalUser, obj_in: LocalUserUpdate):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            update_data["password_hash"] = get_password_hash(update_data.pop("password"))
        return super().update(db, db_obj=db_obj, obj_in=update_data)

local_user = CRUDLocalUser(LocalUser)
from app.crud.base import CRUDBase
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileUpdate

class CRUDUserProfile(CRUDBase[UserProfile, UserProfileCreate, UserProfileUpdate]):
    def get_by_mac(self, db, mac: str):
        return db.query(self.model).filter(self.model.mac_address == mac).first()

user_profile = CRUDUserProfile(UserProfile)
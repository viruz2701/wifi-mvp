from app.crud.base import CRUDBase
from app.models.user_social_action import UserSocialAction
from app.schemas.user_social_action import UserSocialActionCreate, UserSocialActionUpdate

class CRUDUserSocialAction(CRUDBase[UserSocialAction, UserSocialActionCreate, UserSocialActionUpdate]):
    def get_by_user_and_action(self, db, user_profile_id: int, action_id: int):
        return db.query(self.model).filter(
            self.model.user_profile_id == user_profile_id,
            self.model.action_id == action_id
        ).first()

user_social_action = CRUDUserSocialAction(UserSocialAction)
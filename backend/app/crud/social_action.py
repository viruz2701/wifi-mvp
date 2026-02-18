from app.crud.base import CRUDBase
from app.models.social_action import SocialAction
from app.schemas.social_action import SocialActionCreate, SocialActionUpdate

class CRUDSocialAction(CRUDBase[SocialAction, SocialActionCreate, SocialActionUpdate]):
    def get_active_by_network(self, db, network):
        return db.query(self.model).filter(
            self.model.network == network,
            self.model.is_active == True
        ).all()

social_action = CRUDSocialAction(SocialAction)
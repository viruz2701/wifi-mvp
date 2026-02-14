from app.crud.base import CRUDBase
from app.models.banner import Banner
from app.schemas.banner import BannerCreate, BannerUpdate

class CRUDBanner(CRUDBase[Banner, BannerCreate, BannerUpdate]):
    pass

banner = CRUDBanner(Banner)
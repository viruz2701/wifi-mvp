from .base import Base
from .user import User
from .venue import Venue
from .nas_device import NASDevice
from .user_profile import UserProfile
from .session import Session
from .local_user import LocalUser
from .sms_code import SMSCode
from .sms_provider import SMSProvider
from .netflow_record import NetFlowRecord
from .wireguard_peer import WireGuardPeer
from .portal_template import PortalTemplate
from .event import Event
from .banner import Banner
from .nas_status_history import NASStatusHistory      # новая модель
from .audit_log import AuditLog                        # новая модель
from .radius_attribute import RadiusAttribute
from .tariff_radius_attribute import TariffRadiusAttribute
from .crm_provider import CRMProvider
from .tariff import TariffPlan
from .venue_crm import VenueCRM
from .setting import Setting
from .social_action import SocialAction
from .user_social_action import UserSocialAction
from .venue_social_action import VenueSocialAction



__all__ = [
    "Base",
    "User",

    "SocialAction",
    "UserSocialAction",
    "VenueSocialAction",


    "Venue",
    "NASDevice",
    "UserProfile",
    "Session",
    "LocalUser",
    "SMSCode",
    "SMSProvider",
    "NetFlowRecord",
    "WireGuardPeer",
    "PortalTemplate",
    "Event",
    "Banner",
    "NASStatusHistory",   # добавить сюда
    "AuditLog",           # добавить сюда
    "RadiusAttribute",
    "TariffRadiusAttribute",
    "CRMProvider",
    "TariffPlan",
    "VenueCRM",
    "Setting",
]

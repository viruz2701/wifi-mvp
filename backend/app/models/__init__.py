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
from .event import Event          # новая модель
from .banner import Banner        # новая модель

__all__ = [
    "Base",
    "User",
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
]
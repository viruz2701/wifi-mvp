from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
import logging
from app.models.social_action import SocialAction, SocialNetwork

logger = logging.getLogger(__name__)

class SocialProviderBase(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @abstractmethod
    async def verify(self, user_id: str, **kwargs) -> bool:
        """Проверяет, выполнил ли пользователь действие."""
        pass

class VKAdapter(SocialProviderBase):
    async def verify(self, user_id: str, **kwargs) -> bool:
        group_id = self.config.get("group_id")
        access_token = self.config.get("access_token")
        if not group_id or not access_token:
            logger.error("VK: missing group_id or access_token")
            return False
        # Проверка подписки через VK API
        url = "https://api.vk.com/method/groups.isMember"
        params = {
            "group_id": group_id,
            "user_id": user_id,
            "access_token": access_token,
            "v": "5.131"
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                if "error" in data:
                    logger.error(f"VK API error: {data['error']}")
                    return False
                return data.get("response", 0) == 1
            except Exception as e:
                logger.exception(f"VK exception: {e}")
                return False

class TelegramAdapter(SocialProviderBase):
    async def verify(self, user_id: str, **kwargs) -> bool:
        # user_id - это chat_id пользователя в Telegram
        channel_id = self.config.get("channel_id")
        bot_token = self.config.get("bot_token")
        if not channel_id or not bot_token:
            logger.error("Telegram: missing channel_id or bot_token")
            return False
        # Проверка через бота: может ли бот получить информацию о пользователе в канале?
        # Обычно бот должен быть администратором канала, чтобы получать список подписчиков.
        # Альтернатива: просить пользователя подписаться и затем отправлять команду боту.
        # Упростим: будем считать, что пользователь нажал кнопку и сообщил боту свой chat_id, а бот проверит членство.
        # Здесь мы можем вызвать метод getChatMember
        url = f"https://api.telegram.org/bot{bot_token}/getChatMember"
        params = {
            "chat_id": channel_id,
            "user_id": user_id
        }
        async with httpx.AsyncClient() as client:
            try:
                resp = await client.get(url, params=params)
                resp.raise_for_status()
                data = resp.json()
                if not data.get("ok"):
                    logger.error(f"Telegram error: {data}")
                    return False
                status = data["result"]["status"]
                return status in ["creator", "administrator", "member"]
            except Exception as e:
                logger.exception(f"Telegram exception: {e}")
                return False

class ViberAdapter(SocialProviderBase):
    async def verify(self, user_id: str, **kwargs) -> bool:
        # user_id - это идентификатор пользователя в Viber (обычно полученный от бота)
        bot_token = self.config.get("bot_token")
        if not bot_token:
            logger.error("Viber: missing bot_token")
            return False
        # Для проверки подписки на публичный аккаунт используем метод get_account_info?
        # Viber API: https://developers.viber.com/docs/api/rest-bot-api/#get-account-info
        # Но он возвращает информацию о боте, не о подписчике.
        # Чтобы проверить, подписан ли пользователь, нужно, чтобы пользователь отправил сообщение боту,
        # тогда мы получим его ID. Затем можно проверить, что пользователь есть в списке подписчиков?
        # В Viber нет прямого метода проверки подписки. Обычно проверяют, что бот может отправить сообщение пользователю.
        # Альтернатива: мы можем считать, что если пользователь нажал кнопку и перешёл по ссылке, то он подписался.
        # Упростим: будем всегда возвращать true, так как проверка сложна.
        # Но для демо можно сделать заглушку.
        logger.warning("Viber verification not fully implemented, returning True")
        return True

class InstagramAdapter(SocialProviderBase):
    async def verify(self, user_id: str, **kwargs) -> bool:
        # Заглушка
        logger.warning("Instagram verification not implemented")
        return True

class FacebookAdapter(SocialProviderBase):
    async def verify(self, user_id: str, **kwargs) -> bool:
        # Заглушка
        logger.warning("Facebook verification not implemented")
        return True

def get_social_adapter(action: SocialAction) -> SocialProviderBase:
    if action.network == SocialNetwork.VK:
        return VKAdapter(action.config)
    elif action.network == SocialNetwork.TELEGRAM:
        return TelegramAdapter(action.config)
    elif action.network == SocialNetwork.VIBER:
        return ViberAdapter(action.config)
    elif action.network == SocialNetwork.INSTAGRAM:
        return InstagramAdapter(action.config)
    elif action.network == SocialNetwork.FACEBOOK:
        return FacebookAdapter(action.config)
    else:
        raise ValueError(f"Unsupported network: {action.network}")
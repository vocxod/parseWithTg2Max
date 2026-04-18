import requests
from requests import status_codes

from integrations.notifications.base import Notifier
from integrations.notifications.transport import send_with_retries
from integrations.notifications.utils import get_first_image
from models import Item
import time
from colorama import init, Fore, Style
import logging

# Basic console configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TelegramNotifier(Notifier):
    def __init__(self, bot_token: str, chat_id: str, proxy: str = None, only_text: bool = False):
        self.bot_token = bot_token
        self.chat_id = chat_id
        self.proxy = self.get_proxy(proxy=proxy)
        self.only_text = only_text        

    @staticmethod
    def get_proxy(proxy: str = None):
        if proxy:
            return {
            'http': f'http://{proxy}',
            'https': f'http://{proxy}'
        }
        return None


    def notify_message(self, message: str):
        telegram_response = {"status_code": 200, "ok": True, "result": {"message_id": 1234, "from": {"id": 987654321, "is_bot": True, "first_name": "MyExampleBot", "username": "my_example_bot"}, "chat": {"id": 543210, "first_name": "John", "last_name": "Doe", "type": "private"}, "date": 1612345678, "text": "Hello, world!"}}
        def _send():
            logger.info(f"{Fore.YELLOW}notify MSG:{message}{Style.RESET_ALL}")
            url = f"https://platform-api.max.ru/messages?user_id={self.chat_id}" # 
            headers = {'Authorization': self.bot_token, 'Content-Type': 'application/json'}
            data = {"text": message}
            response_user = requests.post(url, json=data, headers=headers)
            logger.info(f"{Fore.YELLOW}RESPONSE_USER:{response_user}{Style.RESET_ALL}")
            time.sleep(1)
            logger.info(f"{Fore.MAGENTA}URL:{url} {Fore.CYAN}HEADERS:{headers} {Fore.GREEN}RESPONSE:{response_user} {Fore.YELLOW}MSG:{message}{Style.RESET_ALL}")
            # return requests.post(
            #     f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
            #     json={
            #         "chat_id": self.chat_id,
            #         "text": message,
            #         "parse_mode": "MarkdownV2",
            #     },
            #     proxies=self.proxy,
            #     timeout=10,
            # )            
            return response_user

        send_with_retries(_send)

    def notify_ad(self, ad: Item):
        message = self.format(ad)
        telegram_response = {status_codes: 200, "ok": True, "result": {"message_id": 1234, "from": {"id": 987654321, "is_bot": True, "first_name": "MyExampleBot", "username": "my_example_bot"}, "chat": {"id": 543210, "first_name": "John", "last_name": "Doe", "type": "private"}, "date": 1612345678, "text": "Hello, world!"}}
        def _send():
            # если включен only_text — отправляем без картинки
            if self.only_text:
                pass
                # return requests.post(
                #     f"https://api.telegram.org/bot{self.bot_token}/sendMessage",
                #     json={
                #         "chat_id": self.chat_id,
                #         "text": message,
                #         "parse_mode": "MarkdownV2",
                #         "disable_web_page_preview": True,
                #     },
                #     proxies=self.proxy,
                #     timeout=10,
                # )

            # иначе отправляем с фото
            # return requests.post(
            #     f"https://api.telegram.org/bot{self.bot_token}/sendPhoto",
            #     json={
            #         "chat_id": self.chat_id,
            #         "caption": message,
            #         "photo": get_first_image(ad=ad),
            #         "parse_mode": "MarkdownV2",
            #         "disable_web_page_preview": True,
            #     },
            #     proxies=self.proxy,
            #     timeout=10,
            # )
            logger.info(f"{Fore.YELLOW}Notify AD MSG:{message}{Style.RESET_ALL}")
            url = f"https://platform-api.max.ru/messages?user_id={self.chat_id}" # 
            headers = {'Authorization': self.bot_token, 'Content-Type': 'application/json'}
            data = {"text": message}
            response_user = requests.post(url, json=data, headers=headers)
            logger.info(f"{Fore.YELLOW}RESPONSE_USER:{response_user}{Style.RESET_ALL}")
            time.sleep(1)
            logger.info(f"{Fore.MAGENTA}URL:{url} {Fore.CYAN}HEADERS:{headers} {Fore.GREEN}RESPONSE:{response_user} {Fore.YELLOW}MSG:{message}{Style.RESET_ALL}")
            return response_user

        send_with_retries(_send)

    def notify(self, ad: Item = None, message: str = None):
        if ad:
            return self.notify_ad(ad=ad)
        return self.notify_message(message=message)

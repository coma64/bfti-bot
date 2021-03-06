from os import getenv
from types import SimpleNamespace
from typing import List

from dotenv import load_dotenv


class ConfigError(Exception):
    def __init__(self, missing_key: str) -> None:
        self.missing_key = missing_key

    def __str__(self):
        return f"Environment variable '{self.missing_key}' doesn't exist"


class Config(SimpleNamespace):
    """Read only config class loading values from .env and environment"""

    def __init__(self):
        self.token: str = self._getenv_or_throw('BOT_TOKEN', '')
        self.prefix: str = self._getenv_or_throw('BOT_PREFIX', '-')
        self.moderation_roles: List[int] = [
            int(role_id)
            for role_id in self._getenv_or_throw('MODERATION_ROLES').split(',')
        ]
        self.teacher_role: int = int(self._getenv_or_throw('TEACHER_ROLE_ID'))
        self.guild_id: int = int(self._getenv_or_throw('GUILD_ID'))
        self.channel_id: int = int(self._getenv_or_throw('CHANNEL_ID'))
        self.mail_channel_id: int = int(self._getenv_or_throw('MAIL_CHANNEL_ID'))
        self.calendar_channel_id: int = int(self._getenv_or_throw('CALENDAR_CHANNEL_ID'))

        self.iserv_hostname: str = self._getenv_or_throw('ISERV_HOSTNAME')
        self.iserv_username: str = self._getenv_or_throw('ISERV_USERNAME')
        self.iserv_password: str = self._getenv_or_throw('ISERV_PASSWORD')
        self.target_mail: str = self._getenv_or_throw('TARGET_MAIL')

        self.debug: bool = self._getenv_or_throw('DEBUG', 'true') != 'false'

    def _getenv_or_throw(self, key: str, default: str = None) -> str:
        value = getenv(key)

        if value == None:
            if default != None:
                return default
            else:
                raise ConfigError(key)

        return value


load_dotenv()
config = Config()

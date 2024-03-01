from typing import Optional

from nonebot import get_plugin_config
from pydantic import BaseModel


class Config(BaseModel):
    http_proxy: Optional[str] = None


emoji_config = get_plugin_config(Config)

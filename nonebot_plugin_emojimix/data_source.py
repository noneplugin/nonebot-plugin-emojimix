import httpx
import traceback
from typing import Union, Optional
from nonebot import get_driver
from nonebot.log import logger

from .emoji import emojis, EmojiData

global_config = get_driver().config
proxy = global_config.http_proxy
httpx_proxy = {
    'http://': global_config.http_proxy,
    'https://': global_config.http_proxy
}


API = 'https://www.gstatic.com/android/keyboard/emojikitchen/'


def create_url(emoji1: EmojiData, emoji2: EmojiData) -> str:
    def emoji_code(emoji: EmojiData):
        return '-'.join(map(lambda c: f'u{c:x}', emoji[0]))

    u1 = emoji_code(emoji1)
    u2 = emoji_code(emoji2)
    return f'{API}{emoji1[2]}/{u1}/{u1}_{u2}.png'


def find_emoji(emoji_code: str) -> Optional[EmojiData]:
    emoji_num = ord(emoji_code)
    for e in emojis:
        if emoji_num in e[0]:
            return e
    return None


async def mix_emoji(emoji_code1: str, emoji_code2: str) -> Union[str, bytes]:
    emoji1 = find_emoji(emoji_code1)
    emoji2 = find_emoji(emoji_code2)
    if not emoji1:
        return f'不支持的emoji：{emoji_code1}'
    if not emoji2:
        return f'不支持的emoji：{emoji_code2}'

    url1 = create_url(emoji1, emoji2)
    url2 = create_url(emoji2, emoji1)
    logger.info(url1)
    logger.info(url2)
    try:
        async with httpx.AsyncClient(proxies=httpx_proxy, timeout=10) as client:
            resp = await client.get(url1)
            if resp.status_code == 200:
                return resp.content
            resp = await client.get(url2)
            if resp.status_code == 200:
                return resp.content
            return '出错了，可能不支持该emoji组合'
    except:
        logger.warning(traceback.format_exc())
        return '下载出错，请稍后再试'

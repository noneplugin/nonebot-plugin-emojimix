import re

import emoji
from nonebot import on_message, require
from nonebot.matcher import Matcher
from nonebot.params import EventPlainText
from nonebot.plugin import PluginMetadata, inherit_supported_adapters
from nonebot.typing import T_State

require("nonebot_plugin_alconna")

from nonebot_plugin_alconna import UniMessage

from .config import Config
from .data_source import mix_emoji

__plugin_meta__ = PluginMetadata(
    name="emoji合成",
    description="将两个emoji合成为一张图片",
    usage="{emoji1}+{emoji2}，如：😎+😁",
    type="application",
    homepage="https://github.com/noneplugin/nonebot-plugin-emojimix",
    config=Config,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={
        "example": "😎+😁",
    },
)


emojis = filter(lambda e: len(e) == 1, emoji.EMOJI_DATA.keys())
emoji_pattern = "(" + "|".join(re.escape(e) for e in emojis) + ")"
pattern = re.compile(
    rf"^\s*(?P<code1>{emoji_pattern})\s*\+\s*(?P<code2>{emoji_pattern})\s*$"
)


async def check_eomjis(state: T_State, text: str = EventPlainText()) -> bool:
    text = text.strip()
    if not text or "+" not in text:
        return False
    if matched := re.match(pattern, text):
        state["code1"] = matched.group("code1")
        state["code2"] = matched.group("code2")
        return True
    return False


emojimix = on_message(check_eomjis, block=True, priority=13)


@emojimix.handle()
async def _(state: T_State, matcher: Matcher):
    emoji_code1 = state["code1"]
    emoji_code2 = state["code2"]

    result = await mix_emoji(emoji_code1, emoji_code2)

    if isinstance(result, str):
        await matcher.finish(result)

    await UniMessage.image(raw=result).send()

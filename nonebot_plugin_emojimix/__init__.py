from nonebot import on_regex
from nonebot.params import RegexDict
from nonebot.adapters.onebot.v11 import MessageSegment

from .data_source import mix_emoji

pattern = '[\u200d-\U0001fab5]'
emojimix = on_regex(rf'^(?P<code1>{pattern})\s*\+\s*(?P<code2>{pattern})$',
                    block=True, priority=13)


@emojimix.handle()
async def _(msg: dict = RegexDict()):
    emoji_code1 = msg['code1']
    emoji_code2 = msg['code2']
    result = await mix_emoji(emoji_code1, emoji_code2)
    if isinstance(result, str):
        await emojimix.finish(result)
    else:
        await emojimix.finish(MessageSegment.image(result))

#   encoding: utf-8

import asyncio

from gbf.events.times.cycle5 import cycle5
from gbf.events.times.cycle10 import cycle10


def init(bot):

    @bot.event
    async def on_ready():
        """
        イベントの初期化処理
        """
        print("グラブル周期botを起動します")
        asyncio.ensure_future(cycle5(bot))
        asyncio.ensure_future(cycle10(bot))

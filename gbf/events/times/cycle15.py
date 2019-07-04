#   encoding: utf-8
import os
from gbf.events.times.t_event import times_event


def init(bot):

    _id = int(os.environ["GBF_BOT_CYCLE_CH"])

    @times_event(client=bot, wait=15, ch_id=_id)
    async def cycle15event(client, ch):
        await ch.send('15秒毎の処理です')

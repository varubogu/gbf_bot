#   encoding: utf-8
import asyncio

ch_id = -1


async def cycle10(bot):
    """
    周期処理
    """
    print("shedule.cycle2 s")

    # チャンネル名「botテストとか」
    ch = bot.get_channel(ch_id)
    print(ch)

    if ch is not None:
        while True:
            await ch.send('10秒毎の処理です')
            await asyncio.sleep(10)

    else:
        err_msg = "Error chが見つかりません。"
        print(err_msg)
        Exception(err_msg)

    print("shedule.cycle2 e")

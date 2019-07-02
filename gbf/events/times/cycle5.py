#   encoding: utf-8
import asyncio

ch_id = -1


async def cycle5(bot):
    """
    周期処理
    """
    print("shedule.cycle s")

    # チャンネル名「botテストとか」
    ch = bot.get_channel(ch_id)
    print(ch)

    if ch is not None:
        while True:
            await ch.send('5秒毎の処理です')
            await asyncio.sleep(5)

    else:
        err_msg = "Error chが見つかりません。"
        print(err_msg)
        Exception(err_msg)

    print("shedule.cycle e")

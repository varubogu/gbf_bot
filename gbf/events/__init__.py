#   encoding: utf-8

import gbf.commands
import gbf.events.times


def init(bot):
    """
    グランブルーファンタジーBotの初期化を行う

    :param bot: discordのBotオブジェクト

    """
    print("times.init() s")
    times.init(bot)
    print("times.init() e")

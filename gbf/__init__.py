#   encoding: utf-8

from gbf import commands, events


def init(bot):
    """
    グランブルーファンタジーBotの初期化を行う

    :param bot: discordのBotオブジェクト

    """
    print("commands.init() s")
    commands.init(bot)
    print("commands.init() e")

    print("events.init() s")
    events.init(bot)
    print("events.init() e")

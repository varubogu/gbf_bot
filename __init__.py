#   encoding: utf-8

import os
from discord.ext import commands

import gbf
import prefix
import logging


def init():
    """
    discordのbotの初期化を行います。
    この関数以外ではdiscordのインスタンスを生成しないでください。
    また、複数回呼び出さないでください。

    """

    bot = commands.Bot(command_prefix=prefix.get())

    gbf.init(bot)

    logging.debug("debug on")
    bot.run(os.environ["GBF_BOT_TOKEN"])


init()

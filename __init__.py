#   encoding: utf-8

import os
from discord.ext import commands
from discord.ext.commands import Bot

import gbf
import prefix

# グローバル変数宣言
# 各所でbotはこの変数のみを使用してください。
g_bot: Bot = commands.Bot(command_prefix=prefix.get())

# 子モジュールの初期化
gbf.init(g_bot)

g_bot.run(os.environ["GBF_BOT_TOKEN"])

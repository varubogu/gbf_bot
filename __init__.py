#   encoding: utf-8

# グローバル変数宣言
# 各所でbot変数はこの変数のみを使用してください。
# また、取得する際は必ず
from discord.ext import commands
from discord.ext.commands import Bot

from command_prefix import get_prefix

from gbf.command.hello import call_hello
from gbf.__init__ import init2
from my_token import get_token

g_bot: Bot = commands.Bot(command_prefix=get_prefix())


# グローバル変数宣言
# 各所でbotはこの変数のみを使用してください。
async def get_bot() -> Bot:
    return g_bot


@g_bot.command(name="hello3")
async def _hello(ctx):
    await call_hello(ctx)

init2(g_bot)


g_bot.run(get_token())
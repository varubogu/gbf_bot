#   encoding: utf-8

from __init__ import g_bot
from gbf.command.hello import hello


@g_bot.command(name="hello")
async def _hello(ctx):
    await hello(ctx)

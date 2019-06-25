#   encoding: utf-8

from gbf.command.hello import call_hello, init


def init2(__bot):
    print("init2 -> hello2作成")
    init(__bot)

    @__bot.command(name="hello2")
    async def _hello2(ctx):
        await call_hello(ctx)



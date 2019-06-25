#   encoding: utf-8


async def call_hello(ctx):
    await __hello3(ctx)


async def __hello3(ctx):
    name = ctx.message.author.name
    msg = f"Hallo! 3  {name}\n" + __ax()
    await ctx.send(msg)


def __ax() -> str:
    print("a")
    return "おっすおっす"


def init(bot):

    @bot.command(name="hello")
    async def hello(ctx):
        await __hello(ctx)

    async def __hello(ctx):
        name = ctx.message.author.name
        msg = f"Hello! {name}\n" + __ax()
        await ctx.send(msg)

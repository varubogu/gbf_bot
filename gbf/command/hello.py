#   encoding: utf-8


async def hello(ctx):
    await __hello(ctx)


async def __hello(ctx):
    name = ctx.message.author.name
    msg = f"Hallo! {name}\n" + __ax()
    await ctx.send(msg)


def __ax() -> str:
    print("a")
    return "おっすおっす"

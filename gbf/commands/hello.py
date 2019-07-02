#   encoding: utf-8


def init(bot):

    @bot.command()
    async def hello(ctx):
        name = ctx.message.author.name
        msg = f"Hello! {name}\n"
        await ctx.send(msg)


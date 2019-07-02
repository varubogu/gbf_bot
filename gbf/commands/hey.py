#   encoding: utf-8


def init(bot):

    @bot.command()
    async def hey(ctx):
        name = ctx.message.author.name
        msg = f"hey! {name}\n"
        await ctx.send(msg)


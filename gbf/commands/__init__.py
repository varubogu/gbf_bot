#   encoding: utf-8

from gbf.commands import hello, hey


def init(bot):
    """

    :param bot:
    """
    hello.init(bot)
    hey.init(bot)

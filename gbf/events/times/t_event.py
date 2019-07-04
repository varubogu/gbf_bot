#   encoding: utf-8
import asyncio
from discord.client import Client


def times_event(client: Client, wait: int, ch_id=-1):
    """
    周期イベント用デコレーター関数
    :param client:デコレート先で使用するクライアントオブジェクト
    :param wait:イベント周期秒数
    :param ch_id:チャンネルID
    :return:関数オブジェクト
    """
    ch = _get_ch(client, ch_id)

    def __wrapper(func):
        return _inner(wait, func, client, ch)

    return __wrapper


def _get_ch(client: Client, ch_id: int):
    """
    チャンネル取得処理
    :param client: チャンネル取得に使用するClient
    :param ch_id: チャンネルのID
    :return:チャンネルオブジェクト（取得失敗時はNoneではなくExceptionが発生します）
    :except チャンネルIDが不正、またはチャンネル取得失敗
    """
    if ch_id == -1 or ch_id is None:
        Exception('ch_id is bad parameter')

    ch = client.get_channel(ch_id)

    if ch is None:
        Exception('ch is not found')

    return ch


def _inner(wait, func, *args, **kwargs):
    """
    wrapperのための内部関数
    :param wait: 待機秒数
    :param func: 実行する処理
    :param args: 実行関数のリスト引数
    :param kwargs: 実行関数のキーワード引数
    :return: なし
    """
    async def event_loop(f):
        while True:
            await f(*args, **kwargs)
            await asyncio.sleep(wait)

    asyncio.ensure_future(event_loop(func))

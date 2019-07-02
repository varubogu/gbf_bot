#   encoding: utf-8

# コマンド接頭詞
# TODO:prifixを変更できるらしい。どのように実装するのか現在不明
prefix = '$'


def get() -> chr:
    """
    コマンドの接頭詞を取得します。

    例 ※サンプルとしてコマンド名は「hello」とします
        '$' -> $hello
        '/' -> /hello
        '!' -> !hello

    :return: 接頭詞

    """
    return prefix

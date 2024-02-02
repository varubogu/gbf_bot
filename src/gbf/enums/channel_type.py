from enum import Enum


class ChannelType(Enum):
    """チャンネル種類

    Args:
        Base (_type_): _description_
    """
    DEFAULT = 0
    NOTIFICATION = 1
    BATTLE_RECRUIT = 2
    TEAM_NOTIFICATION = 3
    GLOBAL_BATTLE_RECRUIT = 4

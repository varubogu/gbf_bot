from enum import Enum


class LastProcessType(Enum):
    """最終実行種類

    Args:
        Base (_type_): _description_
    """
    SCHEDULE = 1
    SPREADSHEET_LOAD = 2
    SPREADSHEET_PUSH = 3

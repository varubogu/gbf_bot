import os
from enum import Enum


class BattleTypeEnum(Enum):
    DEFAULT = (0, [os.environ['STAMP_PARTICIPATION']])
    ALL_ELEMENT = (1, [
        os.environ['STAMP_ELEMENT_FIRE'],
        os.environ['STAMP_ELEMENT_WATER'],
        os.environ['STAMP_ELEMENT_EARTH'],
        os.environ['STAMP_ELEMENT_WIND'],
        os.environ['STAMP_ELEMENT_LIGHT'],
        os.environ['STAMP_ELEMENT_DARK']
    ])
    SYSTEM = (2, [os.environ['STAMP_PARTICIPATION']])

    def __init__(
            self,
            value: int,
            reactions: [str]
    ):
        super().__init__(value)
        self.__type_value = value
        self.__reactions = reactions

    @property
    def type_value(self) -> int:
        return self.__type_value

    @property
    def reactions(self):
        return self.__reactions

    @classmethod
    def find(cls, type_value: int) -> 'BattleTypeEnum':
        for item in cls:
            if item.__type_value == type_value:
                return item
        return None

from enum import Enum
from cogs.battle.battle_type import BattleTypeEnum as BT


class Target(Enum):
    PROTO_BAHAMUT_HL = (1, 6, [BT.DEFAULT], "プロトバハムートHL", "つよバハ")
    ULTIMATE_BAHAMUT = (2, 6, [BT.DEFAULT], "進撃せし究極の竜HL", "アルバハHL")
    LUCIFER = (3, 6, [BT.DEFAULT, BT.ALL_ELEMENT, BT.SYSTEM], "ダークラプチャー(Hard)", "ルシH")
    BEELZEBUB = (4, 6, [BT.DEFAULT, BT.SYSTEM], "バース・オブ・ニューキング", "バブ")
    BELIAL = (5, 6, [BT.DEFAULT, BT.ALL_ELEMENT], "狡智の堕天使", "ベリ")
    SUPER_ULTIMATE_BAHAMUT = (6, 6, [BT.DEFAULT, BT.ALL_ELEMENT, BT.SYSTEM], "進撃せし蒼き究極の竜", "スパバハ")

    def __init__(
            self,
            target_id: int,
            recruit_count: int,
            use_battle_type: [int],
            quest_name: str,
            quest_alias: str
    ):
        self.__target_id = target_id
        self.__recruit_count = recruit_count
        self.__use_battle_type = use_battle_type
        self.__quest_name = quest_name
        self.__quest_alias = quest_alias

    @property
    def target_id(self) -> int:
        return self.__target_id

    @property
    def recruit_count(self) -> int:
        return self.__recruit_count

    @property
    def use_battle_type(self) -> [int]:
        return self.__use_battle_type

    @property
    def quest_name(self) -> str:
        return self.__quest_name

    @property
    def quest_alias(self) -> str:
        return self.__quest_alias

    @classmethod
    def find_target(cls, target_id_) -> 'Target':
        for item in cls:
            if item.target_id == target_id_:
                return item
        return None

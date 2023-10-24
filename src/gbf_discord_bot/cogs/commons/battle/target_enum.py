from enum import Enum
from gbf_discord_bot.cogs.commons.battle.battle_type import BattleTypeEnum as BT


class Target(Enum):
    PROTO_BAHAMUT_HL = (1, 6, "プロトバハムートHL", "つよバハ", [BT.DEFAULT])
    ULTIMATE_BAHAMUT = (2, 6, "進撃せし究極の竜HL", "アルバハHL", [BT.DEFAULT])
    LUCIFER = (3, 6, "ダークラプチャー(Hard)", "ルシH", [BT.DEFAULT, BT.ALL_ELEMENT, BT.SYSTEM])
    BEELZEBUB = (4, 6, "バース・オブ・ニューキング", "ベルゼバブ", [BT.DEFAULT, BT.SYSTEM])
    BELIAL = (5, 6, "狡智の堕天使", "ベリアル", [BT.DEFAULT, BT.ALL_ELEMENT])
    SUPER_ULTIMATE_BAHAMUT = (6, 6, "進撃せし蒼き究極の竜", "スパバハ", [BT.DEFAULT, BT.ALL_ELEMENT, BT.SYSTEM])
    REASON6 = (7, 6, "天元たる六色の理", "六色の理", [BT.ALL_ELEMENT])

    def __init__(
            self,
            target_id: int,
            recruit_count: int,
            quest_name: str,
            quest_alias: str,
            use_battle_type: [int]
    ):
        self.__target_id = target_id
        self.__recruit_count = recruit_count
        self.__quest_name = quest_name
        self.__quest_alias = quest_alias
        self.__use_battle_type = use_battle_type

    @property
    def target_id(self) -> int:
        return self.__target_id

    @property
    def recruit_count(self) -> int:
        return self.__recruit_count

    @property
    def quest_name(self) -> str:
        return self.__quest_name

    @property
    def quest_alias(self) -> str:
        return self.__quest_alias

    @property
    def use_battle_type(self) -> [int]:
        return self.__use_battle_type

    @classmethod
    def find_target(cls, target_id_) -> 'Target':
        for item in cls:
            if item.target_id == target_id_:
                return item
        return None

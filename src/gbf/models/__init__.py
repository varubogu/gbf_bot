# モデル定義をimportすることでModelBase.metadata内に反映され、自動でテーブル作成処理が実行される
from gbf.models.model_base import ModelBase
from gbf.models.battle_recruitments import BattleRecruitments
from gbf.models.battle_types import BattleTypes
from gbf.models.channel_types import ChannelTypes
from gbf.models.elements import Elements
from gbf.models.environments import Environments
from gbf.models.event_schedule_details import EventSchedulesDetails
from gbf.models.event_schedules import EventSchedules
from gbf.models.guild_channels import GuildChannels
from gbf.models.guild_environments import GuildEnvironments
from gbf.models.guild_event_schedule_details import GuildEventSchedulesDetails
from gbf.models.guild_event_schedules import GuildEventSchedules
from gbf.models.guild_last_process_times import GuildLastProcessTimes
from gbf.models.guild_messages import GuildMessages
from gbf.models.last_process_times import LastProcessTimes
from gbf.models.messages import Messages
from gbf.models.quests import Quests
from gbf.models.quests_alias import QuestsAlias
from gbf.models.schedules import Schedules


async def init_db(conn):
    # モデル定義に従ってテーブル作成
    await conn.run_sync(ModelBase.metadata.create_all)


def get_metadata():
    return ModelBase.metadata


class TableNameMapping:

    __MAPPING__ = [
        # order by table_name_en asc
        {
            'table_name_en': 'battle_recruitments',
            'clsobj': BattleRecruitments
        },
        {
            'table_name_en': 'battle_types',
            'clsobj': BattleTypes
        },
        {
            'table_name_en': 'channel_types',
            'clsobj': ChannelTypes
        },
        {
            'table_name_en': 'elements',
            'clsobj': Elements
        },
        {
            'table_name_en': 'environments',
            'clsobj': Environments
        },
        {
            'table_name_en': 'event_schedule_details',
            'clsobj': EventSchedulesDetails
        },
        {
            'table_name_en': 'event_schedules',
            'clsobj': EventSchedules
        },
        {
            'table_name_en': 'guild_channels',
            'clsobj': GuildChannels
        },
        {
            'table_name_en': 'guild_environments',
            'clsobj': GuildEnvironments
        },
        {
            'table_name_en': 'guild_event_schedule_details',
            'clsobj': GuildEventSchedulesDetails
        },
        {
            'table_name_en': 'guild_event_schedules',
            'clsobj': GuildEventSchedules
        },
        {
            'table_name_en': 'guild_last_process_times',
            'clsobj': GuildLastProcessTimes
        },
        {
            'table_name_en': 'guild_messages',
            'clsobj': GuildMessages
        },
        {
            'table_name_en': 'last_process_times',
            'clsobj': LastProcessTimes
        },
        {
            'table_name_en': 'messages',
            'clsobj': Messages
        },
        {
            'table_name_en': 'quests_alias',
            'clsobj': QuestsAlias
        },
        {
            'table_name_en': 'quests',
            'clsobj': Quests
        },
        {
            'table_name_en': 'schedules',
            'clsobj': Schedules
        },
    ]

    @classmethod
    def getClassObject(cls, table_name_en: str) -> ModelBase:
        """
        get table model
        """
        for cls_info in cls.__MAPPING__:
            if cls_info['table_name_en'] == table_name_en:
                return cls_info['clsobj']
        return None

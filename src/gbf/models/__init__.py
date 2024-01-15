# モデル定義をimportすることでModelBase.metadata内に反映され、自動でテーブル作成処理が実行される
from sqlalchemy.ext.asyncio import AsyncEngine
from gbf.models.model_base import ModelBase
from gbf.models.battle_recruitments import BattleRecruitments
from gbf.models.battle_types import BattleTypes
from gbf.models.channel_types import ChannelTypes
from gbf.models.elements import Elements
from gbf.models.environments import Environments
from gbf.models.event_schedule_details import EventScheduleDetails
from gbf.models.event_schedules import EventSchedules
from gbf.models.guild_channels import GuildChannels
from gbf.models.guild_environments import GuildEnvironments
from gbf.models.guild_event_schedule_details import GuildEventScheduleDetails
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


async def drop_db(conn):
    await conn.run_sync(ModelBase.metadata.drop_all)


async def init_db_from_engine(engine: AsyncEngine):
    async with engine.begin() as conn:
        await init_db(conn)


async def drop_db_from_engine(engine: AsyncEngine):
    async with engine.begin() as conn:
        await drop_db(conn)


def get_metadata():
    return ModelBase.metadata


class TableNameMapping:

    __CLASSES__ = [
            BattleRecruitments,
            BattleTypes,
            ChannelTypes,
            Elements,
            Environments,
            EventScheduleDetails,
            EventSchedules,
            GuildChannels,
            GuildEnvironments,
            GuildEventScheduleDetails,
            GuildEventSchedules,
            GuildLastProcessTimes,
            GuildMessages,
            LastProcessTimes,
            Messages,
            Quests,
            QuestsAlias,
            Schedules
    ]

    __MAPPING__ = [
            {
                'table_name_en': table_class.__tablename__,
                'clsobj': table_class
            } for table_class in __CLASSES__
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

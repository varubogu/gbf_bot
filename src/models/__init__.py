from models.base import Base, engine, SessionLocal
from models.battle_recruitment import BattleRecruitment
from models.battle_type import BattleType
from models.environment import Environment
from models.event_schedules import EventSchedules
from models.event_schedules_detail import EventSchedulesDetail
from models.last_process_time import LastProcessTime
from models.messages import Messages
from models.quest import Quest
from models.schedules import Schedules


def init_db():
    Base.metadata.create_all(bind=engine)

from models.base import Base, engine, SessionLocal
from models.battle_recruitment import BattleRecruitment


def init_db():
    Base.metadata.create_all(bind=engine)

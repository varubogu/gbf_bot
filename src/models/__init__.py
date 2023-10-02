from .base import Base, engine, SessionLocal
from .battle_recruitment import BattleRecruitment


def init_db():
    Base.metadata.create_all(bind=engine)

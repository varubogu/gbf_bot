import uuid
from sqlalchemy \
    import UUID, Column, UniqueConstraint, \
    DateTime, BigInteger, Integer, String
from sqlalchemy.future import select
from gbf.models.model_base import ModelBase
from gbf.models.table_scopes import TableScopes
from gbf.models.table_types import TableType


class EventSchedules(ModelBase):
    """イベントスケジュール情報

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'event_schedules'
    __tabletype__ = TableType.Reference
    __tablescope__ = TableScopes.All
    row_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String)
    event_count = Column(BigInteger)
    profile = Column(String)
    weak_attribute = Column(Integer)
    start_at = Column(DateTime)
    end_at = Column(DateTime)

    __table_args__ = (
        UniqueConstraint(
            'event_type',
            'event_count',
            name='unique_event'
        ),
    )

    async def create(self, session):
        """イベントスケジュールを作成する

        Args:
            session (Session): DB接続セッション

        Raises:
            SQLAlchemyError: DB操作でエラーが発生した場合に発生する例外
        """
        session.add(self)
        await session.commit()

    @classmethod
    async def select_all(cls, session) -> list['EventSchedules']:
        """
        全てのイベントスケジュールを取得する
        Args:
            session (Session): DB接続セッション
        Returns:
            list[EventSchedules]: イベントスケジュールのリスト
        """
        result = await session.execute(select(cls))
        return result.scalars().all()

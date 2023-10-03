
from datetime import datetime, timedelta
import uuid
from sqlalchemy import UUID, Column, String, UniqueConstraint
from models.base import Base
from util.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


def default_expiry_date():
    return datetime.now() + timedelta(days=1)


class Environment(Base):
    """環境変数

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'environment'
    rowid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    key = Column(String)
    value = Column(String)
    memo = Column(String)

    __table_args__ = (
        UniqueConstraint(
            'key',
            name='unique_environment'
        ),
    )

    @classmethod
    def select_one(cls, session, key) -> 'Environment':
        """
        環境変数を取得する
        Args:
            session (Session): DB接続
            key (str): 環境変数キー
        Returns:
            Environment: 環境変数オブジェクト
        Raises:
            EnvironmentNotFound: 環境変数が存在しない場合に発生する例外
        """
        environment = session.query(cls).filter(cls.key == key).first()
        if environment is None:
            raise EnvironmentNotFoundException(key)
        return session.query(cls).filter(cls.key == key).first()

    @classmethod
    def select_all(cls, session, keys) -> ['Environment']:
        """
        環境変数を一括取得する

        """
        return session.query(cls).filter(cls.key.in_(keys)).all()

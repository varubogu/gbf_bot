
from datetime import datetime, timedelta
from sqlalchemy import Column, String
from models.base import Base
from util.exception.environment_notfound_exception \
    import EnvironmentNotFoundException


def default_expiry_date():
    return datetime.now() + timedelta(days=1)


class Environments(Base):
    """環境変数

    Args:
        Base (_type_): _description_
    """
    __tablename__ = 'environments'
    key = Column(String, primary_key=True)
    value = Column(String)
    memo = Column(String)

    @classmethod
    def select_one(cls, session, key) -> 'Environments':
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
    def select_all(cls, session, keys) -> ['Environments']:
        """
        環境変数を一括取得する

        """
        return session.query(cls).filter(cls.key.in_(keys)).all()

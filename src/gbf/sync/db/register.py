from sqlalchemy.ext.asyncio import AsyncSession
from gbf.models.model_base import ModelBase
from gbf.models.utils.get_column_names import get_column_names


class DbRegister:

    async def regist(
            self,
            session: AsyncSession,
            table: list[ModelBase]
    ):
        if not table:
            return

        # テーブル1行目で列名リストを作成
        column_names = await get_column_names(table[0].__class__)

        for row in table:
            # column_namesの1列目は必ず主キー
            if not getattr(row, column_names[0]):
                continue
            await session.merge(row)

        await session.commit()

import uuid
from datetime import datetime

import pytest
from sqlalchemy.future import select

from gbf.models.battle_recruitments import BattleRecruitments
from sqlalchemy.ext.asyncio.session import AsyncSession


class TestBattleRecruitments:

    TEST_GUILD_ID = -1234567890

    @pytest.fixture(scope='function', autouse=True)
    def test_data1(self) -> BattleRecruitments:
        return BattleRecruitments(
            row_id=uuid.uuid4(),
            guild_id=self.TEST_GUILD_ID,
            channel_id=987654321,
            message_id=123456789,
            target_id=0,
            battle_type_id=0,
            room_id="AAAAAA",
            expiry_date=None
        )

    @pytest.fixture(scope='function', autouse=True)
    def test_data2(self) -> BattleRecruitments:
        return BattleRecruitments(
            row_id=uuid.uuid4(),
            guild_id=self.TEST_GUILD_ID,
            channel_id=987654321,
            message_id=123456789,
            target_id=0,
            battle_type_id=0,
            room_id="BBBBBB",
            expiry_date=datetime(2024, 12, 31, 23, 59, 59)
        )

    @pytest.mark.asyncio
    async def test_create(
        self,
        async_db_session: AsyncSession,
        test_data1: BattleRecruitments
    ):

        # テスト対象のメソッドの呼び出し
        await test_data1.create(async_db_session)
        await async_db_session.refresh(test_data1)

        # 結果の検証
        result_data = await async_db_session.execute(
            select(BattleRecruitments).filter(
                BattleRecruitments.row_id == test_data1.row_id
            )
        )

        result = result_data.scalars().first()

        assert result is not None
        assert result.guild_id == test_data1.guild_id
        assert result.channel_id == test_data1.channel_id
        assert result.message_id == test_data1.message_id
        assert result.target_id == test_data1.target_id
        assert result.battle_type_id == test_data1.battle_type_id
        assert result.room_id == test_data1.room_id
        assert result.expiry_date == test_data1.expiry_date

    @pytest.mark.asyncio
    async def test_select_single(
        self,
        async_db_session: AsyncSession,
        test_data2: BattleRecruitments
    ):

        # テストデータの作成
        async_db_session.add(test_data2)
        await async_db_session.commit()
        await async_db_session.refresh(test_data2)

        # テスト対象のメソッドの呼び出し
        result = await BattleRecruitments.select_single(
            async_db_session,
            test_data2.guild_id,
            test_data2.channel_id,
            test_data2.message_id
        )

        # 結果の検証
        assert result is not None
        assert result.guild_id == test_data2.guild_id
        assert result.channel_id == test_data2.channel_id
        assert result.message_id == test_data2.message_id
        assert result.target_id == test_data2.target_id
        assert result.battle_type_id == test_data2.battle_type_id
        assert result.room_id == test_data2.room_id
        assert result.expiry_date == test_data2.expiry_date

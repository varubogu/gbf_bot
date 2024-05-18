from datetime import datetime
from discord.ext import commands, tasks
from sqlalchemy.ext.asyncio import AsyncSession
from gbf.schedules.minute_executor import MinuteScheduleExecutor
from gbf.models.messages import Messages
from gbf.models.session import AsyncSessionLocal
from gbf_discord_bot.cogs.commons.battle.after_reaction import AfterReaction
from gbf_discord_bot.utils.reaction_util import ReactionUtil


class MinuteSchedule(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.channel = None
        self.executor = MinuteScheduleExecutor()

    async def cog_load(self):
        self.loop.start()

    async def cog_unload(self):
        self.loop.cancel()

    @tasks.loop(seconds=10)
    async def loop(self):
        now = datetime.now()

        if not self.bot.is_ready():
            return

        try:
            async with self.bot.db_lock:
                async with AsyncSessionLocal() as session:
                    await self.inner_loop(session, now)
        except Exception as e:
            print(f'schedule.loopで例外発生:{e}')

    async def inner_loop(
            self,
            session: AsyncSession,
            now: datetime
    ):
        schedules = await self.executor.fetch_schedules(session, now)
        message_ids = [schedule.message_id for schedule in schedules]
        db_messages = await Messages.select_multi(session, message_ids)

        for schedule in schedules:
            db_message: Messages = next(
                (m for m in db_messages
                    if m.message_id == schedule.message_id),
                None)

            if db_message is None:
                continue

            channel = await self.bot.fetch_channel(schedule.channel_id)

            mention = ''
            # マルチ募集に紐づくリアクション者を取得
            if len(schedule.children) > 0:
                mid = schedule.children[0].message_id
                original_message = await channel.fetch_message(mid)
                # Botユーザーは除外してリアクションとユーザーの一覧を取得
                reactions = await ReactionUtil.get_reaction_users(
                    original_message,
                    lambda user: user == self.bot.user
                )

                reaction_users = await AfterReaction.get_reaction_users(reactions)
                if self.bot.user in reaction_users:
                    reaction_users.remove(self.bot.user)
                mention = ' '.join(f"{user.mention}" for user in reaction_users) + '\n'

            message = await channel.send(mention + db_message.message_jp)
            if db_message.reactions:
                for reaction in db_message.reactions.split(","):
                    if reaction:
                        await message.add_reaction(reaction)


async def setup(bot: commands.Bot):
    await bot.add_cog(MinuteSchedule(bot))

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from db import get_all_users
from greetings import get_scheduled_message

async def schedule_checks(bot):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_users, "interval", days=1, args=[bot])
    scheduler.start()

async def check_users(bot):
    users = await get_all_users()
    today = datetime.now().date()

    for user_id, join_date in users:
        join_date = datetime.strptime(join_date, "%Y-%m-%d").date()
        days = (today - join_date).days

        msg = get_scheduled_message(days)
        if msg:
            try:
                await bot.send_message(user_id, msg)
            except:
                pass  # возможно пользователь ограничил бота

        if days == 364:
            try:
                await bot.ban_chat_member(int(bot.group_id), user_id)
            except:
                pass

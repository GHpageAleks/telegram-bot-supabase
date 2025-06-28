import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import ChatMemberUpdated
from aiogram.enums import ChatMemberStatus
from dotenv import load_dotenv

from db import init_db, add_user, get_all_users
from scheduler import schedule_checks
from greetings import send_welcome_message

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
GROUP_ID = int(os.getenv("GROUP_ID"))

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, parse_mode="HTML")  # так, чтобы работало в 3.4.1
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)


@dp.chat_member()
async def on_user_joined(event: ChatMemberUpdated):
    if event.old_chat_member.status in {ChatMemberStatus.LEFT, ChatMemberStatus.KICKED} and \
       event.new_chat_member.status == ChatMemberStatus.MEMBER:

        user_id = event.new_chat_member.user.id
        full_name = event.new_chat_member.user.full_name
        logging.info(f"[JOINED] {full_name} ({user_id})")

        await add_user(user_id, full_name)
        await send_welcome_message(bot, event.chat.id, user_id)


@dp.chat_member()
async def on_user_added(event: ChatMemberUpdated):
    if event.old_chat_member.status == ChatMemberStatus.BANNED and \
       event.new_chat_member.status == ChatMemberStatus.MEMBER:

        user_id = event.new_chat_member.user.id
        full_name = event.new_chat_member.user.full_name
        logging.info(f"[ADDED] {full_name} ({user_id})")

        await add_user(user_id, full_name)
        await send_welcome_message(bot, event.chat.id, user_id)


async def main():
    await init_db()
    await schedule_checks(bot)
    logging.info("🚀 Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


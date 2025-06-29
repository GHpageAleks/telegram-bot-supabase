import os
from datetime import datetime
from supabase import create_client, Client

# Получаем переменные из .env
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# Создаем клиента Supabase с сервисным ключом
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


async def init_db():
    # Создаем таблицу, если ее нет
    # Supabase не поддерживает прямое создание таблиц через API, 
    # поэтому таблицу нужно создать вручную через панель Supabase.
    # Если таблица есть — эту функцию можно сделать пустой или для проверки.
    pass

async def add_user(user_id: int, name: str):
    now = datetime.now().strftime("%Y-%m-%d")
    data = {
        "user_id": user_id,
        "name": name,
        "join_date": now,
    }
    # Вставляем или обновляем пользователя (upsert)
    response = supabase.table("users").upsert(data).execute()
    if response.error:
        print("Ошибка при добавлении пользователя в Supabase:", response.error)

async def get_all_users():
    response = supabase.table("users").select("user_id, join_date").execute()
    if response.error:
        print("Ошибка при получении пользователей из Supabase:", response.error)
        return []
    return response.data

async def remove_user(user_id: int):
    response = supabase.table("users").delete().eq("user_id", user_id).execute()
    if response.error:
        print("Ошибка при удалении пользователя из Supabase:", response.error)


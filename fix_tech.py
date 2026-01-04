# fix_tech.py
from database import init_db, AsyncSessionLocal, User, Role
from sqlalchemy import select
from config import TECH_SPECIALIST_ID
import asyncio

async def check():
    await init_db()
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User).where(User.telegram_id == TECH_SPECIALIST_ID))
        user = result.scalar_one_or_none()
        print(f"ID: {TECH_SPECIALIST_ID}")
        print(f"Роль: '{user.role}' (должно быть 'Глав Тех Специалист')")
        print(f"Забанен: {user.is_banned}")
        if user.role != Role.CHIEF_TECH.value:
            user.role = Role.CHIEF_TECH.value
            user.is_banned = False
            await session.commit()
            print("✅ ИСПРАВЛЕНО!")
        else:
            print("✅ Роль правильная")

asyncio.run(check())
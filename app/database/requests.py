from app.database.models import async_session
from app.database.models import User, Category, Item
from sqlalchemy import select


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def add_category_to_db(name: str):
    async with async_session() as session:
        new_category = Category(name=name)
        session.add(new_category)
        await session.commit()
        
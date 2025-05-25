from app.database.models import async_session
from app.database.models import User, House, Corp, Floor, Apartment
from sqlalchemy import select


async def set_user(tg_id: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def get_houses():
    async with async_session() as session:
        return await session.scalars(select(House))
    

async def get_corp_house(house_id):
    async with async_session() as session:
        return await session.scalars(select(Corp).where(Corp.house_id == house_id))
    

async def get_floor_corp(corp_id):
    async with async_session() as session:
        return await session.scalars(select(Floor).where(Floor.corp_id == corp_id))
    
async def get_apartament_floor(floor_id):
    async with async_session() as session:
        return await session.scalars(select(Apartment).where(Apartment.floor_id == floor_id))
    
async def get_apartament(apartament_id):
    async with async_session() as session:
        return await session.scalar(select(Apartment).where(Apartment.id == apartament_id))
    
    
'''
async def get_categories():
    async with async_session() as session:
        return await session.scalars(select(Category))


async def add_category_to_db(name: str):
    async with async_session() as session:
        new_category = Category(name=name)
        session.add(new_category)
        await session.commit()
        '''
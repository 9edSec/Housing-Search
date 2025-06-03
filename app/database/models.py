from sqlalchemy import BigInteger, String, ForeignKey, UniqueConstraint, Integer, Boolean, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    
    
class Corp(Base):
    __tablename__ = "corps"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column()



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
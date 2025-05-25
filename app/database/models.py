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


class House(Base):
    __tablename__ = 'houses'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(25))


class Corp(Base):
    __tablename__ = 'corps'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False) 
    house_id: Mapped[int] = mapped_column(ForeignKey('houses.id'))


class Floor(Base):
    __tablename__ = 'floors'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer) 
    corp_id: Mapped[int] = mapped_column(ForeignKey('corps.id')) 


class Apartment(Base):
    __tablename__ = 'apartments'

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(Integer)
    square: Mapped[int] = mapped_column(Integer)
    rooms: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Integer)
    price_m2: Mapped[int] = mapped_column(Integer)
    pdf: Mapped[str] = mapped_column()
    floor_id: Mapped[int] = mapped_column(ForeignKey('floors.id'), nullable=False) 
    



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
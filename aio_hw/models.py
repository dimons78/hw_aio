import os

from sqlalchemy import Column, DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "1234")
PG_DB = os.getenv("PG_DB", "netology")
PG_HOST = os.getenv("PG_HOST", "127.0.0.1")
PG_PORT = os.getenv("PG_PORT", "5431")


PG_DSN = f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"


engine = create_async_engine(PG_DSN)

Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()


class Announcement(Base):

    __tablename__ = "app_announcement"

    id = Column(Integer, primary_key=True)

    title = Column(String, unique=True, index=True, nullable=False)

    description = Column(String, nullable=False)

    creation_time = Column(DateTime, server_default=func.now())

    owner = Column(String, nullable=False)


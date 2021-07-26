from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from backend.config import conf

engine = create_async_engine(
    f"postgresql+asyncpg://{conf.get('DB_USER')}:{conf.get('DB_PASSWORD')}@postgres:{conf.get('DB_PORT')}/{conf.get('DB_NAME')}"
)


SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

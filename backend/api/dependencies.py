from .session import SessionLocal


async def get_db():
    """
    Return a local session maker to interact with the database

    :return: AsyncSession
    """
    async with SessionLocal() as db_session:
        yield db_session

from collections.abc import AsyncGenerator

from redis.asyncio.client import Redis
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from python_code.config import settings
from python_code.redis import get_redis_connection

# connection pool - список соеденений с бд


# future – Use the 2.0 style Engine and Connection API.

# echo=False – if True, the Engine will log all statements as well
# as a repr() of their parameter lists to the default log handler,
# which defaults to sys.stdout for output

# Engine= Connects a Pool and Dialect together to provide a source of database connectivity and behavior.

print(settings.DATABASE_URL)
engine: AsyncEngine = create_async_engine(settings.DATABASE_URL)


async def init_db(eng: AsyncEngine):
    redis: Redis = await get_redis_connection()
    await redis.flushall()
    async with eng.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        # Base.metadata.drop_all(bind=eng)
        # Base.metadata.create_all(bind=eng)
        print('hello')


# фабрика, которая генерируют новую сессия при каждом вызове
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Every model will inherit this 'Base' class and we will utilize this base class to create all the database tables.
Base = declarative_base()


# используется как зависимости, для создания сессии с бд
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session() as session:
        yield session

    # session: sqlalchemy.orm.Session = Session()
    # try:
    #     yield session
    # except Exception as e:
    #     print(str(type(e)))
    # finally:
    #     session.close()

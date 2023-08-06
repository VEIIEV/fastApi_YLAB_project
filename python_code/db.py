import sqlalchemy as sa
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from python_code.config import settings

# connection pool - список соеденений с бд


# future – Use the 2.0 style Engine and Connection API.

# echo=False – if True, the Engine will log all statements as well
# as a repr() of their parameter lists to the default log handler,
# which defaults to sys.stdout for output

# Engine= Connects a Pool and Dialect together to provide a source of database connectivity and behavior.

print(settings.DATABASE_URL)
engine = sa.create_engine(settings.DATABASE_URL)


def init_db(eng):
    Base.metadata.drop_all(bind=eng)
    Base.metadata.create_all(bind=eng)
    print('hello')


# фабрика, которая генерируют новую сессия при каждом вызове
Session = sessionmaker(bind=engine, class_=Session)


# Every model will inherit this 'Base' class and we will utilize this base class to create all the database tables.
class Base(DeclarativeBase):
    pass


# используется как зависимости, для создания сессии с бд
async def get_session():
    session = Session()
    try:
        yield session
    except Exception as e:
        print(str(type(e)))
    finally:
        session.close()

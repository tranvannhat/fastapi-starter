import redis
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
redis_db = redis.Redis(host='localhost', port=6379, db=0)


def init_db_pg_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    from app.core.config import settings

    some_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
    session_maker = sessionmaker(bind=some_engine)
    session = session_maker()
    return session
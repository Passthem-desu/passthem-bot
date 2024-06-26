import sqlalchemy
import sqlalchemy.event
from sqlalchemy import PoolProxiedConnection
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.common.config import config

sqlEngine = create_async_engine(config.sqlalchemy_database_url)

_async_session_factory = async_sessionmaker(
    sqlEngine, class_=AsyncSession, expire_on_commit=False, autoflush=False
)


@sqlalchemy.event.listens_for(sqlEngine.sync_engine, "connect")
def set_sqlite_pragma(dbapi_connection: PoolProxiedConnection, _):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.execute("PRAGMA threading_mode = MULTITHREAD;")
    cursor.execute("PRAGMA busy_timeout = 30000;")
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.close()


def get_session():
    return _async_session_factory()


__all__ = ["get_session", "sqlEngine"]

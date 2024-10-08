from __future__ import annotations

import asyncio

import nonebot
from sqlalchemy import Connection
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.util import await_only

from alembic import context

# 初始化 Nonebot


nonebot.init()

import src.common.config
import src.models.models
import src.models.base

# Alembic Config 对象, 它提供正在使用的 .ini 文件中的值.
config = context.config

# 默认 AsyncEngine
# engine: AsyncEngine = config.attributes["engines"][""]
engine = create_async_engine(src.common.config.get_config().sqlalchemy_database_url)

# 模型的 MetaData, 用于 "autogenerate" 支持.
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = src.models.base.Base.metadata

# 其他来自 config 的值, 可以按 env.py 的需求定义, 例如可以获取:
# my_important_option = config.get_main_option("my_important_option")
# ... 等等.


def run_migrations_offline() -> None:
    """在“离线”模式下运行迁移.

    虽然这里也可以获得 Engine, 但我们只需要一个 URL 即可配置 context.
    通过跳过 Engine 的创建, 我们甚至不需要 DBAPI 可用.

    在这里调用 context.execute() 会将给定的字符串写入到脚本输出.
    """

    context.configure(
        url=engine.url,
        dialect_opts={"paramstyle": "named"},
        target_metadata=target_metadata,
        literal_binds=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        render_as_batch=True,
        target_metadata=target_metadata,
        # include_object=no_drop_table,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """在“在线”模式下运行迁移.

    这种情况下, 我们需要为 context 创建一个连接.
    """

    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)


if context.is_offline_mode():
    run_migrations_offline()
else:
    coro = run_migrations_online()

    try:
        asyncio.run(coro)
    except RuntimeError:
        await_only(coro)

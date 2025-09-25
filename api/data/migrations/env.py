import asyncio
from logging.config import fileConfig
# from sqlalchemy import engine_from_config
from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy import Connection
from sqlalchemy import pool
from alembic import context
from api.data.base import Base
from api.data import models  # Ensure all models are imported for Alembic to detect them
from api.settings import Settings
from dotenv import load_dotenv

class Migration:
    def __init__(self, config=None, settings=None):        
        # this is the Alembic Config object, which provides
        # access to the values within the .ini file in use.
        self.config = config

        # Interpret the config file for Python logging.
        # This line sets up loggers basically.
        if self.config.config_file_name is not None:
            fileConfig(self.config.config_file_name)

        # add your model's MetaData object here
        # for 'autogenerate' support
        # from myapp import mymodel
        # target_metadata = mymodel.Base.metadata
        self.target_metadata = Base.metadata

        # other values from the config, defined by the needs of env.py,
        # can be acquired:
        # my_important_option = config.get_main_option("my_important_option")
        # ... etc.

        # Set the alembic sqlalchemy.url option dynamically using settings from settings.py
        self.settings = settings or Settings()
        self.config.set_main_option(
            "sqlalchemy.url",
            f"postgresql+asyncpg://{self.settings.database_username}:{self.settings.database_password}@{self.settings.database_hostname}:{self.settings.database_port}/{self.settings.database_name}"
        )

    def run_migrations_offline(self) -> None:
        """Run migrations in 'offline' mode.

        This configures the context with just a URL
        and not an Engine, though an Engine is acceptable
        here as well.  By skipping the Engine creation
        we don't even need a DBAPI to be available.

        Calls to context.execute() here emit the given string to the
        script output.

        """
        url = self.config.get_main_option("sqlalchemy.url")
        context.configure(
            url=url,
            target_metadata=self.target_metadata,
            literal_binds=True,
            dialect_opts={"paramstyle": "named"},
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    def do_run_migrations(self, connection: Connection) -> None:
        context.configure(
            connection=connection,
            target_metadata=self.target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()

    async def run_migrations_online(self) -> None:
        """Run migrations in 'online' mode.

        In this scenario we need to create an Engine
        and associate a connection with the context.

        """
        connectable = async_engine_from_config(
            configuration=self.config.get_section(self.config.config_ini_section, {}),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
            future=True
        )

        async with connectable.connect() as async_connection:
            await async_connection.run_sync(self.do_run_migrations)
        
        await connectable.dispose()

# Instantiate the Migration class
if hasattr(context, "config") and context.config is not None:    
    load_dotenv()  # Load environment variables from .env file
    migration = Migration(context.config)
    # Determine if we are in offline or online mode and run the appropriate migration method
    if context.is_offline_mode():
        migration.run_migrations_offline()
    else:
        asyncio.run(migration.run_migrations_online())

import pytest
from unittest.mock import MagicMock, AsyncMock

from api.data.migrations.env import Migration
from sqlalchemy.engine import Connection

def test_sqlalchemy_url_is_set_from_settings(monkeypatch):
    """Test that the sqlalchemy.url is set correctly from Settings in Migration."""
    # Mock environment variables for Settings
    # Create a mock config object    
    config_mock = MagicMock()
    config_mock.config_file_name = None
    config_mock.set_main_option = MagicMock()
    # create a mock settings object
    settings_mock = MagicMock()
    settings_mock.database_username = "test_user"
    settings_mock.database_password = "test_password"
    settings_mock.database_hostname = "localhost"
    settings_mock.database_port = "5432"
    settings_mock.database_name = "test_db"
    # Instantiate Migration with mocks
    migration = Migration(config=config_mock, settings=settings_mock)
    config_mock.set_main_option.assert_called_once_with("sqlalchemy.url", "postgresql+asyncpg://test_user:test_password@localhost:5432/test_db")

def test_run_migrations_offline_calls_context(monkeypatch):
    """Test that the run_migrations_offline method calls the context correctly."""
    # Mock the context and its methods
    context_mock = MagicMock()
    context_mock.config = MagicMock()
    context_mock.config.get_main_option = MagicMock(return_value="postgresql+asyncpg://test_user:test_password@localhost:5432/test_db")
    context_mock.run_migrations = MagicMock()

    # Patch the context creation to return the mock
    monkeypatch.setattr("api.data.migrations.env.context", context_mock)

    # Create a mock config object    
    config_mock = MagicMock()
    config_mock.config_file_name = None
    config_mock.set_main_option = MagicMock()
    # create a mock settings object
    settings_mock = MagicMock()
    settings_mock.database_username = "test_user"
    settings_mock.database_password = "test_password"
    settings_mock.database_hostname = "localhost"
    settings_mock.database_port = "5432"
    settings_mock.database_name = "test_db"
    # Instantiate Migration with mocks
    migration = Migration(config=config_mock, settings=settings_mock)

    migration.run_migrations_offline()
    context_mock.configure.assert_called_once()

def test_do_run_migrations(monkeypatch):
    """Test that the do_run_migrations method calls the context correctly."""
    # Mock the context and its methods
    context_mock = MagicMock()
    context_mock.run_migrations = MagicMock()

    # Patch the context creation to return the mock
    monkeypatch.setattr("api.data.migrations.env.context", context_mock)

    # Create a mock config object    
    config_mock = MagicMock()
    config_mock.config_file_name = None
    config_mock.set_main_option = MagicMock()
    # create a mock settings object
    settings_mock = MagicMock()
    settings_mock.database_username = "test_user"
    settings_mock.database_password = "test_password"
    settings_mock.database_hostname = "localhost"
    settings_mock.database_port = "5432"
    settings_mock.database_name = "test_db"
    # Instantiate Migration with mocks
    migration = Migration(config=config_mock, settings=settings_mock)

    # Create a mock connection
    connection_mock = MagicMock()
    connection_mock = MagicMock(spec=Connection)
    migration.do_run_migrations(connection=connection_mock)
    context_mock.run_migrations.assert_called_once()

@pytest.mark.asyncio
async def test_run_migrations_online(monkeypatch):
    connectable_mock = MagicMock()
    async_connection_mock = MagicMock()
    async_connection_mock.run_sync = AsyncMock()

    class AsyncContextManagerMock:
        async def __aenter__(self):
            return async_connection_mock
        async def __aexit__(self, exc_type, exc, tb):
            return None

    connectable_mock.connect = MagicMock(return_value=AsyncContextManagerMock())
    connectable_mock.dispose = AsyncMock()
    # Patch the async_engine_from_config to return the mock
    monkeypatch.setattr("api.data.migrations.env.async_engine_from_config", MagicMock(return_value=connectable_mock))
    # Patch the do_run_migrations method to be a mock
    do_run_migrations_mock = MagicMock()
    monkeypatch.setattr("api.data.migrations.env.Migration.do_run_migrations", do_run_migrations_mock)

    # Create a mock config object
    config_mock = MagicMock()
    config_mock.config_file_name = None
    config_mock.set_main_option = MagicMock()
    # create a mock settings object
    settings_mock = MagicMock()
    settings_mock.database_username = "test_user"
    settings_mock.database_password = "test_password"
    settings_mock.database_hostname = "localhost"
    settings_mock.database_port = "5432"
    settings_mock.database_name = "test_db"
    # Instantiate Migration with mocks
    migration = Migration(config=config_mock, settings=settings_mock)
    await migration.run_migrations_online()
    connectable_mock.connect.assert_called_once()
    async_connection_mock.run_sync.assert_called_once_with(do_run_migrations_mock)
    connectable_mock.dispose.assert_called_once()

def test_migration_run(monkeypatch):
    """Test the static run method of Migration."""
    # Mock the context and its methods
    context_mock = MagicMock()
    context_mock.config = MagicMock()
    context_mock.is_offline_mode = MagicMock(return_value=True)
    context_mock.config.get_main_option = MagicMock(return_value="postgresql+asyncpg://test_user:test_password@localhost:5432/test_db")
    # Patch the context creation to return the mock
    monkeypatch.setattr("api.data.migrations.env.context", context_mock)
    # Patch load_dotenv to be a mock
    monkeypatch.setattr("api.data.migrations.env.load_dotenv", MagicMock())
    # Patch asyncio.run to be a mock
    monkeypatch.setattr("api.data.migrations.env.asyncio.run", MagicMock())

    # Create a mock config object    
    config_mock = MagicMock()
    config_mock.config_file_name = None
    config_mock.set_main_option = MagicMock()
    # create a mock settings object
    settings_mock = MagicMock()
    settings_mock.database_username = "test_user"
    settings_mock.database_password = "test_password"
    settings_mock.database_hostname = "localhost"
    settings_mock.database_port = "5432"
    settings_mock.database_name = "test_db"
    
    # Patch the Migration constructor to use our mock settings
    original_init = Migration.__init__
    def mock_init(self, config, settings=None):
        original_init(self, config=config_mock, settings=settings_mock)
    monkeypatch.setattr("api.data.migrations.env.Migration.__init__", mock_init)

    # Run the static method
    Migration.run()
    context_mock.is_offline_mode.assert_called_once()
    context_mock.run_migrations.assert_called_once()
    # Check that load_dotenv was called
    from api.data.migrations.env import load_dotenv, asyncio
    load_dotenv.assert_called_once()
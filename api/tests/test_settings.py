import pytest
from pydantic import ValidationError
from api.settings import Settings
from api.constants import NEO4J_INVALID_SCHEME_ERROR, INVALID_URL_ERROR, INVALID_PORT_TYPE_ERROR, FIELD_REQUIRED_ERROR

# This fixture provides a complete and valid set of environment variables for testing.
# It uses monkeypatch to set them for the duration of the test.
@pytest.fixture
def valid_env_vars(monkeypatch):
    monkeypatch.setenv("APP_NAME", "Test App")
    monkeypatch.setenv("DATABASE_USERNAME", "test_user")
    monkeypatch.setenv("DATABASE_PASSWORD", "test_password")
    monkeypatch.setenv("DATABASE_HOSTNAME", "localhost")
    monkeypatch.setenv("DATABASE_PORT", "5432")
    monkeypatch.setenv("DATABASE_NAME", "test_db")
    monkeypatch.setenv("NEO4J_URI", "bolt://localhost:7687")
    monkeypatch.setenv("NEO4J_USERNAME", "neo4j_user")
    monkeypatch.setenv("NEO4J_PASSWORD", "neo4j_password")

def test_settings_loads_successfully_with_correct_types(valid_env_vars):
    """Test that the Settings object is created without errors."""
    try:
        settings = Settings()
        # The test passes if no ValidationError is raised.
    except ValidationError as e:
        pytest.fail(f"Settings validation failed unexpectedly: {e}")

def test_raises_error_when_variable_is_missing(valid_env_vars, monkeypatch):
    """Test that validation fails when a required environment variable is missing."""
    monkeypatch.delenv("APP_NAME")

    with pytest.raises(ValidationError) as excinfo:
        Settings()

    assert "app_name" in str(excinfo.value)
    assert FIELD_REQUIRED_ERROR in str(excinfo.value)

def test_raises_error_for_invalid_port_type(valid_env_vars, monkeypatch):
    """Test that validation fails for a non-integer value in an integer field."""
    monkeypatch.setenv("DATABASE_PORT", "not_an_integer")

    with pytest.raises(ValidationError) as excinfo:
        Settings()

    assert "database_port" in str(excinfo.value)
    assert INVALID_PORT_TYPE_ERROR in str(excinfo.value)

def test_raises_error_for_invalid_url(valid_env_vars, monkeypatch):
    """
    Test a more complex pydantic validation, like a URL format.
    You can add similar tests for other complex types if you have them.
    """
    monkeypatch.setenv("NEO4J_URI", "invalid_uri")

    with pytest.raises(ValidationError) as excinfo:
        Settings()

    assert "neo4j_uri" in str(excinfo.value)
    assert INVALID_URL_ERROR in str(excinfo.value)

def test_raises_error_for_invalid_neo4j_scheme(valid_env_vars, monkeypatch):
    """Test that validation fails for an invalid Neo4j URI scheme."""
    monkeypatch.setenv("NEO4J_URI", "http://localhost:7687")  # Invalid scheme

    with pytest.raises(ValidationError) as excinfo:
        Settings()

    assert "neo4j_uri" in str(excinfo.value)
    assert NEO4J_INVALID_SCHEME_ERROR in str(excinfo.value)

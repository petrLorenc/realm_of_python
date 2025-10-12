import pytest
from typing import Annotated

# Import your dependency injection system
from di_playground import registry, injectable, inject, Depends, DependencyRegistry


# Test dependencies and services
@injectable
def database_connection():
    """In a real app, this would create an actual DB connection."""
    return {"type": "production", "host": "real-db.example.com"}


@injectable
def config_service():
    """Real production config service."""
    return {"api_key": "real-production-key", "timeout": 30, "retry_attempts": 3}


@injectable
def user_repository(
    db: Annotated[dict, Depends(database_connection)],
    config: Annotated[dict, Depends(config_service)],
):
    """Repository that depends on the database and config."""
    return {
        "db": db,
        "config": config,
        "get_user": lambda user_id: {"id": user_id, "name": f"User {user_id}"},
    }


# The actual service we want to test
@inject
def get_user_data(user_id: int, repo: Annotated[dict, Depends(user_repository)]):
    """Service that gets user data - this is what we want to test."""
    user = repo["get_user"](user_id)
    return {
        "user": user,
        "database_type": repo["db"]["type"],
        "timeout": repo["config"]["timeout"],
    }


# Tests demonstrating the benefits of DI
class TestDependencyInjection:

    def test_real_dependencies(self):
        """Test with real dependencies (integration test)."""
        result = get_user_data(42)
        assert result["user"]["id"] == 42
        assert result["database_type"] == "production"
        assert result["timeout"] == 30

    def test_with_mock_database(self):
        """Test with a mock database dependency."""

        # Override just the database dependency
        @injectable
        def database_connection():
            return {"type": "mock", "host": "in-memory"}

        result = get_user_data(42)
        assert result["user"]["id"] == 42
        assert result["database_type"] == "mock"  # Using mock DB
        assert result["timeout"] == 30  # Still using real config

    # def test_with_custom_config(self):
    #     """Test with custom configuration."""
    #     # Override just the config dependency
    #     @injectable
    #     def config_service():
    #         return {
    #             "api_key": "test-key",
    #             "timeout": 5,  # Much shorter timeout for tests
    #             "retry_attempts": 0  # No retries in tests
    #         }

    #     result = get_user_data(42)
    #     assert result["user"]["id"] == 42
    #     assert result["database_type"] == "production"  # Still using real DB
    #     assert result["timeout"] == 5  # Using test timeout

    # def test_with_fully_mocked_dependencies(self):
    #     """Test with all dependencies mocked."""
    #     # Create a test-specific registry for complete isolation
    #     test_registry = DependencyRegistry()
    #     original_registry = registry

    #     try:
    #         # Replace the global registry temporarily
    #         globals()['registry'] = test_registry

    #         # Register mock dependencies
    #         @injectable
    #         def database_connection():
    #             return {"type": "mock", "host": "in-memory"}

    #         @injectable
    #         def config_service():
    #             return {"api_key": "test-key", "timeout": 1, "retry_attempts": 0}

    #         # Custom mock repository with controlled behavior
    #         @injectable
    #         def user_repository(db: Annotated[dict, Depends(database_connection)],
    #                             config: Annotated[dict, Depends(config_service)]):
    #             return {
    #                 "db": db,
    #                 "config": config,
    #                 "get_user": lambda user_id: {"id": user_id, "name": "Test User"}
    #             }

    #         result = get_user_data(42)
    #         assert result["user"]["name"] == "Test User"
    #         assert result["database_type"] == "mock"
    #         assert result["timeout"] == 1

    #     finally:
    #         # Restore the original registry
    #         globals()['registry'] = original_registry

    # def test_direct_injection_override(self):
    #     """Test that explicit parameters override injected dependencies."""
    #     # Create a custom repository directly
    #     custom_repo = {
    #         "db": {"type": "direct-injection"},
    #         "config": {"timeout": 999},
    #         "get_user": lambda user_id: {"id": user_id, "name": "Direct Injection User"}
    #     }

    #     # Pass the repository directly instead of using DI
    #     result = get_user_data(42, repo=custom_repo)

    #     assert result["user"]["name"] == "Direct Injection User"
    #     assert result["database_type"] == "direct-injection"
    #     assert result["timeout"] == 999

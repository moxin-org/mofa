"""Configuration file for pytest.

This module contains pytest fixtures and configuration that are shared across tests.
"""

import pytest


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for each test session.
    
    This is needed for proper asyncio test configuration with pytest-asyncio.
    """
    import asyncio
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


# Add global test fixtures here

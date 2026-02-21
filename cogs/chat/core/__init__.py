"""Core module - Framework-independent logic."""

from .config import ChatConfig
from .exceptions import (
    ChatException,
    ProviderException,
    RateLimitException,
    ConfigurationException,
    ContextException,
    TimeoutException,
    AuthenticationException
)
from .rate_limiter import RateLimiter
from .personality import PersonalityManager, get_personality_manager, UserMemory

__all__ = [
    'ChatConfig',
    'ChatException',
    'ProviderException',
    'RateLimitException',
    'ConfigurationException',
    'ContextException',
    'TimeoutException',
    'AuthenticationException',
    'RateLimiter',
    'PersonalityManager',
    'get_personality_manager',
    'UserMemory',
]

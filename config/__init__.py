"""
Configuration Module
====================
Handles loading and parsing of the settings.ini file.
"""

import configparser
import os
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger('discord.config')

# Default configuration directory
CONFIG_DIR = Path(__file__).parent
CONFIG_FILE = CONFIG_DIR / 'settings.ini'


class Config:
    """Configuration manager for the music bot."""
    
    def __init__(self, config_file: Optional[Path] = None):
        self.config = configparser.ConfigParser()
        self.config_file = config_file or CONFIG_FILE
        self._loaded = False
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from INI file."""
        if not self.config_file.exists():
            logger.warning(f"Config file not found: {self.config_file}")
            logger.info("Using default configuration values")
            return
        
        try:
            self.config.read(self.config_file, encoding='utf-8')
            self._loaded = True
            logger.info(f"✅ Loaded configuration from {self.config_file}")
        except Exception as e:
            logger.error(f"❌ Failed to load config: {e}")
    
    def get(self, section: str, key: str, fallback: Any = None) -> Any:
        """
        Get a configuration value.
        
        Args:
            section: INI section name
            key: Configuration key
            fallback: Default value if key not found
            
        Returns:
            Configuration value or fallback
        """
        try:
            value = self.config.get(section, key)
            
            # Convert string booleans
            if value.lower() in ('true', 'yes', '1'):
                return True
            elif value.lower() in ('false', 'no', '0'):
                return False
            
            # Convert numeric values
            try:
                if '.' in value:
                    return float(value)
                return int(value)
            except (ValueError, TypeError):
                pass
            
            # Return string as-is
            return value
            
        except (configparser.NoSectionError, configparser.NoOptionError):
            return fallback
    
    def get_int(self, section: str, key: str, fallback: int = 0) -> int:
        """Get integer configuration value."""
        value = self.get(section, key, fallback)
        try:
            return int(value)
        except (ValueError, TypeError):
            return fallback
    
    def get_float(self, section: str, key: str, fallback: float = 0.0) -> float:
        """Get float configuration value."""
        value = self.get(section, key, fallback)
        try:
            return float(value)
        except (ValueError, TypeError):
            return fallback
    
    def get_bool(self, section: str, key: str, fallback: bool = False) -> bool:
        """Get boolean configuration value."""
        return bool(self.get(section, key, fallback))
    
    def get_list(self, section: str, key: str, fallback: list = None, 
                 separator: str = ',') -> list:
        """Get list configuration value (comma-separated)."""
        value = self.get(section, key, None)
        if value is None:
            return fallback or []
        return [item.strip() for item in value.split(separator) if item.strip()]
    
    @property
    def is_loaded(self) -> bool:
        """Check if configuration was loaded successfully."""
        return self._loaded
    
    # Convenience properties for commonly used settings
    
    @property
    def token(self) -> str:
        """Get Discord bot token."""
        return self.get('discord', 'token', os.getenv('DISCORD_TOKEN', ''))
    
    @property
    def prefix(self) -> str:
        """Get command prefix."""
        return self.get('discord', 'prefix', '!')
    
    @property
    def default_volume(self) -> int:
        """Get default volume level."""
        return self.get_int('discord', 'default_volume', 50)
    
    @property
    def max_volume(self) -> int:
        """Get maximum volume limit."""
        return self.get_int('discord', 'max_volume', 100)
    
    @property
    def owner_id(self) -> int:
        """Get bot owner ID."""
        return self.get_int('discord', 'owner_id', 0)
    
    @property
    def test_guild_id(self) -> int:
        """Get test guild ID."""
        return self.get_int('discord', 'test_guild_id', 0)
    
    @property
    def spotify_enabled(self) -> bool:
        """Check if Spotify is enabled."""
        return self.get_bool('spotify', 'enabled', True)
    
    @property
    def spotify_client_id(self) -> str:
        """Get Spotify client ID."""
        return self.get('spotify', 'client_id', '')
    
    @property
    def spotify_client_secret(self) -> str:
        """Get Spotify client secret."""
        return self.get('spotify', 'client_secret', '')
    
    @property
    def youtube_api_key(self) -> str:
        """Get YouTube API key."""
        return self.get('youtube', 'api_key', '')
    
    @property
    def use_youtube_music(self) -> bool:
        """Check if YouTube Music should be used."""
        return self.get_bool('youtube', 'use_youtube_music', True)
    
    @property
    def db_type(self) -> str:
        """Get database type."""
        return self.get('database', 'type', 'sqlite')
    
    @property
    def db_file(self) -> str:
        """Get SQLite database file path."""
        return self.get('database', 'db_file', 'data/bot.db')
    
    @property
    def log_file(self) -> str:
        """Get log file path."""
        return self.get('logging', 'log_file', 'bot.log')
    
    @property
    def log_level(self) -> str:
        """Get log level."""
        return self.get('logging', 'discord_log_level', 'INFO')
    
    @property
    def max_queue_size(self) -> int:
        """Get maximum queue size."""
        return self.get_int('queue', 'max_queue_size', 1000)
    
    @property
    def pre_extract(self) -> bool:
        """Check if pre-extraction is enabled."""
        return self.get_bool('playback', 'pre_extract', True)
    
    @property
    def preload_next(self) -> bool:
        """Check if next song preloading is enabled."""
        return self.get_bool('playback', 'preload_next', True)

    # ======================= MUSIC CONFIG PROPERTIES =======================

    @property
    def music_default_volume(self) -> int:
        """Get default music volume."""
        return self.get_int('volume', 'default_volume', 50)

    @property
    def music_min_volume(self) -> int:
        """Get minimum volume."""
        return self.get_int('volume', 'min_volume', 0)

    @property
    def music_max_volume(self) -> int:
        """Get maximum volume."""
        return self.get_int('volume', 'max_volume', 100)

    @property
    def music_audio_bitrate(self) -> int:
        """Get audio bitrate in kbps."""
        return self.get_int('audio_quality', 'audio_bitrate', 128)

    @property
    def music_sample_rate(self) -> int:
        """Get audio sample rate in Hz."""
        return self.get_int('audio_quality', 'sample_rate', 48000)

    @property
    def music_auto_play(self) -> bool:
        """Check if auto-play is enabled."""
        return self.get_bool('playback', 'auto_play', False)

    @property
    def music_default_repeat(self) -> str:
        """Get default repeat mode."""
        return self.get('playback', 'default_repeat', 'off')

    @property
    def music_default_shuffle(self) -> bool:
        """Check if shuffle is enabled by default."""
        return self.get_bool('playback', 'default_shuffle', False)

    @property
    def music_bass_boost_enabled(self) -> bool:
        """Check if bass boost is enabled."""
        return self.get_bool('filters', 'bass_boost_enabled', False)

    @property
    def music_bass_boost_level(self) -> int:
        """Get bass boost level."""
        return self.get_int('filters', 'bass_boost_level', 50)

    @property
    def music_nightcore_enabled(self) -> bool:
        """Check if nightcore effect is enabled."""
        return self.get_bool('filters', 'nightcore_enabled', False)

    @property
    def music_nightcore_speed(self) -> float:
        """Get nightcore speed multiplier."""
        return self.get_float('filters', 'nightcore_speed', 1.25)

    @property
    def music_equalizer_enabled(self) -> bool:
        """Check if equalizer is enabled."""
        return self.get_bool('equalizer', 'enabled', False)

    @property
    def music_equalizer_preset(self) -> str:
        """Get active equalizer preset."""
        return self.get('equalizer', 'active_preset', 'flat')

    @property
    def music_crossfade_enabled(self) -> bool:
        """Check if crossfade is enabled."""
        return self.get_bool('crossfade', 'enabled', False)

    @property
    def music_crossfade_duration(self) -> int:
        """Get crossfade duration in seconds."""
        return self.get_int('crossfade', 'duration', 3)

    @property
    def music_stop_fade_duration(self) -> int:
        """Get stop fade duration in seconds."""
        return self.get_int('fade', 'stop_fade_duration', 2)

    @property
    def music_max_queue_size(self) -> int:
        """Get maximum queue size."""
        return self.get_int('queue', 'max_queue_size', 1000)

    @property
    def music_allow_duplicates(self) -> bool:
        """Check if duplicate songs are allowed."""
        return self.get_bool('queue', 'allow_duplicates', True)

    @property
    def music_max_song_duration(self) -> int:
        """Get maximum song duration in seconds (0 = unlimited)."""
        return self.get_int('queue', 'max_song_duration', 0)

    @property
    def music_default_provider(self) -> str:
        """Get default search provider."""
        return self.get('search', 'default_provider', 'youtube_music')

    @property
    def music_max_search_results(self) -> int:
        """Get maximum search results."""
        return self.get_int('search', 'max_search_results', 5)

    @property
    def music_spotify_enabled(self) -> bool:
        """Check if Spotify is enabled."""
        return self.get_bool('search', 'spotify_enabled', True)

    @property
    def music_idle_timeout(self) -> int:
        """Get idle timeout in seconds."""
        return self.get_int('voice', 'idle_timeout', 300)

    @property
    def music_auto_disconnect_alone(self) -> bool:
        """Check if bot auto-disconnects when alone."""
        return self.get_bool('voice', 'auto_disconnect_alone', True)

    @property
    def music_history_enabled(self) -> bool:
        """Check if playback history is enabled."""
        return self.get_bool('history', 'enabled', True)

    @property
    def music_max_history_size(self) -> int:
        """Get maximum history size."""
        return self.get_int('history', 'max_history_size', 50)

    @property
    def music_pre_extract_enabled(self) -> bool:
        """Check if pre-extraction is enabled."""
        return self.get_bool('pre_extraction', 'enabled', True)

    @property
    def music_preload_next(self) -> bool:
        """Check if next song preload is enabled."""
        return self.get_bool('pre_extraction', 'preload_next', True)

    @property
    def music_use_youtube_music_api(self) -> bool:
        """Check if YTMusicAPI should be used."""
        return self.get_bool('performance', 'use_youtube_music_api', True)

    @property
    def music_low_latency(self) -> bool:
        """Check if low latency mode is enabled."""
        return self.get_bool('performance', 'low_latency', True)


# Global config instances
_config: Optional[Config] = None
_music_config: Optional[Config] = None


def get_config(config_file: Optional[Path] = None) -> Config:
    """
    Get the global configuration instance.
    
    Args:
        config_file: Optional path to config file
        
    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = Config(config_file)
    return _config


def get_music_config() -> Config:
    """
    Get the music-specific configuration instance.
    
    Returns:
        Config instance for music.ini
    """
    global _music_config
    if _music_config is None:
        music_config_file = CONFIG_DIR / 'music.ini'
        _music_config = Config(music_config_file)
    return _music_config


def reload_config() -> Config:
    """Reload configuration from file."""
    global _config, _music_config
    _config = Config()
    _music_config = Config(CONFIG_DIR / 'music.ini')
    return _config

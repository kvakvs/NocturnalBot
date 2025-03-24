import json
import os
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime, timedelta


class RaidCache:
    """
    Handles file-based caching of raid data with expiration.
    """

    def __init__(self, cache_dir: str = ".cache"):
        """
        Initialize the cache with a specified directory.

        Args:
            cache_dir (str): Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_duration = timedelta(hours=1)  # Cache expires after 1 hour

    def _get_cache_path(self, key: str) -> Path:
        """
        Get the cache file path for a specific key.

        Args:
            key (str): The key, something like "signup_1234567890" or "plan_1234567890"

        Returns:
            Path: Path to the cache file
        """
        return self.cache_dir / f"{key}.json"

    def get(self, key: str) -> Optional[Dict]:
        """
        Retrieve cached raid data if it exists and hasn't expired.

        Args:
            key (str): The key, something like "signup_1234567890" or "plan_1234567890"

        Returns:
            Optional[Dict]: Cached raid data if valid, None otherwise
        """
        cache_path = self._get_cache_path(key)

        if not cache_path.exists():
            return None

        try:
            # Check if cache has expired
            cache_time = datetime.fromtimestamp(cache_path.stat().st_mtime)
            if datetime.now() - cache_time > self.cache_duration:
                return None

            with open(cache_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None

    def set(self, key: str, data: Dict) -> None:
        """
        Cache raid data with current timestamp.

        Args:
            key (str): The key, something like "signup_1234567890" or "plan_1234567890"
            data (Dict): The raid data to cache
        """
        cache_path = self._get_cache_path(key)

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"Warning: Failed to cache raid data: {e}")

    def clear(self, key: Optional[str] = None) -> None:
        """
        Clear cache for a specific key or all keys.

        Args:
            key (Optional[str]): Specific key to clear, or None to clear all
        """
        if key:
            cache_path = self._get_cache_path(key)
            if cache_path.exists():
                cache_path.unlink()
        else:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()

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

    def _get_cache_path(self, raid_id: str) -> Path:
        """
        Get the cache file path for a specific raid ID.

        Args:
            raid_id (str): The raid ID

        Returns:
            Path: Path to the cache file
        """
        return self.cache_dir / f"raid_{raid_id}.json"

    def get(self, raid_id: str) -> Optional[Dict]:
        """
        Retrieve cached raid data if it exists and hasn't expired.

        Args:
            raid_id (str): The raid ID

        Returns:
            Optional[Dict]: Cached raid data if valid, None otherwise
        """
        cache_path = self._get_cache_path(raid_id)

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

    def set(self, raid_id: str, data: Dict) -> None:
        """
        Cache raid data with current timestamp.

        Args:
            raid_id (str): The raid ID
            data (Dict): The raid data to cache
        """
        cache_path = self._get_cache_path(raid_id)

        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
        except OSError as e:
            print(f"Warning: Failed to cache raid data: {e}")

    def clear(self, raid_id: Optional[str] = None) -> None:
        """
        Clear cache for a specific raid or all raids.

        Args:
            raid_id (Optional[str]): Specific raid ID to clear, or None to clear all
        """
        if raid_id:
            cache_path = self._get_cache_path(raid_id)
            if cache_path.exists():
                cache_path.unlink()
        else:
            for cache_file in self.cache_dir.glob("raid_*.json"):
                cache_file.unlink()
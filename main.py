#!/usr/bin/env python3

import requests
from typing import Dict, Optional

from raidassign.raidhelperbot.raid_event import RaidEvent
from raidassign.cache import RaidCache

def fetch_raid_data(raid_id: str, cache: Optional[RaidCache] = None) -> Optional[Dict]:
    """
    Fetch raid data from the Raid Helper API or cache.

    Args:
        raid_id (str): The ID of the raid event
        cache (Optional[RaidCache]): Cache instance to use for storing/retrieving data

    Returns:
        Optional[Dict]: The raid data as a dictionary if successful, None if failed
    """
    # Try to get data from cache first
    if cache:
        cached_data = cache.get(raid_id)
        if cached_data:
            print(f"Using cached data for raid {raid_id}")
            return cached_data

    # If no cache or cache miss, fetch from API
    base_url = "https://raid-helper.dev/api/v2/events"
    url = f"{base_url}/{raid_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # Cache the response if cache is available
        if cache:
            cache.set(raid_id, data)
            print(f"Cached data for raid {raid_id}")

        return data
    except requests.RequestException as e:
        print(f"Error fetching raid data: {e}")
        return None

def main():
    # Initialize cache
    cache = RaidCache()

    # Example usage
    raid_id = "1353459210448408607"
    raid_data = fetch_raid_data(raid_id, cache)
    if raid_data:
        evt = RaidEvent(json_data=raid_data)
        print(f"Successfully fetched raid data: {evt}")
    else:
        print("Failed to fetch raid data")

if __name__ == "__main__":
    main()

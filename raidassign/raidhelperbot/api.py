from typing import Dict, Optional

import requests

from raidassign.cache import RaidCache


def fetch_signup_data(raid_id: str, cache: Optional[RaidCache] = None) -> Optional[Dict]:
    """
    Fetch raid data from the Raid Helper API or cache.

    Args:
        raid_id (str): The ID of the raid event
        cache (Optional[RaidCache]): Cache instance to use for storing/retrieving data

    Returns:
        Optional[Dict]: The raid data as a dictionary if successful, None if failed
    """
    key = f"signup_{raid_id}"

    # Try to get data from cache first
    if cache:
        cached_data = cache.get(key)
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
            cache.set(key, data)
            print(f"Writing cache data for raid {raid_id}")

        return data
    except requests.RequestException as e:
        print(f"Error fetching raid data: {e}")
        return None


def fetch_raid_plan(raid_id: str, cache: Optional[RaidCache] = None) -> Optional[Dict]:
    """
    Fetch raid plan data from the Raid Helper API or cache.
    The URL is https://raid-helper.dev/api/raidplan/<raid id>

    Args:
        raid_id (str): The ID of the raid event
        cache (Optional[RaidCache]): Cache instance to use for storing/retrieving data

    Returns:
        Optional[Dict]: The raid plan data as a dictionary if successful, None if failed
    """
    # Try to get data from cache first
    key = f"plan_{raid_id}"
    if cache:
        cached_data = cache.get(key)  # Use a different cache key for plans
        if cached_data:
            print(f"Using cached plan data for raid {raid_id}")
            return cached_data

    # If no cache or cache miss, fetch from API
    base_url = "https://raid-helper.dev/api/raidplan"
    url = f"{base_url}/{raid_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()

        # Cache the response if cache is available
        if cache:
            cache.set(key, data)  # Use a different cache key for plans
            print(f"Writing raid-plan cache data for raid {raid_id}")

        return data
    except requests.RequestException as e:
        print(f"Error fetching raid plan data: {e}")
        return None

#!/usr/bin/env python3
"""
Get cities where people listen to an artist (Spotify data).

Usage:
    python get_artist_cities.py <chartmetric_id>
    python get_artist_cities.py 3380

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import sys
import json
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def get_artist_cities(cm_id: str) -> dict:
    """Fetch where people listen data from Chartmetric."""
    headers = get_auth_headers()
    
    response = requests.get(
        f"{API_BASE}/artist/{cm_id}/where-people-listen",
        headers=headers
    )
    
    if response.status_code == 402:
        return {"error": "Payment Required", "message": "Check your Chartmetric subscription."}
    
    if response.status_code == 404:
        return {"error": "Artist not found", "chartmetric_id": cm_id}
    
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_artist_cities.py <chartmetric_id>")
        sys.exit(1)
    
    result = get_artist_cities(sys.argv[1])
    
    if "error" in result:
        print(f"Error: {result.get('error')}")
        if "message" in result:
            print(result.get('message'))
        sys.exit(1)
    
    cities_data = result.get("obj", {}).get("cities", {})
    print(f"Top cities for this artist:\n")
    
    # Get latest listener count for each city
    city_latest = []
    for city_name, history in cities_data.items():
        if history and len(history) > 0:
            latest = history[-1]  # Most recent data point
            city_latest.append({
                "name": city_name,
                "country": latest.get("code2", ""),
                "listeners": latest.get("listeners", 0)
            })
    
    # Sort by listeners descending
    city_latest.sort(key=lambda x: x.get("listeners", 0), reverse=True)
    
    for city in city_latest[:20]:
        print(f"- {city.get('name', 'Unknown')}, {city.get('country', '')}")
        print(f"  Listeners: {city.get('listeners', 0):,}")
        print()

#!/usr/bin/env python3
"""
List all Chartmetric genres.

Usage:
    python list_genres.py

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import json
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def list_genres() -> dict:
    """Fetch all genres from Chartmetric."""
    headers = get_auth_headers()
    
    response = requests.get(
        f"{API_BASE}/genres",
        headers=headers
    )
    
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = list_genres()
    genres = result.get("obj", [])
    
    print(f"Found {len(genres)} genres:\n")
    for genre in genres[:50]:
        print(f"- {genre.get('name')} (ID: {genre.get('id')})")
    
    if len(genres) > 50:
        print(f"\n... and {len(genres) - 50} more")

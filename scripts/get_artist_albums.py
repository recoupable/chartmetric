#!/usr/bin/env python3
"""
Get artist's albums.

Usage:
    python get_artist_albums.py <chartmetric_id>
    python get_artist_albums.py 3380

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import sys
import json
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def get_artist_albums(cm_id: str) -> dict:
    """Fetch artist's albums from Chartmetric."""
    headers = get_auth_headers()
    
    response = requests.get(
        f"{API_BASE}/artist/{cm_id}/albums",
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
        print("Usage: python get_artist_albums.py <chartmetric_id>")
        sys.exit(1)
    
    result = get_artist_albums(sys.argv[1])
    
    if "error" in result:
        print(f"Error: {result.get('error')}")
        if "message" in result:
            print(result.get('message'))
        sys.exit(1)
    
    albums = result.get("obj", [])
    print(f"Found {len(albums)} albums:\n")
    for album in albums[:20]:  # Limit to first 20
        print(f"- {album.get('name')}")
        print(f"  Chartmetric ID: {album.get('id')}")
        print(f"  Release: {album.get('release_date', 'N/A')}")
        print()

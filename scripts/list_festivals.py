#!/usr/bin/env python3
"""
List music festivals.

Usage:
    python list_festivals.py

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import json
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def list_festivals() -> dict:
    """Fetch festival list from Chartmetric."""
    headers = get_auth_headers()
    
    response = requests.get(
        f"{API_BASE}/festival/list",
        headers=headers
    )
    
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    result = list_festivals()
    festivals = result.get("obj", [])
    
    print(f"Found {len(festivals)} festivals:\n")
    for fest in festivals[:30]:
        print(f"- {fest.get('name')}")
        if fest.get('city'):
            print(f"  Location: {fest.get('city')}, {fest.get('country', '')}")
        print()

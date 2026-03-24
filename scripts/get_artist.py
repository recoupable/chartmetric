#!/usr/bin/env python3
"""
Get artist profile by Chartmetric ID.

Usage:
    python get_artist.py <chartmetric_id>
    python get_artist.py 1234567

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import sys
import json
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def get_artist(cm_id: str) -> dict:
    """Fetch artist profile from Chartmetric."""
    headers = get_auth_headers()
    
    response = requests.get(
        f"{API_BASE}/artist/{cm_id}",
        headers=headers
    )
    
    if response.status_code == 402:
        return {
            "error": "Payment Required",
            "message": "Your Chartmetric API subscription may be expired or this endpoint requires a higher tier. Check your account at chartmetric.com or contact hi@chartmetric.com"
        }
    
    if response.status_code == 404:
        return {"error": "Artist not found", "chartmetric_id": cm_id}
    
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_artist.py <chartmetric_id>")
        sys.exit(1)
    
    result = get_artist(sys.argv[1])
    print(json.dumps(result, indent=2))

#!/usr/bin/env python3
"""
Get artist audience demographics for a platform.

Usage:
    python get_artist_audience.py <chartmetric_id> [--platform instagram]
    python get_artist_audience.py 3380
    python get_artist_audience.py 3380 --platform tiktok
    python get_artist_audience.py 3380 --platform youtube

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import sys
import json
import argparse
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def get_artist_audience(cm_id: str, platform: str = "instagram") -> dict:
    """Fetch artist audience demographics from Chartmetric."""
    headers = get_auth_headers()
    
    endpoint_map = {
        "instagram": f"{API_BASE}/artist/{cm_id}/instagram-audience-stats",
        "tiktok": f"{API_BASE}/artist/{cm_id}/tiktok-audience-stats",
        "youtube": f"{API_BASE}/artist/{cm_id}/youtube-audience-stats",
    }
    
    url = endpoint_map.get(platform)
    if not url:
        return {"error": f"Unknown platform: {platform}", "valid_platforms": list(endpoint_map.keys())}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 402:
        return {"error": "Payment Required", "message": "Check your Chartmetric subscription."}
    
    if response.status_code == 404:
        return {"error": "Artist not found or no audience data", "chartmetric_id": cm_id}
    
    response.raise_for_status()
    return response.json()


def main():
    parser = argparse.ArgumentParser(description="Get artist audience demographics")
    parser.add_argument("chartmetric_id", help="Chartmetric artist ID")
    parser.add_argument("--platform", "-p", default="instagram",
                        choices=["instagram", "tiktok", "youtube"],
                        help="Platform for audience data")
    
    args = parser.parse_args()
    result = get_artist_audience(args.chartmetric_id, args.platform)
    
    if "error" in result:
        print(f"Error: {result.get('error')}")
        if "message" in result:
            print(result.get('message'))
        sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()

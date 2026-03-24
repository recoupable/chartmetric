#!/usr/bin/env python3
"""
Get AI-generated noteworthy insights for an artist.

Usage:
    python get_artist_insights.py <chartmetric_id>
    python get_artist_insights.py 3380

Environment:
    CHARTMETRIC_BASE_URL + RECOUP_API_KEY - Proxy mode (recommended in Recoup sandboxes)
    CHARTMETRIC_REFRESH_TOKEN - Direct Chartmetric token (fallback if BASE_URL not set)
"""

import sys
import json
import requests
from get_auth import get_auth_headers, get_api_base

API_BASE = get_api_base()


def get_artist_insights(cm_id: str) -> dict:
    """Fetch noteworthy insights from Chartmetric."""
    headers = get_auth_headers()
    
    response = requests.get(
        f"{API_BASE}/artist/{cm_id}/noteworthy-insights",
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
        print("Usage: python get_artist_insights.py <chartmetric_id>")
        sys.exit(1)
    
    result = get_artist_insights(sys.argv[1])
    
    if "error" in result:
        print(f"Error: {result.get('error')}")
        if "message" in result:
            print(result.get('message'))
        sys.exit(1)
    
    insights = result.get("obj", [])
    print(f"Noteworthy Insights:\n")
    for insight in insights:
        print(f"• {insight.get('text', insight)}")
        print()

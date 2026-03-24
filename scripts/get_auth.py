#!/usr/bin/env python3
"""
Auth helper for Chartmetric API requests.

Supports two modes:
  1. Proxy mode (recommended in Recoup sandboxes): Set CHARTMETRIC_BASE_URL and RECOUP_API_KEY.
     Requests go through the Recoup API proxy, which handles token exchange and credit deduction.
  2. Direct mode (fallback): Set CHARTMETRIC_REFRESH_TOKEN.
     Requests go directly to api.chartmetric.com using a short-lived access token.
"""

import os


def get_auth_headers() -> dict:
    """Return auth headers for Chartmetric API requests.

    In proxy mode (CHARTMETRIC_BASE_URL set): returns {"x-api-key": <RECOUP_API_KEY>}.
    In direct mode (fallback): returns {"Authorization": "Bearer <access_token>"}.
    """
    if os.environ.get("CHARTMETRIC_BASE_URL"):
        api_key = os.environ.get("RECOUP_API_KEY")
        if not api_key:
            raise ValueError(
                "RECOUP_API_KEY environment variable not set "
                "(required when CHARTMETRIC_BASE_URL is set)"
            )
        return {"x-api-key": api_key}

    # Fall back to direct Chartmetric auth via refresh token
    from get_token import get_token

    return {"Authorization": f"Bearer {get_token()}"}


def get_api_base() -> str:
    """Return the Chartmetric API base URL.

    Uses CHARTMETRIC_BASE_URL if set (proxy mode), otherwise the direct Chartmetric API.
    """
    return os.environ.get("CHARTMETRIC_BASE_URL", "https://api.chartmetric.com/api")

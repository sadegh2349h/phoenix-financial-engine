#!/usr/bin/env python3
"""PHOENIX live Instagram acquisition smoke test via Apify."""
from __future__ import annotations

import json
import os
import sys
import urllib.parse
import urllib.request

PROFILE_URL = os.environ.get("INSTAGRAM_PROFILE_URL", "https://www.instagram.com/mahmoud_julaei/")
ACTOR = "apify~instagram-profile-scraper"
ENDPOINT = f"https://api.apify.com/v2/actors/{ACTOR}/run-sync-get-dataset-items"


def username_from_url(url: str) -> str:
    path = urllib.parse.urlparse(url).path.strip("/")
    if not path:
        raise ValueError("Instagram profile URL has no username")
    return path.split("/")[0].lstrip("@")


def main() -> int:
    token = os.environ.get("APIFY_API_TOKEN")
    if not token:
        print("APIFY_API_TOKEN is not configured", file=sys.stderr)
        return 2

    try:
        username = username_from_url(PROFILE_URL)
    except ValueError as exc:
        print(f"INVALID_PROFILE_URL: {exc}", file=sys.stderr)
        return 2

    payload = json.dumps({"usernames": [username]}).encode()
    endpoint = f"{ENDPOINT}?token={urllib.parse.quote(token, safe='')}"
    req = urllib.request.Request(
        endpoint,
        data=payload,
        method="POST",
        headers={"Content-Type": "application/json", "Accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            body = response.read().decode("utf-8", errors="replace")
            status = response.status
    except Exception as exc:
        print(f"APIFY_REQUEST_FAILED: {exc}", file=sys.stderr)
        return 1

    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        print("APIFY_RETURNED_NON_JSON", file=sys.stderr)
        return 1

    result = {
        "profile_url": PROFILE_URL,
        "actor": ACTOR,
        "http_status": status,
        "item_count": len(data) if isinstance(data, list) else None,
        "items": data,
    }
    os.makedirs("artifacts", exist_ok=True)
    safe_name = username.replace(".", "_")
    with open(f"artifacts/instagram_{safe_name}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    if not isinstance(data, list) or not data:
        print("APIFY_NO_PROFILE_DATA", file=sys.stderr)
        return 1

    print(json.dumps({"status": "success", "item_count": len(data), "profile_url": PROFILE_URL}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

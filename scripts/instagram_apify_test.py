#!/usr/bin/env python3
"""PHOENIX generic Instagram public-profile acquisition via Apify."""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.parse
import urllib.request

ACTOR = "apify~instagram-profile-scraper"
ENDPOINT = f"https://api.apify.com/v2/actors/{ACTOR}/run-sync-get-dataset-items"


def username_from_input(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("Instagram profile URL/username is empty")
    if not value.startswith(("http://", "https://")):
        value = "https://www.instagram.com/" + value.lstrip("@/")
    parsed = urllib.parse.urlparse(value)
    if parsed.netloc.lower() not in {"instagram.com", "www.instagram.com"}:
        raise ValueError("URL is not an Instagram profile URL")
    parts = [p for p in parsed.path.split("/") if p]
    if not parts:
        raise ValueError("Instagram profile URL has no username")
    username = parts[0].lstrip("@")
    if username.lower() in {"p", "reel", "reels", "tv", "stories", "explore", "accounts", "direct"}:
        raise ValueError("A post/reel/navigation URL was supplied; a profile URL is required")
    if not re.fullmatch(r"[A-Za-z0-9._]+", username):
        raise ValueError("Invalid Instagram username")
    return username


def main() -> int:
    profile_input = os.environ.get("INSTAGRAM_PROFILE_URL") or os.environ.get("INSTAGRAM_PROFILE")
    if not profile_input:
        print("INSTAGRAM_PROFILE_URL is required", file=sys.stderr)
        return 2
    token = os.environ.get("APIFY_API_TOKEN")
    if not token:
        print("APIFY_API_TOKEN is not configured", file=sys.stderr)
        return 2

    try:
        username = username_from_input(profile_input)
    except ValueError as exc:
        print(f"INVALID_PROFILE_URL: {exc}", file=sys.stderr)
        return 2

    normalized_url = f"https://www.instagram.com/{username}/"
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
        "profile_url": normalized_url,
        "requested_input": profile_input,
        "username": username,
        "actor": ACTOR,
        "http_status": status,
        "item_count": len(data) if isinstance(data, list) else None,
        "items": data,
    }
    os.makedirs("artifacts", exist_ok=True)
    with open(f"artifacts/instagram_{username.replace('.', '_')}.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    if not isinstance(data, list) or not data:
        print("APIFY_NO_PROFILE_DATA", file=sys.stderr)
        return 1

    print(json.dumps({"status": "success", "item_count": len(data), "profile_url": normalized_url}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

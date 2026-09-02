"""Public social profile evidence provider.

Fetches the ordinary public HTTP response only. It does not authenticate,
solve challenges, bypass robots/security controls, or access private data.
"""
from __future__ import annotations

import html
import re
from urllib.parse import urlparse

import requests

from .social_intelligence import SocialProfileInput


_META_RE = re.compile(
    r'<meta[^>]+(?:property|name)=["\']([^"\']+)["\'][^>]+content=["\']([^"\']*)["\']',
    re.I,
)
_FOLLOWERS_RE = re.compile(r'"(?:edge_followed_by|followers)"\s*:\s*\{"?count"?\s*:\s*(\d+)', re.I)
_POSTS_RE = re.compile(r'"(?:edge_owner_to_timeline_media|media)"\s*:\s*\{"?count"?\s*:\s*(\d+)', re.I)


def _meta(html_text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in _META_RE.findall(html_text):
        result.setdefault(key.lower(), html.unescape(value))
    return result


def fetch_public_social_profile(url: str, *, timeout: float = 12.0) -> SocialProfileInput | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url must be an absolute HTTP(S) URL")

    response = requests.get(
        url,
        timeout=timeout,
        allow_redirects=True,
        headers={"User-Agent": "Mozilla/5.0 (compatible; PHOENIX-PublicEvidence/1.0)"},
    )
    response.raise_for_status()
    text = response.text
    meta = _meta(text)

    title = meta.get("og:title") or meta.get("twitter:title")
    description = meta.get("og:description") or meta.get("description") or meta.get("twitter:description")
    if not title and not description:
        return None

    username = parsed.path.strip("/").split("/")[0] or None
    followers_match = _FOLLOWERS_RE.search(text)
    posts_match = _POSTS_RE.search(text)

    return SocialProfileInput(
        url=url,
        username=username,
        bio=description,
        followers=int(followers_match.group(1)) if followers_match else None,
        posts=int(posts_match.group(1)) if posts_match else None,
    )

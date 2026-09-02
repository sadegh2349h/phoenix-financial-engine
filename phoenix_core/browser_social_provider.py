"""Optional browser-based public social evidence provider.

Uses a normal browser visit to a public URL only. No login, credential bypass,
challenge solving, or private-data access is performed. Playwright is optional
so the core package remains lightweight.
"""
from __future__ import annotations

import re
from urllib.parse import urlparse

from .social_intelligence import SocialProfileInput


def fetch_public_social_profile_browser(
    url: str, *, timeout_ms: int = 15000
) -> SocialProfileInput | None:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("url must be an absolute HTTP(S) URL")

    try:
        from playwright.sync_api import sync_playwright
    except ImportError as exc:
        raise RuntimeError("optional dependency 'playwright' is not installed") from exc

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(user_agent=(
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/128 Safari/537.36"
            ))
            page.goto(url, wait_until="domcontentloaded", timeout=timeout_ms)
            title = page.title()
            description = page.locator('meta[name="description"]').get_attribute("content")
            og_description = page.locator('meta[property="og:description"]').get_attribute("content")
            bio = description or og_description or title
            if not bio:
                return None
            username = parsed.path.strip("/").split("/")[0] or None
            body = page.locator("body").inner_text(timeout=5000)
            followers = None
            posts = None
            follower_match = re.search(r"([\d,.]+)\s*(?:followers|فالوور)", body, re.I)
            post_match = re.search(r"([\d,.]+)\s*(?:posts|پست)", body, re.I)
            if follower_match:
                followers = int(follower_match.group(1).replace(",", "").replace(".", ""))
            if post_match:
                posts = int(post_match.group(1).replace(",", "").replace(".", ""))
            return SocialProfileInput(
                url=url, username=username, bio=bio,
                followers=followers, posts=posts,
            )
        finally:
            browser.close()

# PHOENIX Social Gateway

The social acquisition gateway uses ordered, fail-closed routes:

1. official API (authorized only)
2. authorized provider (authorized only)
3. public HTTP evidence
4. public browser evidence (optional Playwright dependency)
5. user-supplied evidence
6. visual capture

No route logs in, bypasses credentials, solves security challenges, or claims private metrics without authorization. Each acquired profile is passed to the PHOENIX Social Intelligence Engine with explicit evidence coverage and human decision ownership.

The repository also contains a live workflow for the public profile test target `eynak_rosee`.

## GitHub ecosystem findings

`subzeroid/instagrapi` is a mature Python Instagram client with a strong GitHub signal, but it targets Instagram's private API and therefore is not adopted as the default PHOENIX route. It can be evaluated later only as an explicitly authorized adapter.

`rajab-bett-analytics/Instagram-Profile-Scraper` demonstrates a Playwright browser-automation approach for public Instagram evidence, but its current community signal is small. PHOENIX adopts the browser pattern as an optional provider boundary rather than copying the project wholesale.

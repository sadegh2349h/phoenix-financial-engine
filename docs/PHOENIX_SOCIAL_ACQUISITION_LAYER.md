# PHOENIX Social Acquisition Layer

The acquisition contract sits between social sources and the PHOENIX Social Intelligence Engine.

## Route priority
1. Official API — authorized credentials required.
2. Authorized provider adapter — compliant provider connection required.
3. Public evidence — only legitimately available public evidence.
4. User-supplied structured data.
5. Visual capture such as screenshots/video supplied by the user.

## Governance
- No credential bypass.
- No unauthorized scraping.
- No fabricated followers, reach, engagement, Insights, or content metrics.
- Preserve source and confidence for every metric.
- Human review remains mandatory for consequential business decisions.

## Current state
The acquisition contract and tests are implemented. No Instagram credential or authorized provider connection is stored in the repository, so authenticated retrieval is intentionally disabled by default. An authorized adapter can be injected into `acquire_social_profile()` without changing the intelligence engine.

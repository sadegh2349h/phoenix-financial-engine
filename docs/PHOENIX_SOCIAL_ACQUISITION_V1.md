# PHOENIX Social Acquisition Layer V1

Acquisition contract for social-profile intelligence.

Routes: official API (authorized), authorized provider adapter, public evidence, user-supplied structured data, visual capture.

Governance: no credential bypass, no unauthorized scraping, no fabricated metrics; preserve source/confidence; human review required for consequential decisions.

Current implementation deliberately does not store Instagram credentials. Authenticated retrieval is enabled only by injecting an authorized provider adapter into `acquire_social_profile()`.

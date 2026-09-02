# PHOENIX Social Acquisition Status

Implemented:
- Provider-agnostic acquisition contract.
- Explicit route priorities.
- Authorized adapter injection point.
- User-supplied evidence path.
- Explicit fallback when no authorized source is connected.
- Contract tests.

Not enabled:
- Direct authenticated Instagram retrieval, because no authorized Instagram provider/credential is configured in the repository.

This prevents PHOENIX from claiming it can read private or unavailable Instagram data when it cannot.

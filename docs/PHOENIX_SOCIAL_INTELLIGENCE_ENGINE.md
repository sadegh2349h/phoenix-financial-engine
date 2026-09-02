# PHOENIX Social Intelligence Engine

## Purpose

A core capability for turning an Instagram profile or other social-profile evidence into an evidence-backed business diagnosis. It is provider-agnostic and does not depend on direct platform scraping.

## Evidence hierarchy

1. Authorized platform/provider data
2. Publicly available profile/content data
3. User-supplied screenshots, exports, transcripts and media
4. Structured samples supplied by the client

If a source is unavailable, the engine uses the available fallback path and explicitly records coverage/confidence. It must never invent unavailable metrics.

## Pipeline

`URL → source discovery → evidence normalization → profile analysis → content analysis → performance analysis → competitor signals → funnel analysis → business diagnosis → growth opportunities → experiment → human decision`

The current code provides the provider-agnostic evidence model, profile/content coverage, confidence tracking, business-bottleneck hypotheses, and orchestrator integration. Provider-specific collectors can be added later behind this boundary.

## Business diagnosis contract

Every diagnosis follows:

`وضعیت فعلی → گلوگاه → شواهد → فرضیه → اقدام → KPI → نتیجه → یادگیری`

A hypothesis is not presented as a fact. Confidence is evidence coverage, not certainty.

## PHOENIX governance

- Human decision remains mandatory for consequential actions.
- No unauthorized scraping or private-data access.
- No psychological diagnosis from social content.
- No claims about metrics that were not observed or supplied.
- Provider integrations must fail closed to the native/fallback path.
- New collectors require tests, source attribution and rollback capability.

## Orchestrator

When `social_profile` is supplied to `build_execution_plan`, the orchestrator activates `PHOENIX Social Intelligence Engine`, includes its business diagnosis as routing evidence, and returns the full social intelligence package.

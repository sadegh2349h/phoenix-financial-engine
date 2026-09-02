# PHOENIX Social Acquisition — Final V1

## Result
The social acquisition layer is now present in the PHOENIX codebase. It exposes a stable acquisition contract and keeps the intelligence engine independent from any specific provider.

## Safety and accuracy
Only authorized adapters, public evidence, or user-supplied evidence may populate the analysis. No unavailable Instagram metric is inferred or fabricated.

## Integration point
Use `acquire_social_profile()` / `analyze_social_url()` from `phoenix_core.social_acquisition_layer`.

## Remaining external dependency
To make a raw Instagram URL automatically resolve into live authenticated profile/Insights data, an authorized Instagram/Meta provider connection must be configured. The code is ready for that adapter; credentials are not embedded in source control.

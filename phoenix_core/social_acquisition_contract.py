"""Stable public contract for PHOENIX social acquisition."""
from .social_acquisition_layer import (
    AcquisitionResult,
    acquisition_routes,
    acquire_social_profile,
    analyze_social_url,
    validate_social_url,
)

__all__ = [
    "AcquisitionResult",
    "acquisition_routes",
    "acquire_social_profile",
    "analyze_social_url",
    "validate_social_url",
]

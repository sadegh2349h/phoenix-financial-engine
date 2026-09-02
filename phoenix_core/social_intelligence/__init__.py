"""Namespace for PHOENIX social intelligence capabilities."""

from ..social_intelligence import (
    SocialEvidence,
    SocialProfileInput,
    analyze_profile,
    build_social_business_diagnosis,
    build_social_intelligence_package,
)

__all__ = [
    "SocialEvidence",
    "SocialProfileInput",
    "analyze_profile",
    "build_social_business_diagnosis",
    "build_social_intelligence_package",
]

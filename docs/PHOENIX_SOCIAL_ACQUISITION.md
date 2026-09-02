# PHOENIX Social Acquisition Layer

## Purpose

Provide a safe acquisition contract between a social-profile URL and PHOENIX Social Intelligence.

## Source priority

1. Official/authorized API
2. Public data that is legally and technically accessible
3. User-supplied profile/export data
4. Visual evidence such as screenshots or screen recordings
5. Authorized platform Insights

## Safety boundary

PHOENIX must not access private data, bypass credentials or platform controls, or make claims about unavailable metrics. Every acquired field must retain its source and confidence.

## Pipeline

URL -> Acquisition Orchestrator -> Evidence Normalizer -> Social Intelligence -> Business Diagnosis -> Growth Opportunities -> Experiments -> Human Decision

## Current status

The Social Intelligence Engine is implemented. This document defines the acquisition boundary and adapter contract; a live Instagram connector still requires a supported official/authorized data access path or supplied evidence.

from __future__ import annotations

import os
from typing import Any

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from .api import PhoenixService

app = FastAPI(title="PHOENIX API", version="0.1.0")
service = PhoenixService()


class AnalysisRequest(BaseModel):
    objective: str = Field(min_length=1, max_length=2000)
    capability: str = Field(min_length=1, max_length=200)
    context: dict[str, Any] = Field(default_factory=dict)


def require_api_key(x_api_key: str | None = Header(default=None)) -> None:
    configured = os.getenv("PHOENIX_API_KEY")
    if configured and x_api_key != configured:
        raise HTTPException(status_code=401, detail="invalid API key")


@app.get("/health")
def health() -> dict[str, Any]:
    return service.health()


@app.post("/v1/analyze")
def analyze(request: AnalysisRequest, _: None = Depends(require_api_key)) -> dict[str, Any]:
    return service.analyze(request.objective, request.capability, request.context)

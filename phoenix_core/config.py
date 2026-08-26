import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    environment: str = os.getenv("PHOENIX_ENV", "development")
    log_level: str = os.getenv("PHOENIX_LOG_LEVEL", "INFO")
    data_retention_days: int = int(os.getenv("PHOENIX_DATA_RETENTION_DAYS", "3650"))
    require_human_approval: bool = os.getenv("PHOENIX_REQUIRE_HUMAN_APPROVAL", "true").lower() == "true"


settings = Settings()

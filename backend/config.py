import os
from pydantic import BaseModel

class Settings(BaseModel):
    PROJECT_NAME: str = "CareAuth-ROCm"
    VERSION: str = "1.0.0"
    TRACK: str = "Track 2: Health & Wellbeing (Vibe Generation) + Evolus Partner Track"
    
    # AMD Cloud Endpoint
    AMD_ROCM_ENDPOINT: str = os.getenv("AMD_ROCM_ENDPOINT", "http://localhost:8000/v1")
    AMD_API_KEY: str = os.getenv("AMD_API_KEY", "amd-developer-cloud-token")
    AMD_MODEL_NAME: str = os.getenv("AMD_MODEL_NAME", "meta-llama/Llama-3.1-8B-Instruct")
    
    # Evolus Platform Settings
    EVOLUS_API_KEY: str = os.getenv("EVOLUS_API_KEY", "")
    EVOLUS_WORKSPACE_ID: str = os.getenv("EVOLUS_WORKSPACE_ID", "")
    EVOLUS_BASE_URL: str = os.getenv("EVOLUS_BASE_URL", "https://api.evolus.ai/v1")
    
    # Operational Modes
    USE_OFFLINE_MOCK: bool = os.getenv("USE_OFFLINE_MOCK", "true").lower() in ("true", "1", "yes")
    HIPAA_STRICT_MODE: bool = True
    
    # Uncertainty Thresholds
    AUTO_APPROVE_THRESHOLD: float = 0.85  # >= 85% match is auto-approved
    ESCALATE_THRESHOLD: float = 0.70      # < 70% requires immediate doctor escalation

settings = Settings()

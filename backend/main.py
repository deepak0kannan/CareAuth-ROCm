import os
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, Optional

from backend.config import settings
from backend.phi_sanitizer import phi_sanitizer
from backend.evolus_client import evolus_client
from backend.amd_telemetry import amd_telemetry
from backend.agents.extractor_agent import extractor_agent
from backend.agents.adjudicator_agent import adjudicator_agent
from backend.agents.appeal_agent import appeal_agent

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="CareAuth-ROCm: Autonomous Healthcare Prior-Authorization & Payer-Policy Adjudication Agent"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AdjudicationRequest(BaseModel):
    document_text: str
    case_key: Optional[str] = "case1"

class SignOffRequest(BaseModel):
    case_id: str
    physician_name: str
    action: str  # "APPROVED_SUBMIT" or "FLAGGED_FOR_CLINIC"
    notes: Optional[str] = ""

# Serve Mock Case Data
MOCK_DIR = os.path.join(os.path.dirname(__file__), "..", "mock_data")

def load_mock_file(filename: str) -> str:
    path = os.path.join(MOCK_DIR, filename)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "track": settings.TRACK,
        "amd_hardware": "AMD Instinct MI300X (192GB HBM3)",
        "offline_mock_mode": settings.USE_OFFLINE_MOCK
    }

@app.get("/api/cases")
def list_demo_cases():
    """
    Returns the 3 Golden Demo Scenarios required for the Hackathon Track 2 Demonstration.
    """
    return [
        {
            "id": "case1",
            "title": "Case 1: Knee Arthroscopy (Clean Auto-Approval)",
            "subtitle": "Anthem CG-SURG-01 | Meniscus Tear + 6 Mo PT Verified",
            "procedure": "CPT 29881 — Partial Meniscectomy",
            "expected_outcome": "AUTO_APPROVED",
            "confidence_expected": "96%",
            "color": "emerald",
            "content": load_mock_file("case1_knee_arthroscopy_approved.md")
        },
        {
            "id": "case2",
            "title": "Case 2: Biologic Humira (Step-Therapy Gap Detected)",
            "subtitle": "Medicare LCD L33777 | Missing Methotrexate Trial ➔ Yellow Alert",
            "procedure": "HCPCS J0135 — Adalimumab 40mg",
            "expected_outcome": "HUMAN_REVIEW_REQUIRED",
            "confidence_expected": "64%",
            "color": "amber",
            "content": load_mock_file("case2_humira_missing_step_therapy.md")
        },
        {
            "id": "case3",
            "title": "Case 3: Complex Transfer (Prior Denial Overturn Appeal)",
            "subtitle": "Medicare LCD §4.2.1 | Statutory Transaminitis Exemption Applied",
            "procedure": "Tertiary Transfer & Specialized Biologic",
            "expected_outcome": "APPEAL_SIGN_OFF_READY",
            "confidence_expected": "92%",
            "color": "indigo",
            "content": load_mock_file("case3_denied_transfer_appeal.md")
        }
    ]

@app.post("/api/phi-sanitize")
def sanitize_phi(payload: Dict[str, str] = Body(...)):
    text = payload.get("text", "")
    return phi_sanitizer.sanitize(text)

@app.get("/api/telemetry")
def get_telemetry():
    return amd_telemetry.get_current_metrics()

@app.post("/api/adjudicate")
async def process_prior_auth(req: AdjudicationRequest):
    """
    Runs the full 4-Agent Autonomous Workflow:
    1. Local HIPAA PHI Sanitization
    2. Evolus Event Workflow Execution
    3. Document Extractor Agent
    4. Policy Adjudicator Agent (Evidence Gap & Confidence Matrix)
    5. Appeal & Packet Drafter Agent (Dual Output: Formal Insurer + Patient-Friendly Multilingual)
    """
    raw_text = req.document_text
    if not raw_text.strip():
        raise HTTPException(status_code=400, detail="Empty clinical document provided.")

    # 1. Local PHI Sanitization
    phi_result = phi_sanitizer.sanitize(raw_text)
    sanitized_text = phi_result["sanitized_text"]

    # 2. Evolus Workflow Coordination
    evolus_result = await evolus_client.execute_business_workflow(sanitized_text)

    # 3. Clinical Data Extraction Agent
    extracted_data = extractor_agent.extract(sanitized_text)

    # 4. Policy Adjudication & Uncertainty Engine
    adjudication_data = adjudicator_agent.adjudicate(extracted_data)

    # 5. Dual-Output Packet Generation Agent
    packets = appeal_agent.generate_packet(extracted_data, adjudication_data)

    # 6. AMD Telemetry Snapshot
    telemetry_snapshot = amd_telemetry.get_current_metrics()

    return {
        "success": True,
        "phi_audit": phi_result,
        "evolus_trace": evolus_result,
        "extracted_clinical_facts": extracted_data,
        "adjudication_analysis": adjudication_data,
        "generated_packets": packets,
        "amd_hardware_telemetry": telemetry_snapshot
    }

@app.post("/api/sign-off")
def submit_sign_off(payload: SignOffRequest):
    """
    Handles Human-in-the-Loop 1-Click Electronic Approval or Nurse Follow-up Flag.
    """
    return {
        "success": True,
        "case_id": payload.case_id,
        "physician_sign_off": f"/s/ {payload.physician_name}",
        "action": payload.action,
        "status": "TRANSMITTED_TO_PAYER_CLEARINGHOUSE",
        "timestamp": "2026-10-17T12:00:00Z",
        "message": f"Case {payload.case_id} successfully signed and transmitted to electronic payer gateway."
    }

# Mount static frontend
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")
if not os.path.exists(FRONTEND_DIR):
    os.makedirs(FRONTEND_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "CareAuth-ROCm Backend Active. UI building..."})

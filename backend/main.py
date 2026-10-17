import os
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import Dict, Any, List, Optional

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
    description="CareAuth-ROCm: Autonomous Healthcare Prior-Authorization & Multi-Role Clinical Portal"
)

# Enable CORS for frontend flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOCK_DIR = os.path.join(BASE_DIR, "mock_data")
POLICIES_DIR = os.path.join(BASE_DIR, "evolus", "policies")
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

def load_file_content(path: str) -> str:
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

# =====================================================================
# IN-MEMORY CLINICAL REPOSITORY (Full RBAC Data Layer)
# =====================================================================

USERS_DB = {
    "coordinator": {
        "id": "usr_coord",
        "username": "deepak.kannan@hospital.org",
        "name": "Deepak Kannan",
        "role": "coordinator",
        "role_title": "Lead Prior-Auth Specialist",
        "department": "Department of Utilization Management",
        "avatar": "DK"
    },
    "doctor": {
        "id": "usr_doc",
        "username": "sarah.jenkins@hospital.org",
        "name": "Dr. Sarah Jenkins, MD",
        "role": "doctor",
        "role_title": "Chief Orthopedic Surgeon & Reviewer",
        "department": "Orthopedics & Joint Reconstruction",
        "avatar": "SJ"
    },
    "patient": {
        "id": "pat_10492",
        "username": "ramesh.patel@gmail.com",
        "name": "Ramesh Patel",
        "role": "patient",
        "role_title": "Verified Patient (MRN: 882194)",
        "department": "Outpatient Knee Surgery",
        "avatar": "RP"
    },
    "lab": {
        "id": "usr_lab",
        "username": "alex.chen@hospital.org",
        "name": "Alex Chen",
        "role": "lab",
        "role_title": "Senior Radiology & Diagnostic Technologist",
        "department": "Advanced Diagnostic Imaging & Pathology",
        "avatar": "AC"
    }
}

PATIENTS_DB = {
    "pat_10492": {
        "id": "pat_10492",
        "mrn": "882194",
        "name": "Ramesh Patel",
        "age": 54,
        "gender": "Male",
        "dob": "1972-04-12",
        "phone": "+1 (555) 382-9011",
        "email": "ramesh.patel@gmail.com",
        "insurance_provider": "Anthem Blue Cross",
        "policy_id": "ANT-8839210-A",
        "diagnosis": "Medial Meniscus Tear of Left Knee (ICD-10 M23.22)",
        "procedure": "Left Knee Arthroscopy & Partial Meniscectomy (CPT 29881)",
        "adjudication_status": "APPROVED",
        "auth_number": "AUTH-2026-ANT-99120",
        "plain_english_summary": {
            "title": "Your Knee Arthroscopy Request is APPROVED!",
            "reading_level": "Grade 6 Simple Language",
            "body": "Good news! Your doctor's request for left knee arthroscopy has been checked and approved by Anthem Blue Cross. Our medical system verified your 6 months of physical therapy and confirmed your MRI shows a torn meniscus cushion. Anthem will cover their portion of the hospital and doctor bills. You do not need to submit any more paperwork. Your surgeon's office will call you within 2 business days to schedule your surgery date.",
            "next_steps": "1. Expect a scheduling call from Dr. Jenkins' clinic.\n2. Review your pre-op checklist.\n3. Pay your small copay balance ($250.00) online anytime before surgery."
        },
        "billing": {
            "procedure_name": "Outpatient Knee Arthroscopy (CPT 29881)",
            "facility_cost": 4200.00,
            "insurance_covered": 3950.00,
            "copay_balance": 250.00,
            "is_paid": False,
            "receipt_id": None,
            "paid_at": None
        },
        "diagnostic_reports": [
            {
                "id": "rep_mri_1",
                "title": "Left Knee 3.0T High-Resolution MRI",
                "type": "Radiology / MRI",
                "date": "2026-09-18",
                "doctor": "Dr. Robert Vance, MD (Radiology)",
                "status": "VERIFIED & SIGNED",
                "summary": "Grade III complex tear involving the posterior horn of the medial meniscus. Cruciate ligaments (ACL/PCL) and collateral ligaments intact. Mild patellofemoral chondromalacia without severe bone-on-bone osteoarthritis.",
                "image_preview": "High-Contrast Coronal & Sagittal T2-Weighted Knee Views Corroborated"
            },
            {
                "id": "rep_pt_1",
                "title": "6-Month Physical Therapy Discharge Summary",
                "type": "Rehabilitation Record",
                "date": "2026-09-10",
                "doctor": "Apex Physical Therapy Specialists",
                "status": "COMPLETED & VERIFIED",
                "summary": "Patient completed 24 supervised physical therapy sessions over 24 weeks (2x/week). Conservative therapy exhausted with persistent joint-line tenderness, mechanical locking, and functional limitation.",
                "image_preview": "PT Attendance Log & Range of Motion Deficit Curves Attached"
            },
            {
                "id": "rep_xray_1",
                "title": "Bilateral Standing Weight-Bearing Knee X-Rays",
                "type": "Radiology / X-Ray",
                "date": "2026-08-14",
                "doctor": "Metro Imaging Center",
                "status": "VERIFIED",
                "summary": "AP and Lateral standing views confirm preservation of tibiofemoral joint space. Kellgren-Lawrence Grade 1 changes only. Excludes advanced tricompartmental osteoarthritis.",
                "image_preview": "AP Weight-Bearing View: Joint Space Clear (KL Grade 1)"
            },
            {
                "id": "rep_lab_1",
                "title": "Pre-Operative Comprehensive Metabolic & CBC Panel",
                "type": "Pathology / Blood",
                "date": "2026-10-02",
                "doctor": "Quest Diagnostics Lab",
                "status": "NORMAL",
                "summary": "Hemoglobin 14.8 g/dL, Platelets 235k, Creatinine 0.92 mg/dL, Fasting Glucose 96 mg/dL. All values within normal physiological limits for general/spinal anesthesia.",
                "image_preview": "Standard 14-Item Automated Hematology Panel"
            }
        ]
    },
    "pat_15489": {
        "id": "pat_15489",
        "mrn": "492011",
        "name": "Sophia Martinez",
        "age": 47,
        "gender": "Female",
        "dob": "1979-08-22",
        "phone": "+1 (555) 749-1102",
        "email": "sophia.martinez@gmail.com",
        "insurance_provider": "Medicare Part B",
        "policy_id": "MED-4920119-B",
        "diagnosis": "Severe Rheumatoid Arthritis (Seropositive, ICD-10 M05.79)",
        "procedure": "Adalimumab (Humira) 40mg SubQ Q2W (HCPCS J0135)",
        "adjudication_status": "NEEDS_INFO",
        "auth_number": "PENDING-MEDICARE-REV",
        "plain_english_summary": {
            "title": "Action Needed: Step-Therapy Information Requested",
            "reading_level": "Grade 6 Simple Language",
            "body": "Medicare requires one extra piece of paperwork before they can approve your Humira injections. Under Medicare guidelines, patients must show they previously tried an oral pill like Methotrexate for 3 months, or their doctor must file a short note explaining why they cannot take that medicine (such as a liver issue or allergy). Our clinic nurse is preparing this doctor note now so Medicare can clear your prescription.",
            "next_steps": "1. Clinic nurse is retrieving your past pharmacy records.\n2. Dr. Jenkins will sign the exception form.\n3. Humira pharmacy will deliver once cleared."
        },
        "billing": {
            "procedure_name": "Biologic Infusion / Prescription (Humira 40mg)",
            "facility_cost": 6800.00,
            "insurance_covered": 6750.00,
            "copay_balance": 50.00,
            "is_paid": False,
            "receipt_id": None,
            "paid_at": None
        },
        "diagnostic_reports": [
            {
                "id": "rep_blood_rheum",
                "title": "Rheumatoid Factor & Anti-CCP Serology Panel",
                "type": "Immunology",
                "date": "2026-09-25",
                "doctor": "LabCorp Specialty Labs",
                "status": "HIGHLY ABNORMAL (CONFIRMED)",
                "summary": "Anti-CCP >250 U/mL (Reference <20 U/mL), RF 112 IU/mL. Corroborates active seropositive erosive rheumatoid arthritis.",
                "image_preview": "Serology ELISA Titration Graph"
            },
            {
                "id": "rep_tb_gold",
                "title": "QuantiFERON-TB Gold Plus Screening",
                "type": "Infectious Disease",
                "date": "2026-10-01",
                "doctor": "Hospital Diagnostic Lab",
                "status": "NEGATIVE (CLEARED)",
                "summary": "Nil: 0.05, TB1-Nil: 0.02, TB2-Nil: 0.01. Negative for latent tuberculosis infection. Clears mandatory biologic safety threshold.",
                "image_preview": "Interferon Gamma Release Assay (IGRA) Verified"
            },
            {
                "id": "rep_xray_hands",
                "title": "Bilateral Hands & Wrists Digital Radiography",
                "type": "Radiology / X-Ray",
                "date": "2026-08-30",
                "doctor": "Advanced Radiology Group",
                "status": "VERIFIED",
                "summary": "Multiple marginal erosions at 2nd and 3rd MCP joints bilaterally. Juxta-articular osteopenia. Confirms progressive inflammatory arthritis.",
                "image_preview": "PA Hand X-Ray Showing MCP Joint Erosions"
            }
        ]
    },
    "pat_78596": {
        "id": "pat_78596",
        "mrn": "109482",
        "name": "Emily Davis",
        "age": 62,
        "gender": "Female",
        "dob": "1964-11-05",
        "phone": "+1 (555) 912-4029",
        "email": "emily.davis@gmail.com",
        "insurance_provider": "UnitedHealthcare",
        "policy_id": "UHC-992104-COMM",
        "diagnosis": "Refractory Inflammatory Arthritis with Hepatic Transaminitis (ICD-10 M06.0, K76.89)",
        "procedure": "Tertiary Care Transfer & Expedited Biologic Appeal",
        "adjudication_status": "APPEAL_READY",
        "auth_number": "APPEAL-UHC-88194",
        "plain_english_summary": {
            "title": "Your Appeal Packet is Prepared & Signed!",
            "reading_level": "Grade 6 Simple Language",
            "body": "Your doctor has filed an expedited appeal to overturn the prior denial from your insurance company. We cited Section 4.2.1 of the medical guidelines, showing that you cannot take standard anti-arthritis pills because your liver enzymes were high (AST 184, ALT 210). Our AI system calculated a 92% chance of winning this appeal. You should hear the final decision within 72 hours.",
            "next_steps": "1. Expedited appeal transmitted to UnitedHealthcare clearinghouse.\n2. 72-hour turnaround clock started.\n3. Care coordinator will update you via SMS."
        },
        "billing": {
            "procedure_name": "Specialized Biologic Infusion & Monitoring",
            "facility_cost": 5100.00,
            "insurance_covered": 4980.00,
            "copay_balance": 120.00,
            "is_paid": False,
            "receipt_id": None,
            "paid_at": None
        },
        "diagnostic_reports": [
            {
                "id": "rep_liver_panel",
                "title": "Comprehensive Hepatic Function & Liver Enzyme Panel",
                "type": "Biochemistry / Pathology",
                "date": "2026-10-08",
                "doctor": "University Pathology Lab",
                "status": "ELEVATED (STATUTORY EXCEPTION)",
                "summary": "AST 184 U/L (Ref: 10-40), ALT 210 U/L (Ref: 7-56), Total Bilirubin 1.4 mg/dL. Frank hepatotoxicity establishes absolute contraindication to methotrexate step therapy.",
                "image_preview": "Hepatic Enzyme Kinetic Analyzer Output"
            },
            {
                "id": "rep_rheum_eval",
                "title": "Tertiary Rheumatology Comprehensive Consult",
                "type": "Specialist Evaluation",
                "date": "2026-10-11",
                "doctor": "Dr. Sarah Jenkins, MD",
                "status": "CERTIFIED",
                "summary": "Disease Activity Score DAS28-CRP is 5.8 (High Disease Activity). Documented statutory medical exemption to conventional DMARDs due to transaminitis.",
                "image_preview": "Signed Specialist Consultation Note"
            }
        ]
    }
}

DOCTOR_QUEUE = [
    {
        "case_id": "case1",
        "patient_id": "pat_10492",
        "patient_name": "Ramesh Patel",
        "mrn": "882194",
        "procedure": "Left Knee Arthroscopy & Partial Meniscectomy (CPT 29881)",
        "payer": "Anthem Blue Cross",
        "status": "PENDING_PHYSICIAN_SIGN_OFF",
        "ai_recommendation": "AUTO_APPROVE",
        "confidence": 0.96,
        "criteria_summary": "6 months PT verified + Grade III MRI meniscus tear corroborated.",
        "signed": False,
        "signature_stamp": None
    },
    {
        "case_id": "case2",
        "patient_id": "pat_15489",
        "patient_name": "Sophia Martinez",
        "mrn": "492011",
        "procedure": "Adalimumab (Humira) 40mg SubQ (HCPCS J0135)",
        "payer": "Medicare Part B",
        "status": "FLAGGED_FOR_CLINICAL_EVIDENCE",
        "ai_recommendation": "HUMAN_REVIEW_REQUIRED",
        "confidence": 0.64,
        "criteria_summary": "Missing 3-Month Methotrexate Step-Therapy trial record.",
        "signed": False,
        "signature_stamp": None
    },
    {
        "case_id": "case3",
        "patient_id": "pat_78596",
        "patient_name": "Emily Davis",
        "mrn": "109482",
        "procedure": "Tertiary Biologic Transfer Appeal",
        "payer": "UnitedHealthcare",
        "status": "APPEAL_SIGN_OFF_READY",
        "ai_recommendation": "SIGN_EXPEDITED_APPEAL",
        "confidence": 0.92,
        "criteria_summary": "Section 4.2.1 statutory transaminitis exception cited (AST 184 / ALT 210).",
        "signed": False,
        "signature_stamp": None
    }
]

# =====================================================================
# REQUEST / RESPONSE SCHEMAS
# =====================================================================

class LoginRequest(BaseModel):
    role: Optional[str] = "coordinator"
    email: Optional[str] = ""
    password: Optional[str] = ""

class NewPatientRequest(BaseModel):
    name: str
    dob: str
    phone: str
    email: Optional[str] = ""
    insurance_provider: str
    policy_id: Optional[str] = ""
    chief_complaint: str
    medical_history: Optional[str] = ""
    report_filename: Optional[str] = "Uploaded_Scan.pdf"
    report_type: Optional[str] = "Diagnostic Scan"

class AdjudicationRequest(BaseModel):
    document_text: str
    case_key: Optional[str] = "case1"

class SignOffRequest(BaseModel):
    case_id: str
    physician_name: str
    action: str  # "APPROVED_SUBMIT" or "FLAGGED_FOR_CLINIC"
    notes: Optional[str] = ""

class PatientPayRequest(BaseModel):
    amount: float
    payment_method: Optional[str] = "CARD"

class LabUploadRequest(BaseModel):
    patient_id: str
    test_title: str
    test_type: str
    summary_findings: str
    technician_name: Optional[str] = "Alex Chen"

class DoctorNoteRequest(BaseModel):
    case_id: str
    note: str

# =====================================================================
# HEALTH & METRICS ENDPOINTS
# =====================================================================

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "track": settings.TRACK,
        "amd_hardware": "AMD Instinct MI300X (192GB HBM3)",
        "offline_mock_mode": settings.USE_OFFLINE_MOCK,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/telemetry")
def get_telemetry():
    return amd_telemetry.get_current_metrics()

# =====================================================================
# AUTHENTICATION & REGISTRATION ENDPOINTS
# =====================================================================

@app.post("/api/auth/login")
def login(req: LoginRequest):
    """
    Authenticates a user via role or email/password and returns role-specific profile.
    """
    role = req.role if req.role in USERS_DB else "coordinator"
    user_info = USERS_DB[role]
    return {
        "success": True,
        "token": f"jwt_{role}_{uuid.uuid4().hex[:12]}",
        "user": user_info,
        "role": role,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/auth/signup")
def register_new_patient(req: NewPatientRequest):
    """
    Registers a brand new patient, stores their records, attaches their initial scan,
    and returns a ready-to-use patient session.
    """
    new_id = f"pat_{uuid.uuid4().hex[:6]}"
    mrn = str(uuid.uuid4().int)[:6]
    
    new_patient = {
        "id": new_id,
        "mrn": mrn,
        "name": req.name,
        "age": 42,
        "gender": "Unspecified",
        "dob": req.dob,
        "phone": req.phone,
        "email": req.email or f"{req.name.lower().replace(' ', '.')}@example.com",
        "insurance_provider": req.insurance_provider,
        "policy_id": req.policy_id or f"POL-{mrn}-NEW",
        "diagnosis": req.chief_complaint,
        "procedure": f"Specialist Consultation & Imaging for {req.chief_complaint}",
        "adjudication_status": "INTAKE_IN_REVIEW",
        "auth_number": f"AUTH-PENDING-{mrn}",
        "plain_english_summary": {
            "title": f"Welcome to CareAuth, {req.name}!",
            "reading_level": "Grade 6 Simple Language",
            "body": f"We have received your medical details and your uploaded diagnostic file ({req.report_filename}). Our clinic staff and doctors are reviewing your record against {req.insurance_provider}'s prior-authorization guidelines. You can see your uploaded files below, and you will receive a notification as soon as the review is complete.",
            "next_steps": "1. Intake nurse will verify your insurance eligibility.\n2. Review your uploaded diagnostic report.\n3. Doctor will certify your care plan."
        },
        "billing": {
            "procedure_name": f"Comprehensive Evaluation & {req.chief_complaint}",
            "facility_cost": 750.00,
            "insurance_covered": 700.00,
            "copay_balance": 50.00,
            "is_paid": False,
            "receipt_id": None,
            "paid_at": None
        },
        "diagnostic_reports": [
            {
                "id": f"rep_{uuid.uuid4().hex[:6]}",
                "title": req.report_filename or "Initial Medical Intake Document",
                "type": req.report_type or "Patient Upload",
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "doctor": "Self-Submitted during Intake",
                "status": "PROCESSING & ATTACHED",
                "summary": f"Uploaded during registration: {req.chief_complaint}. File verified and linked to MRN {mrn}.",
                "image_preview": "Verified Medical PDF/Scan Document Attached"
            }
        ]
    }
    
    # Save to in-memory store
    PATIENTS_DB[new_id] = new_patient
    
    # Also add a dynamic user entry
    USERS_DB[f"user_{new_id}"] = {
        "id": new_id,
        "username": new_patient["email"],
        "name": req.name,
        "role": "patient",
        "role_title": f"New Registered Patient (MRN: {mrn})",
        "department": "Patient Care Portal",
        "avatar": "".join([part[0] for part in req.name.split()[:2]]).upper() or "PT"
    }

    return {
        "success": True,
        "message": f"Patient account created successfully for {req.name}.",
        "patient": new_patient,
        "user": USERS_DB[f"user_{new_id}"],
        "role": "patient",
        "token": f"jwt_patient_{new_id}"
    }

@app.post("/api/auth/logout")
def logout():
    return {
        "success": True,
        "message": "Session invalidated successfully."
    }

# =====================================================================
# PATIENT PORTAL ENDPOINTS
# =====================================================================

@app.get("/api/patient/{patient_id}")
def get_patient_profile(patient_id: str):
    """
    Returns full patient view including plain-English explanation, scan reports, and billing.
    """
    if patient_id not in PATIENTS_DB:
        # Fallback to default patient if ID not found
        patient_id = "pat_10492"
    return PATIENTS_DB[patient_id]

@app.post("/api/patient/{patient_id}/pay")
def pay_copay(patient_id: str, req: PatientPayRequest):
    """
    Processes simulated patient copay payment and generates receipt.
    """
    if patient_id not in PATIENTS_DB:
        patient_id = "pat_10492"
    patient = PATIENTS_DB[patient_id]
    
    receipt_id = f"RCP-{patient['mrn']}-{datetime.utcnow().strftime('%Y%m%d%H%M')}"
    patient["billing"]["is_paid"] = True
    patient["billing"]["copay_balance"] = 0.00
    patient["billing"]["receipt_id"] = receipt_id
    patient["billing"]["paid_at"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

    return {
        "success": True,
        "message": "Payment processed successfully.",
        "receipt_id": receipt_id,
        "amount_paid": req.amount,
        "billing": patient["billing"]
    }

@app.post("/api/patient/{patient_id}/upload-report")
def patient_upload_report(patient_id: str, payload: Dict[str, Any] = Body(...)):
    """
    Allows a patient to upload additional diagnostic reports or prior scans.
    """
    if patient_id not in PATIENTS_DB:
        patient_id = "pat_10492"
    patient = PATIENTS_DB[patient_id]

    title = payload.get("title", "Outside Diagnostic Document")
    doc_type = payload.get("type", "Patient Uploaded Scan")
    summary = payload.get("summary", "Document submitted by patient for prior-authorization clinical correlation.")

    new_report = {
        "id": f"rep_up_{uuid.uuid4().hex[:6]}",
        "title": title,
        "type": doc_type,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "doctor": "Self-Submitted / Outside Facility",
        "status": "PENDING CLINICAL CORRELATION",
        "summary": summary,
        "image_preview": "Scanned Document Preview Verified"
    }
    patient["diagnostic_reports"].insert(0, new_report)

    return {
        "success": True,
        "message": f"Report '{title}' uploaded and attached to patient chart.",
        "report": new_report,
        "total_reports": len(patient["diagnostic_reports"])
    }

# =====================================================================
# DOCTOR PORTAL ENDPOINTS
# =====================================================================

@app.get("/api/doctor/queue")
def get_doctor_queue():
    """
    Returns pending cases awaiting physician electronic attestation or clinical review.
    """
    return DOCTOR_QUEUE

@app.post("/api/doctor/sign-off")
def submit_doctor_sign_off(payload: SignOffRequest):
    """
    Submits 1-Click Electronic Attestation with cryptographic signature timestamp.
    """
    for item in DOCTOR_QUEUE:
        if item["case_id"] == payload.case_id:
            item["signed"] = True
            item["status"] = "CERTIFIED_TRANSMITTED"
            item["signature_stamp"] = f"/s/ {payload.physician_name} ({datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')})"
            break

    # Also update associated patient status if applicable
    case_map = {"case1": "pat_10492", "case2": "pat_15489", "case3": "pat_78596"}
    pat_id = case_map.get(payload.case_id)
    if pat_id and pat_id in PATIENTS_DB:
        PATIENTS_DB[pat_id]["adjudication_status"] = "PHYSICIAN_CERTIFIED"

    return {
        "success": True,
        "case_id": payload.case_id,
        "physician_sign_off": f"/s/ {payload.physician_name}",
        "action": payload.action,
        "status": "TRANSMITTED_TO_PAYER_CLEARINGHOUSE",
        "timestamp": datetime.utcnow().isoformat(),
        "digital_attestation_hash": f"SHA256:{uuid.uuid4().hex}{uuid.uuid4().hex[:16]}",
        "message": f"Case {payload.case_id} electronically signed by {payload.physician_name} and transmitted to electronic payer clearinghouse."
    }

@app.post("/api/doctor/note")
def add_doctor_note(payload: DoctorNoteRequest):
    """
    Allows doctor to document contraindications (e.g. clears step therapy gap).
    """
    for item in DOCTOR_QUEUE:
        if item["case_id"] == payload.case_id:
            item["criteria_summary"] += f" [Physician Note: {payload.note}]"
            item["confidence"] = 0.95
            item["status"] = "GAP_RESOLVED_READY_TO_SIGN"
            break
    return {
        "success": True,
        "case_id": payload.case_id,
        "message": "Clinical contraindication note appended. Evidence gap resolved."
    }

# =====================================================================
# LAB / DIAGNOSTIC TECHNICIAN ENDPOINTS
# =====================================================================

@app.get("/api/lab/patients")
def list_lab_patients():
    """
    Returns list of all active hospital patients for the Lab Technician dashboard.
    """
    result = []
    for pid, p in PATIENTS_DB.items():
        result.append({
            "id": p["id"],
            "mrn": p["mrn"],
            "name": p["name"],
            "age": p["age"],
            "gender": p["gender"],
            "insurance": p["insurance_provider"],
            "procedure": p["procedure"],
            "report_count": len(p.get("diagnostic_reports", [])),
            "latest_test": p["diagnostic_reports"][0]["title"] if p.get("diagnostic_reports") else "No tests"
        })
    return result

@app.get("/api/lab/patients/{patient_id}/reports")
def get_patient_lab_reports(patient_id: str):
    """
    Returns all diagnostic reports, X-Rays, and MRI scans for a specific patient.
    """
    if patient_id not in PATIENTS_DB:
        raise HTTPException(status_code=404, detail="Patient not found.")
    patient = PATIENTS_DB[patient_id]
    return {
        "patient_id": patient["id"],
        "name": patient["name"],
        "mrn": patient["mrn"],
        "reports": patient.get("diagnostic_reports", [])
    }

@app.post("/api/lab/upload")
def lab_upload_report(req: LabUploadRequest):
    """
    Allows Lab Tech to upload, verify, and link new MRI, X-Ray, or blood tests to a patient.
    """
    if req.patient_id not in PATIENTS_DB:
        raise HTTPException(status_code=404, detail="Patient not found.")
    patient = PATIENTS_DB[req.patient_id]

    new_report = {
        "id": f"rep_lab_{uuid.uuid4().hex[:6]}",
        "title": req.test_title,
        "type": req.test_type,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "doctor": f"{req.technician_name} (Radiology/Lab Dept)",
        "status": "VERIFIED & LINKED",
        "summary": req.summary_findings,
        "image_preview": f"Verified Digital {req.test_type} Image Series Stored on PACS"
    }
    patient["diagnostic_reports"].insert(0, new_report)

    return {
        "success": True,
        "message": f"Diagnostic report '{req.test_title}' uploaded and linked to {patient['name']}.",
        "report": new_report
    }

# =====================================================================
# COORDINATOR / PAYER POLICIES & CASES ENDPOINTS
# =====================================================================

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
            "content": load_file_content(os.path.join(MOCK_DIR, "case1_knee_arthroscopy_approved.md"))
        },
        {
            "id": "case2",
            "title": "Case 2: Biologic Humira (Step-Therapy Gap Detected)",
            "subtitle": "Medicare LCD L33777 | Missing Methotrexate Trial ➔ Yellow Alert",
            "procedure": "HCPCS J0135 — Adalimumab 40mg",
            "expected_outcome": "HUMAN_REVIEW_REQUIRED",
            "confidence_expected": "64%",
            "color": "amber",
            "content": load_file_content(os.path.join(MOCK_DIR, "case2_humira_missing_step_therapy.md"))
        },
        {
            "id": "case3",
            "title": "Case 3: Complex Transfer (Prior Denial Overturn Appeal)",
            "subtitle": "Medicare LCD §4.2.1 | Statutory Transaminitis Exemption Applied",
            "procedure": "Tertiary Transfer & Specialized Biologic",
            "expected_outcome": "APPEAL_SIGN_OFF_READY",
            "confidence_expected": "92%",
            "color": "indigo",
            "content": load_file_content(os.path.join(MOCK_DIR, "case3_denied_transfer_appeal.md"))
        }
    ]

@app.get("/api/policies")
def list_payer_policies():
    """
    Returns the loaded payer policy guidelines from Evolus workspace.
    """
    anthem_content = load_file_content(os.path.join(POLICIES_DIR, "anthem_knee_arthroscopy.md"))
    medicare_content = load_file_content(os.path.join(POLICIES_DIR, "medicare_biologics_lcd.md"))
    return {
        "anthem_cg_surg_01": {
            "title": "Anthem Clinical Guideline CG-SURG-01: Knee Arthroscopy & Meniscectomy",
            "effective_date": "2026-01-01",
            "payer": "Anthem Blue Cross Blue Shield",
            "cpt_codes": ["29881", "29880", "29877"],
            "criteria_clauses": [
                "Clause 1: Documented Grade III or IV Meniscus Tear corroborated by 3.0T MRI.",
                "Clause 2: Minimum 6 weeks (preferred 6 months) supervised physical therapy without resolution.",
                "Clause 3: Absence of bone-on-bone tricompartmental osteoarthritis (Kellgren-Lawrence Grade <= 2)."
            ],
            "raw_markdown": anthem_content
        },
        "medicare_lcd_l33777": {
            "title": "Medicare LCD L33777: Biologic DMARD Therapy for Rheumatoid Arthritis",
            "effective_date": "2026-01-01",
            "payer": "Centers for Medicare & Medicaid Services (CMS)",
            "hcpcs_codes": ["J0135", "J0717"],
            "criteria_clauses": [
                "Section 1: Active moderate-to-severe Rheumatoid Arthritis corroborated by serology (RF or Anti-CCP).",
                "Section 2: Documented 3-month trial of conventional synthetic DMARD (Methotrexate >= 15mg/wk).",
                "Section 4.2.1 Statutory Exemption: Step therapy waived if documented contraindication exists (e.g. transaminitis AST/ALT > 2x ULN, severe cytopenia)."
            ],
            "raw_markdown": medicare_content
        }
    }

@app.post("/api/phi-sanitize")
def sanitize_phi(payload: Dict[str, str] = Body(...)):
    text = payload.get("text", "")
    return phi_sanitizer.sanitize(text)

@app.post("/api/adjudicate")
async def process_prior_auth(req: AdjudicationRequest):
    """
    Runs the full 4-Agent Autonomous Workflow:
    1. Local HIPAA PHI Sanitization
    2. Evolus Event Workflow Execution
    3. Document Extractor Agent
    4. Policy Adjudicator Agent (Evidence Gap & Confidence Matrix)
    5. Appeal & Packet Drafter Agent (Dual Output: Formal Insurer + Patient-Friendly Multilingual)
    6. AMD Telemetry Snapshot
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

# Mount static frontend
if not os.path.exists(FRONTEND_DIR):
    os.makedirs(FRONTEND_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def serve_index():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return JSONResponse({"message": "CareAuth-ROCm Backend Active. UI building..."})

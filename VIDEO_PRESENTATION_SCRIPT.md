# 🎬 CareAuth-ROCm: Official 5-Minute Video Presentation Guide

> **Total Video Length:** Exactly 5:00 Minutes (300 Seconds)  
> **Team:** Team Techtors  
> **Submission:** AMD Developer Hackathon: ACT III  
> **Tracks:** Track 2 — Health & Wellbeing (Vibe Generation) + Evolus Partner Track  

---

## ⏱️ Master 5-Minute Time Allocation

| Section | Content / Screen Action | Start | End | Duration |
| :--- | :--- | :---: | :---: | :---: |
| **Part 1** | **Introduction & Problem Statement** (Pitch Deck Slide 1 & 2) | 0:00 | 0:35 | **35 sec** |
| **Part 2** | **Prior-Auth Coordinator Cockpit & The 3 Clinical Cases** | 0:35 | 1:40 | **65 sec** |
| **Part 3** | **Doctor Certification Station (EHR, PACS Scans & 1-Click Sign-Off)** | 1:40 | 2:20 | **40 sec** |
| **Part 4** | **Lab Officials Station (Diagnostic Records & Test Uploading)** | 2:20 | 2:50 | **30 sec** |
| **Part 5** | **Patient Registration & MyCare Patient Portal (6th-Grade, Scans, Pay)** | 2:50 | 3:45 | **55 sec** |
| **Part 6** | **Evolus Platform Workspace & Multi-Agent Architecture** | 3:45 | 4:15 | **30 sec** |
| **Part 7** | **AMD Developer Programme & ROCm Cloud Credit Request** | 4:15 | 4:40 | **25 sec** |
| **Part 8** | **GitHub Repository (`deepak0kannan/CareAuth-ROCm`) & Closing** | 4:40 | 5:00 | **20 sec** |
| **TOTAL** | **Complete Hackathon Demonstration** | **0:00** | **5:00** | **300 sec** |

---

## 🎙️ Step-by-Step Script & Screen Actions

### ⏰ PART 1: Introduction & Problem Statement (0:00 – 0:35 | 35s)
- **On Screen:** Slide 1 (Title) and Slide 2 (The Problem) from `CareAuth_ROCm_Prototype_Presentation.pptx`.
- **What to Say:**
  > *"Hello judges! We are Team Techtors, presenting **CareAuth-ROCm** for Track 2: Health & Wellbeing and the Evolus Partner Track.  
  > In healthcare today, doctors spend over 14 hours every single week on manual insurance prior-authorizations. This paperwork causes massive burnout and delays patient treatments by weeks.  
  > CareAuth-ROCm solves this crisis by combining **Evolus Business Agents** with the high-throughput inference power of **AMD Instinct MI300X (ROCm)** to automate prior-authorization from clinical intake to patient billing in under 12 seconds."*

---

### ⏰ PART 2: Coordinator Cockpit & The 3 Golden Cases (0:35 – 1:40 | 65s)
- **On Screen:** Browser at `http://127.0.0.1:8000`. Click **Coordinator** on the login screen, click **Sign In**, and go to the Cockpit.
- **Actions & What to Say:**
  1. **Case 1 (Clean Auto-Approval — 0:35 to 0:55):**
     - Select **Case 1: Ramesh Patel** (Knee Arthroscopy CPT 29881).
     - Point out the **AMD Instinct MI300X Telemetry HUD** (86.4 tokens/sec, 192ms TTFT).
     - Click **"Run Multi-Agent Pipeline"**.
     - Show the **Evidence Gap Matrix**:
       > *"Our multi-agent pipeline extracts clinical notes, matches Anthem Blue Cross policy rules, verifies 6 months of physical therapy and MRI meniscal tear, achieving a 96% confidence auto-approval."*
  2. **Case 2 (Step-Therapy Uncertainty Gap — 0:55 to 1:15):**
     - Switch dropdown to **Case 2: Sophia Martinez** (Humira Biologic).
     - Show the **Yellow Uncertainty Alert (64% Confidence)**:
       > *"Here, our system makes uncertainty visible. Medicare requires a 3-month trial of Methotrexate before Humira. The EHR only showed Prednisone. The system flags this gap and escalates it to human review instead of blindly guessing."*
  3. **Case 3 (Statutory Exception Appeal — 1:15 to 1:40):**
     - Switch dropdown to **Case 3: Emily Davis** (Expedited Biologic Appeal).
     - Show the **92% Confidence** citing Section 4.2.1:
       > *"In Case 3, the patient had elevated liver transaminases (AST 184, ALT 210). Our agent detected this medical contraindication, automatically cited Medicare Statutory Exception §4.2.1, and drafted a formal appeal packet ready for physician sign-off."*

---

### ⏰ PART 3: Doctor Certification Station (1:40 – 2:20 | 40s)
- **On Screen:** Click **Logout** at top right. Select **Doctor** card, click **Sign In**.
- **Actions & What to Say:**
  - Show the queue of active cases. Click on **Ramesh Patel**.
  - Cycle through the 4 doctor workspace tabs:
    - 📋 **Clinical EHR Note:** Pre-op orthopedic surgical note.
    - 🗣️ **Patient Plain Explanation:** Show the 6th-grade summary and click **ES (Spanish)** or **HI (Hindi)**.
    - 🩻 **Diagnostic Scans & Reports:** Click **"Inspect PACS Scan Image"** on the Knee MRI. In the DICOM viewer, click **Invert** and **Zoom +** to show the Grade III tear crosshair!
    - ⚖️ **Policy Criteria:** Show the matched policy clauses.
  - Click **"Certify & Approve Prior-Auth (1-Click Sign-Off)"**.
  - Show the green **"Physician Certified & Electronically Signed"** badge and cryptographic timestamp.
    > *"With one click, the physician reviews the EHR, inspects high-resolution PACS images, and electronically certifies the claim with a digital cryptographic seal."*

---

### ⏰ PART 4: Lab Officials Station (2:20 – 2:50 | 30s)
- **On Screen:** Click **Logout**. Select **Lab Tech** card, click **Sign In**.
- **Actions & What to Say:**
  - Select **Sophia Martinez** from the left-hand patient list.
  - Show her diagnostic panel: Rheumatoid Serology ELISA, QuantiFERON-TB Gold Plus, and Hand Radiography.
  - Click **"Inspect Imaging (PACS Scan)"** on the Hand X-Ray to show the MCP joint erosions crosshair.
  - Click **"+ Upload Diagnostic Test"** to open the modal:
    > *"Lab technicians can review all patient diagnostic histories, inspect connected PACS series, and upload new pathology or imaging results that immediately link to the patient's prior-auth chart."*

---

### ⏰ PART 5: Patient Registration & MyCare Patient Portal (2:50 – 3:45 | 55s)
- **On Screen:** Click **Logout**.
- **Actions & What to Say:**
  1. **New Patient Registration (2:50 to 3:05):**
     - Click **"Register as New Patient"** tab on the login screen.
     - Show the simple intake form (Full Name, DOB, Phone, Insurance Provider, Chief Complaint).
     - Mention:
       > *"New patients can register directly without initial paperwork friction, entering their basic intake and insurance details."*
  2. **MyCare Patient Portal & 6th-Grade Explanations (3:05 to 3:45):**
     - Switch back to **Sign In**, select **Patient**, and click **Sign In**.
     - Highlight the **6th-Grade Plain-Language Summary**:
       > *"Patients never see confusing medical billing codes. They see a clear, 6th-grade reading level explanation of their approval status."*
     - Click **ES** (Spanish) and **HI** (Hindi) to show instant multilingual translation.
     - Under **"My Scan & Diagnostic Reports"**, click **"View Scan & Image"** on the Physical Therapy Summary to show the **Goniometric ROM Curve Chart** (plateauing at 95° vs. 135° normal).
     - Under **"Insurance Coverage & Co-Pay"**, click **"Pay Co-Pay Balance ($250.00)"** to show the instant paid receipt.
     - Point out the **"Switch Patient Chart"** buttons at the top (`[Ramesh Patel] [Sophia Martinez] [Emily Davis]`) demonstrating instant multi-patient profile switching.

---

### ⏰ PART 6: Evolus Platform Workspace & Multi-Agent Architecture (3:45 – 4:15 | 30s)
- **On Screen:** Switch browser tab to your **Evolus Workspace** (`app.evolus.ai`).
- **Actions & What to Say:**
  - Show your **Evolus Application**: App ID `f21aea1f-f41c-43fc-83e0-f4eea7a9ecc3`.
  - Show the **Knowledge Library**: Payer policies (Anthem CG-SURG-01, Medicare LCD L33777).
  - Show the **Document Extractor & Business Workflows**:
    > *"Behind the scenes, our solution is built on the Evolus platform. We utilize Evolus Document Extractors for clinical entity extraction, Knowledge Libraries for storing dynamic payer rules, and multi-agent workflows that coordinate policy checks and evidence gap detection."*

---

### ⏰ PART 7: AMD Developer Programme & ROCm Cloud Request (4:15 – 4:40 | 25s)
- **On Screen:** Switch browser tab to your **AMD Developer Programme** portal / email confirmation.
- **Actions & What to Say:**
  - Show your logged-in **AMD Developer Account Profile**.
  - Show the **submitted request / application for AMD ROCm Cloud Accelerator Credits** (targeting the AMD Instinct MI300X 192GB HBM3 instance).
  - Explain:
    > *"For inference, CareAuth-ROCm is architected for AMD Instinct MI300X accelerators using ROCm and vLLM. We have officially applied to the AMD Developer Program for cloud accelerator credits to scale our model co-residency, enabling local HIPAA-compliant PHI sanitization and sub-200ms time-to-first-token."*

---

### ⏰ PART 8: GitHub Repository & Closing (4:40 – 5:00 | 20s)
- **On Screen:** Switch browser tab to **`https://github.com/deepak0kannan/CareAuth-ROCm`**.
- **Actions & What to Say:**
  - Scroll through the GitHub repository showing:
    - Clean file structure: `backend/`, `frontend/`, `mock_data/`, `evolus/`.
    - Comprehensive `README.md` with system architecture diagrams.
    - Open-source `LICENSE` (MIT) and `requirements.txt`.
    - Presentation pitch deck: `CareAuth_ROCm_Prototype_Presentation.pptx`.
  - **Final Closing:**
    > *"All code, presentation materials, and reproduction steps are open-sourced on our GitHub at `deepak0kannan/CareAuth-ROCm`.  
    > Thank you AMD and Evolus judges for this incredible hackathon opportunity!"*

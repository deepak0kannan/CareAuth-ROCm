# CareAuth-ROCm: 3-Minute Video Presentation & Demo Script

> **Video Duration Target:** 2 minutes 50 seconds (under the 3-minute hard limit)  
> **Screen Setup:** Open `http://localhost:8000` in Google Chrome or Edge.  
> **Recording Tool:** Loom, OBS Studio, or Windows Game Bar (`Win + Alt + R`).  

---

## ⏱️ Visual & Voiceover Breakdown (Timestamped)

### [0:00 - 0:35] The Hook & The Healthcare Crisis
* **On Screen:** Full-screen view of the **CareAuth-ROCm Clinical Cockpit** (`http://localhost:8000`). Highlight the top KPI banner (*45 Mins Manual ➔ 11.4s CareAuth | 98.6% Workload Cut*).
* **Voiceover (Speak confidently):**
  > *"Every single week, doctors and clinical staff spend over 14 hours buried under paperwork—not treating patients, but fighting insurance prior-authorizations. In the US alone, this administrative nightmare costs over $31 billion annually and delays critical care for millions of patients.*
  >
  > *Hello judges, we are Team Techtors, and this is **CareAuth-ROCm**—an autonomous healthcare administrative business agent built on **Evolus** and powered by high-throughput **AMD Instinct MI300X** infrastructure."*

---

### [0:35 - 1:05] Architecture, Evolus & AMD Silicon
* **On Screen:** Point mouse to the **Top Header** showing the **Track 2 Badge**, **HIPAA PHI Sanitized Locally Badge**, and the **AMD MI300X Telemetry Pill** (*86.4 tok/s | 192ms TTFT*).
* **Voiceover:**
  > *"CareAuth-ROCm addresses two fundamental healthcare hurdles:*
  >
  > *First, **Privacy**: Patient records cannot be sent to closed proprietary clouds. CareAuth de-identifies all Protected Health Information locally on AMD silicon with zero external leakage.*
  >
  > *Second, **Workflow Automation**: Built on the Evolus Platform, it connects Evolus Document Extractors, Knowledge Libraries, and Multi-Agent Workflows to evaluate clinical records against 80-page payer manuals.*
  >
  > *Behind the scenes, AMD's 192 gigabyte HBM3 memory allows us to hold entire patient histories and payer guidelines simultaneously with sub-200 millisecond time-to-first-token."*

---

### [1:05 - 1:40] Demo Scenario 1: Clean Auto-Approval
* **On Screen:** Click **Case 1: Knee Arthroscopy** on the left panel. Click the big green button: **"Run Multi-Agent Adjudication on AMD"**. Watch the animated agent trace execute and the Evidence Gap Matrix light up Green (96%).
* **Voiceover:**
  > *"Let's look at a real-world case. A patient requires knee arthroscopy for a meniscus tear.*
  >
  > *In under 12 seconds, our Extraction Agent identifies CPT code 29881 and ICD-10 M23.22. Our Policy Agent queries Anthem guideline CG-SURG-01 in the Evolus Knowledge Library.*
  >
  > *All 4 clinical criteria—including 6 months of physical therapy and MRI proof—are verified. Confidence is 96%. It generates an instant CMS-1500 Prior Authorization packet, saving 45 minutes of manual clinic time."*

---

### [1:40 - 2:15] Demo Scenario 2: Visible Uncertainty & Human Escalation (Track 2 Rule)
* **On Screen:** Click **Case 2: Biologic Humira** on the left panel. Click **"Run Multi-Agent Adjudication on AMD"**. Show the Confidence drop to **64% (Yellow Alert)**, the **Evidence Gap Detected** box appear, and the **Escalate to Clinic Nurse** button.
* **Voiceover:**
  > *"Now, here is how we strictly satisfy the hackathon's requirement to **Make Uncertainty Visible and Enforce Human Review**.*
  >
  > *In Case 2, a patient is prescribed Humira for severe rheumatoid arthritis. While the diagnosis is clear, our Adjudication Agent detects an evidence gap: Medicare rule Section 2.3 mandates a 3-month trial of conventional Methotrexate before biologic approval.*
  >
  > *Instead of guessing, the agent flags uncertainty, drops confidence to 64%, highlights the exact remediation path, and routes the file into our Human-in-the-Loop review queue for clinic nurse verification."*

---

### [2:15 - 2:40] Demo Scenario 3: Complex Transfer & Multilingual Patient Tab
* **On Screen:** Click **Case 3: Complex Transfer**. Show the 92% Denial Overturn. Then click **"Patient Explanation"** tab, and toggle between **EN**, **ES (Spanish)**, and **HI (Hindi)**. Click **"1-Click Physician Sign & Transmit"**.
* **Voiceover:**
  > *"In Case 3, a previously denied claim is overturned by uncovering a statutory hepatic transaminitis exemption in a 45-page transfer chart.*
  >
  > *And to help patients navigate this scary process, CareAuth includes a **Patient-Friendly Multilingual Explanation** in plain 6th-grade English, Spanish, and Hindi, explaining their coverage status with zero confusing jargon.*
  >
  > *With one click, the attending physician electronically signs and transmits the packet to the payer clearinghouse."*

---

### [2:40 - 2:50] The Wrap-Up & Closing
* **On Screen:** Show the full dashboard with all metrics.
* **Voiceover:**
  > *"CareAuth-ROCm transforms days of bureaucratic gridlock into seconds of transparent, compliant clinical automation—built on Evolus, powered by AMD. Thank you!"*

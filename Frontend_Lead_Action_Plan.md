# Frontend Lead Action Plan: Enterprise Clinical Cockpit

> **Project:** CareAuth-ROCm (Powered by HyperForge-ROCm)  
> **Team:** Team Techtors  
> **Owner:** Frontend Lead (Person A)  
> **Core Deliverable:** Next.js 14 App Router + Tailwind CSS Clinical Cockpit Dashboard  
> **Target Tracks:** Track 3 (Health & Wellbeing) + Evolus Partner Track  

---

## 1. Role Mission & Objectives

As the **Frontend Lead**, you own the **Front-of-House experience** that judges and physicians interact with. 
Your goal is to build a sleek, hospital-grade dashboard that:
1. Showcases the **Evolus Multi-Agent reasoning traces** in real time.
2. Clearly visualizes **clinical uncertainty and missing policy gaps** (Uncertainty Matrix).
3. Provides a **1-click Human-in-the-Loop review & sign-off queue**.
4. Features the **AMD Telemetry & KernelForge HUD** displaying live hardware performance (tokens/sec, VRAM, and kernel speedup).
5. Includes a **1-Click Demo Switcher** for instant presentation of the 3 hackathon scenarios.

---

## 2. Tech Stack & Dependencies

* **Framework:** Next.js 14 (App Router, TypeScript)
* **Styling:** Tailwind CSS + CSS Modules
* **Icons:** `lucide-react`
* **Components & UI:** Radix UI primitives (`@radix-ui/react-dialog`, `@radix-ui/react-tabs`, `@radix-ui/react-progress`, `@radix-ui/react-tooltip`)
* **State & Data Fetching:** React Hooks (`useState`, `useEffect`, `useCallback`) / SWR or TanStack Query
* **Visual Effects:** Framer Motion (for streaming agent reasoning cards & telemetry pulses)

---

## 3. Directory Layout (`frontend/`)

```
frontend/
├── app/
│   ├── layout.tsx                # Healthcare dark theme, navigation header, status banners
│   ├── page.tsx                  # Main 3-Panel Clinical Cockpit Dashboard
│   ├── cases/                    # Historical case viewer & audit log
│   │   └── [id]/page.tsx
│   └── api/                      # Next.js proxy routes to FastAPI backend
│       ├── adjudicate/route.ts
│       ├── telemetry/route.ts
│       └── approve/route.ts
├── components/
│   ├── Header.tsx                # Evolus status, AMD MI300X link, Active Model pill
│   ├── QuickDemoBar.tsx          # 1-click switcher: [Case 1: Knee] [Case 2: Humira] [Case 3: Appeal]
│   ├── DocumentViewer.tsx        # Multi-page clinical note viewer with clause highlights
│   ├── AgentReasoningTrace.tsx   # Live step-by-step thinking timeline (Extractor ➔ Adjudicator ➔ Drafter)
│   ├── UncertaintyMatrix.tsx     # Evidence Gap Matrix (Green/Yellow/Red confidence breakdown)
│   ├── HumanReviewQueue.tsx      # Modal / Drawer for doctor 1-click approval or record request
│   └── AmdTelemetryHud.tsx       # Live GPU gauges: Tokens/s, TTFT, VRAM (192GB), KernelForge Speedup
├── lib/
│   ├── mock-cases.ts             # Embedded fallback data for the 3 demo cases
│   ├── types.ts                  # Shared TypeScript interfaces (matches backend schema)
│   └── utils.ts                  # Formatting, classnames helper
├── package.json
└── tailwind.config.js
```

---

## 4. UI Architecture: The 3-Panel Cockpit

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│  [CareAuth-ROCm]  |  Model: Qwen-2.5-70B  |  Evolus: Connected  |  AMD MI300X: 192GB HBM3   │
├─────────────────────────────────────────────────────────────────────────────────────────────┤
│  DEMO SHORTCUTS: [Case 1: Knee Meniscectomy] [Case 2: Humira Step-Gap] [Case 3: 45-Page Transfer]
├───────────────────────────────┬─────────────────────────────┬───────────────────────────────┤
│ PANEL A: Clinical EHR Note    │ PANEL B: Multi-Agent Trace  │ PANEL C: Action & AMD HUD     │
│ & Policy Matcher              │ & Evidence Gap Matrix       │                               │
│                               │                             │ [1-Click Physician Sign-Off]  │
│ • Patient: [Redacted]         │ 1. Extraction Agent (3B)    │ • Status: PENDING REVIEW      │
│ • CPT: 29881 / ICD-10: M23.22 │    ✓ ICD-10 & CPT parsed    │ • Action: [Approve] [Reject]  │
│ • Conservative Therapy:       │ 2. Policy Adjudicator (14B) │                               │
│    ✓ 12 wks Physical Therapy  │    ✓ Anthem CG-SURG-01      │ ───────────────────────────── │
│ • MRI: Articular tear         │ 3. Gap Detector:            │ [AMD ROCm Hardware Telemetry] │
│                               │    ■ Criterion 1: 98% (Grn) │ • VRAM: 142 GB / 192 GB       │
│ [Uploaded Document Preview]   │    ■ Criterion 2: 95% (Grn) │ • Inference: 114 tokens/s     │
│ (Interactive highlighted text)│    Overall Score: 96%       │ • TTFT: 142 ms                │
│                               │                             │ • KernelForge: +22% Speedup   │
└───────────────────────────────┴─────────────────────────────┴───────────────────────────────┘
```

---

## 5. Component Breakdown & Functional Specs

### Component 1: `QuickDemoBar.tsx` (Critical for the 3-Minute Video)
* **Purpose:** Allows judges or presenters to instantly load any of the 3 hackathon scenarios without waiting for file uploads.
* **Buttons:**
  1. `Scenario 1: Knee Meniscectomy` $\rightarrow$ Instantly loads Case 1, shows Green 96% auto-approval, sub-3s latency.
  2. `Scenario 2: Humira Biologic` $\rightarrow$ Instantly loads Case 2, displays Yellow 64% alert, highlights *"Missing Methotrexate Step-Therapy"*.
  3. `Scenario 3: 45-Page Transfer Appeal` $\rightarrow$ Instantly loads Case 3, shows 70B routing, cites Medicare Section 4.2.1, and pulses the KernelForge Speedup badge.

### Component 2: `AgentReasoningTrace.tsx`
* **Purpose:** Visualizes autonomous multi-agent collaboration for Evolus judges.
* **Features:**
  * Animated feed displaying agent handoffs:
    * `[0.4s]` **Extraction Agent (3B):** De-identified PHI; extracted CPT 29881, ICD-10 M23.22.
    * `[1.1s]` **Knowledge Library Query:** Queried Anthem CG-SURG-01 vector index.
    * `[1.8s]` **Adjudication Agent (14B):** Evaluated conservative therapy and MRI findings.
    * `[2.4s]` **Uncertainty Gate:** Confidence calculated at 96% $\rightarrow$ Safe for auto-approval.

### Component 3: `UncertaintyMatrix.tsx` (Evidence Gap Heatmap)
* **Purpose:** Directly satisfies Track 3's strict **Visible Uncertainty** requirement.
* **Features:**
  * Renders a breakdown of policy criteria with color-coded confidence:
    * **Green ($\ge 90\%$):** Fully satisfied with citation to page/paragraph.
    * **Yellow ($70-89\%$):** Ambiguous or partial documentation.
    * **Red ($<70\%$):** Requirement missing or violated.
  * Clicking any criterion highlights the exact excerpt in the `DocumentViewer`.

### Component 4: `HumanReviewQueue.tsx` (Physician Oversight)
* **Purpose:** Proves clinical safety and human-in-the-loop control.
* **Features:**
  * When confidence is $<90\%$ (Scenario 2 & 3), activates a prominent review drawer:
    * Displays the exact missing item (e.g. *"Mandatory 3-month trial of conventional synthetic DMARD"*).
    * Provides 3 action buttons: `[1-Click Doctor Approval]`, `[Request Additional Records]`, `[Generate Formal Appeal]`.

### Component 5: `AmdTelemetryHud.tsx` (For AMD Judges)
* **Purpose:** Proves that the app is deeply integrated with AMD silicon.
* **Features:**
  * **Active Model Pill:** Displays `Llama-3.1-8B` (Green), `Qwen-2.5-14B` (Blue), or `Qwen-2.5-70B` (Purple) based on HyperRouter's dispatch.
  * **VRAM Gauge:** Visualizes MI300X's 192GB memory pool (e.g. `142 / 192 GB HBM3 used`).
  * **Throughput Meter:** Live tokens/sec counter.
  * **KernelForge Speedup Badge:** An animated pill stating `KernelForge Active: +22.4% Triton Attention Speedup on MI300X`.

---

## 6. Shared TypeScript Interfaces (`lib/types.ts`)

```typescript
export type CaseScenarioId = 'case1_knee' | 'case2_humira' | 'case3_appeal';

export interface CriterionMatch {
  criterion_id: string;
  criterion_description: string;
  required_policy_clause: string;
  status: 'MET' | 'MISSING' | 'CONTRAINDICATED' | 'EXCEPTION_APPLIED';
  confidence_score: number; // 0.0 to 1.0
  evidence_excerpt?: string;
  source_page?: number;
}

export interface AdjudicationResponse {
  case_id: string;
  patient_id: string;
  diagnosis_icd10: string;
  requested_cpt: string;
  routed_model: 'Llama-3.1-8B' | 'Qwen-2.5-14B' | 'Qwen-2.5-70B';
  overall_confidence: number;
  recommendation: 'AUTO_APPROVE' | 'HUMAN_ESCALATION' | 'GENERATE_APPEAL';
  criteria_breakdown: CriterionMatch[];
  generated_packet_markdown?: string;
  agent_trace: Array<{
    timestamp: string;
    agent_name: string;
    message: string;
    duration_ms: number;
  }>;
}

export interface AmdTelemetryResponse {
  hardware_device: string;
  total_vram_gb: number;
  used_vram_gb: number;
  tokens_per_second: number;
  time_to_first_token_ms: number;
  active_model: string;
  kernelforge_status: {
    enabled: boolean;
    operator_profiled: string;
    speedup_percentage: number;
    correctness_verified: boolean;
  };
}
```

---

## 7. Day-by-Day Implementation Roadmap (Person A)

| Day | Primary Focus | Daily Deliverable |
| :--- | :--- | :--- |
| **Day 1** | Project Setup & Shell | Initialize Next.js 14 App Router, install Tailwind + Lucide icons. Build responsive 3-panel layout and top navigation header. |
| **Day 2** | Mock Data & Demo Switcher | Build `QuickDemoBar.tsx` and load mock data from `lib/mock-cases.ts`. Ensure all 3 scenarios can be previewed without backend. |
| **Day 3** | Reasoning Trace & Evidence Matrix | Implement `AgentReasoningTrace.tsx` with animated progress and `UncertaintyMatrix.tsx` with colored confidence badges. |
| **Day 4** | Human Sign-Off & Telemetry HUD | Build `HumanReviewQueue.tsx` with action buttons and `AmdTelemetryHud.tsx` displaying live GPU gauges and KernelForge pill. |
| **Day 5** | API Integration | Connect Next.js API routes to Person B's FastAPI endpoints (`/adjudicate`, `/telemetry`). Test live data flow. |
| **Day 6** | Polish & Demo Recording | Refine transitions, verify mobile/desktop responsiveness, assist with the 3-minute video presentation capture. |

---

## 8. Definition of Done (Frontend Lead Checklist)

- [ ] Next.js 14 app builds with zero TypeScript or lint errors.
- [ ] 3-panel layout renders cleanly on 1080p and 4K displays.
- [ ] Clicking any scenario on `QuickDemoBar` updates all 3 panels in $<500$ ms.
- [ ] Uncertainty Matrix clearly distinguishes Green ($\ge 90\%$), Yellow ($70-90\%$), and Red ($<70\%$).
- [ ] Doctor Sign-Off drawer permits 1-click approval or appeal generation.
- [ ] AMD Telemetry HUD shows dynamic VRAM, tokens/sec, and KernelForge speedup.

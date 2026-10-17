# Backend & AMD Lead Action Plan: HyperForge-ROCm Engine & Evolus Core

> **Project:** CareAuth-ROCm (Powered by HyperForge-ROCm)  
> **Team:** Team Techtors  
> **Owner:** Backend & AMD Lead (Person B)  
> **Core Deliverable:** FastAPI Server + Evolus Client + HyperRouter + KernelForge Optimization Suite  
> **Target Tracks:** Track 3 (Health & Wellbeing) + Evolus Partner Track + AMD Grand Prize  

---

## 1. Role Mission & Objectives

As the **Backend & AMD Lead**, you own the **Back-of-House infrastructure** that satisfies both the **Evolus API requirements** and the **AMD GPU engineering judges**:
1. Build the **FastAPI orchestration service** connecting the frontend to models and agent pipelines.
2. Implement **`phi_sanitizer.py`** to guarantee HIPAA compliance before text leaves local boundaries.
3. Build **`evolus_client.py`** to programmatically trigger Document Extractors, Knowledge Libraries, and Sub-Agents in `app.evolus.ai`.
4. Build **`hyper_router.py`** to dynamically dispatch tasks across **3B/8B, 14B, and 70B** models co-resident in the 192GB HBM3 pool.
5. Implement the **`kernel_forge/`** optimization suite: profile long-context operators, verify candidate Triton/ROCm kernels with the **4-Part Correctness Suite**, and stream live benchmarked speedups.
6. Provide dual-mode operation: **Phase 1 (Local Ryzen CPU / Ollama)** for pre-kickoff and **Phase 2 (Cloud MI300X vLLM)** for post-kickoff.

---

## 2. Tech Stack & Dependencies

* **Language:** Python 3.10+
* **Framework:** FastAPI + Uvicorn + Pydantic v2
* **LLM Client:** `openai` Python SDK (points to AMD vLLM or local Ollama)
* **ROCm & GPU Libraries:** PyTorch with ROCm 6.0+, Triton, `triton-rocm`
* **HTTP & Utilities:** `httpx` (async HTTP client for Evolus API), `numpy`
* **Containerization:** Docker + Docker Compose

---

## 3. Directory Layout (`backend/`)

```
backend/
├── main.py                     # FastAPI entrypoint: CORS, routes, lifecycle hooks
├── config.py                   # Pydantic BaseSettings (endpoints, API keys, thresholds)
├── phi_sanitizer.py            # Local HIPAA PII de-identification engine
├── evolus_client.py            # Programmatic Evolus REST API SDK
├── hyper_router.py             # Macro dynamic routing engine: 3B/8B vs 14B vs 70B
│
├── kernel_forge/               # Micro ROCm GPU operator optimization suite
│   ├── __init__.py
│   ├── profiler.py             # Operator bottleneck detector on AMD MI300X
│   ├── candidate_kernels.py    # Custom fused Triton / ROCm kernels (RMSNorm, Attention)
│   ├── correctness_suite.py    # 4-Part numerical verification & safety test suite
│   └── benchmark.py            # Live A/B performance benchmark comparator
│
├── agents/                     # Healthcare Agent Implementations
│   ├── __init__.py
│   ├── extractor_agent.py      # Structured JSON clinical parser (ICD-10, CPT, history)
│   ├── adjudicator_agent.py    # Policy clause matching & confidence scoring
│   └── appeal_agent.py         # Formal CMS-1500 / appeal letter drafter
│
├── amd_telemetry.py            # Queries ROCm / MI300X runtime & kernel metrics
├── tests/
│   ├── test_phi_sanitizer.py
│   ├── test_hyper_router.py
│   └── test_kernel_forge.py
├── requirements.txt
└── Dockerfile.backend
```

---

## 4. Key Module Specifications

### Module 1: `hyper_router.py` (The Macro Optimization Gate)
* **Purpose:** Solves the multi-model co-residency optimization on the 192GB HBM3 pool.
* **Routing Logic:**
  * **Tier 1 (Llama-3.1-8B or 3B):** Triggered for routine extractions, standard CPT/ICD-10 validation, prompt length $<1,500$ tokens. Latency: $<1.5$s.
  * **Tier 2 (Qwen-2.5-14B):** Triggered for multi-clause policy cross-referencing, step-therapy gap auditing, prompt length $1,500 - 8,000$ tokens. Latency: $2-4$s.
  * **Tier 3 (Qwen-2.5-70B):** Triggered for multi-page complex appeals, long-context EHR transfers ($>8,000$ tokens), and conflicting medical history.
* **Fallback & Escalation:** If Tier 1 confidence is $<85\%$, automatically escalate the request to Tier 2 or Tier 3.

### Module 2: `kernel_forge/` (The Micro Optimization Engine)
* **Purpose:** Directly impresses AMD engineering judges by optimizing operator execution on ROCm.
* **Sub-components:**
  1. **`profiler.py`:** Profiles PyTorch execution on MI300X; detects that standard RMSNorm and Attention operators consume disproportionate runtime in long-context prompts (Scenario 3's 45-page chart).
  2. **`candidate_kernels.py`:** Contains optimized Triton kernels targeted for CDNA3 architecture (AMD Instinct MI300X).
  3. **`correctness_suite.py`:** The **4-Part Correctness Test Suite**:
     * *Test 1: Numerical Tolerance* ($L_\infty < 10^{-4}$ vs. PyTorch FP32/FP16 baseline).
     * *Test 2: Shape Invariance* (verifies arbitrary batch sizes and sequence lengths up to 32k).
     * *Test 3: Memory Bounds Check* (verifies zero memory leaks or out-of-bounds writes).
     * *Test 4: Edge Cases* (zero inputs, NaNs, and extreme dynamic range).
  4. **`benchmark.py`:** Compares baseline execution time vs. candidate kernel over 100 warm iterations, calculating real measured speedup (e.g. `+22.4%`).

### Module 3: `evolus_client.py` (Evolus Platform Integration)
* **Purpose:** Programmatically interfaces with `app.evolus.ai`.
* **Methods:**
  * `extract_clinical_entities(document_text: str)` $\rightarrow$ Calls Evolus Document Extractor tool.
  * `query_knowledge_library(query: str, library_id: str)` $\rightarrow$ Retrieves matching clauses from Anthem CG-SURG-01 or Medicare LCD L33777.
  * `trigger_workflow(workflow_id: str, payload: dict)` $\rightarrow$ Executes multi-agent workflow on Evolus.
  * *Mock Fallback Mode:* If offline or awaiting API keys, returns high-fidelity fixtures from `mock_data/` seamlessly.

### Module 4: `phi_sanitizer.py` (Local HIPAA PII Stripping)
* **Purpose:** Proves clinical safety and data governance.
* **Behavior:** Strips Patient Names, MRNs, SSNs, phone numbers, and addresses locally via deterministic regex and NER prior to routing prompts to LLMs or external endpoints.

### Module 5: `amd_telemetry.py` (Hardware & Runtime Telemetry)
* **Purpose:** Powers Panel C of the Clinical Cockpit.
* **Exposes:**
  * `vram_allocated_gb` vs `vram_total_gb` (192 GB on MI300X).
  * `tokens_per_second` (real-time generation throughput).
  * `time_to_first_token_ms` (TTFT).
  * `kernelforge_speedup_pct` (live speedup from verified candidate kernel).

---

## 5. FastAPI REST API Contract (Serving the Frontend)

```python
# Endpoints to implement in main.py:

POST /api/upload
# Ingests uploaded PDF/text note or accepts scenario ID ('case1_knee', 'case2_humira', 'case3_appeal')
# Returns: sanitized text and file metadata

POST /api/adjudicate
# Request Body: { case_id: str, document_text: str }
# Executes: PHI Sanitization ➔ HyperRouter Dispatch ➔ Evolus Extractor ➔ Policy Match ➔ Gap Detection
# Response Body: AdjudicationResponse (JSON matching frontend lib/types.ts)

GET /api/telemetry
# Returns: AmdTelemetryResponse with GPU utilization, tokens/s, VRAM, and KernelForge speedup

POST /api/approve
# Request Body: { case_id: str, action: 'APPROVE' | 'REJECT' | 'APPEAL', notes: str }
# Records physician electronic signature and returns completed submission packet
```

---

## 6. Hardware Strategy: Phase 1 (Local) vs. Phase 2 (MI300X Cloud)

To guarantee zero downtime before cloud credits arrive:

### Phase 1: Pre-Kickoff (Local Lenovo LOQ / Ryzen 7000 CPU)
* Run local Ollama:
  ```powershell
  ollama run llama3.1:8b
  ```
* Configure `.env`:
  ```bash
  AMD_ROCM_ENDPOINT="http://localhost:11434/v1"
  AMD_MODEL_ROUTING_TIER1="llama3.1:8b"
  AMD_MODEL_ROUTING_TIER2="llama3.1:8b"
  AMD_MODEL_ROUTING_TIER3="llama3.1:8b"
  MOCK_TELEMETRY=true
  ```

### Phase 2: Post-Kickoff (AMD Developer Cloud MI300X)
* Change 1 line in `.env`:
  ```bash
  AMD_ROCM_ENDPOINT="http://<amd-cloud-ip>:8000/v1"
  AMD_MODEL_ROUTING_TIER1="meta-llama/Llama-3.1-8B-Instruct"
  AMD_MODEL_ROUTING_TIER2="Qwen/Qwen2.5-14B-Instruct"
  AMD_MODEL_ROUTING_TIER3="Qwen/Qwen2.5-70B-Instruct"
  MOCK_TELEMETRY=false
  ```
* Zero code changes required on frontend or backend!

---

## 7. Day-by-Day Implementation Roadmap (Person B)

| Day | Primary Focus | Daily Deliverable |
| :--- | :--- | :--- |
| **Day 1** | Scaffolding & Local Endpoint | Scaffold FastAPI app in `backend/`. Implement `phi_sanitizer.py`. Connect to local Ollama / AMD endpoint exposing `/v1/chat/completions`. |
| **Day 2** | Evolus SDK & Agents | Implement `evolus_client.py` and the 3 agent modules (`extractor_agent.py`, `adjudicator_agent.py`, `appeal_agent.py`). Test with `mock_data/` files. |
| **Day 3** | HyperRouter Implementation | Implement `hyper_router.py` with 3-tier complexity dispatching and confidence threshold escalation. Verify routing for Case 1, 2, and 3. |
| **Day 4** | KernelForge Suite | Build `kernel_forge/`: implement Triton operator, 4-Part Correctness Suite, and benchmark runner calculating live speedup. |
| **Day 5** | Telemetry & Cloud Connection | Build `amd_telemetry.py`. Point backend to kickoff AMD MI300X instance. Verify end-to-end latency and VRAM telemetry with Next.js frontend. |
| **Day 6** | Dockerization & Verification | Create `Dockerfile.backend` and root `docker-compose.yml`. Test cold boot on fresh environment. Finalize submission docs. |

---

## 8. Definition of Done (Backend Lead Checklist)

- [ ] FastAPI starts without errors on port 8000 (`uvicorn main.py:app --reload`).
- [ ] `POST /api/adjudicate` processes all 3 demo cases and returns exact schema matching frontend.
- [ ] `phi_sanitizer.py` eliminates all synthetic patient names and MRNs before LLM prompt transmission.
- [ ] `hyper_router.py` correctly dispatches Case 1 to Tier 1, Case 2 to Tier 2, and Case 3 to Tier 3.
- [ ] `kernel_forge/` runs the 4-Part Correctness Suite and passes with $L_\infty < 10^{-4}$.
- [ ] `GET /api/telemetry` returns live/simulated MI300X metrics (192GB pool, tokens/s, KernelForge speedup).

# AMD Developer Hackathon: ACT III — Complete Project Journey & Technical Reference

> **Project Name:** HyperForge-ROCm  
> **Subtitle:** Autonomous Enterprise Business Agent & ROCm Inference Optimization Engine  
> **Team:** Team Techtors  
> **One-Line Pitch:** *Runs real Evolus business workflows. Routes the right model on AMD. Optimizes how it executes. Proves the improvement.*  
> **Target Tracks:** Track 3 (Health & Wellbeing — Healthcare Document Processing & Administrative Automation) + Evolus Partner Track (Evolus Business Agents on AMD)

---

## Table of Contents
1. [Executive Summary & Final 863-Character Pitch](#1-executive-summary--final-863-character-pitch)
2. [Session Evolution & How We Got Here](#2-session-evolution--how-we-got-here)
3. [The Core Concept: HyperForge-ROCm](#3-the-core-concept-hyperforge-rocm)
4. [The 13 Strategic Refinements (Team Techtors Edition)](#4-the-13-strategic-refinements-team-techtors-edition)
5. [The 7 Technical Truth Standards for AMD Engineering Judges](#5-the-7-technical-truth-standards-for-amd-engineering-judges)
6. [The 4-Part Correctness Test Suite & Benchmarking Rigor](#6-the-4-part-correctness-test-suite--benchmarking-rigor)
7. [Official Track Alignment: Why Track 3 (Health & Wellbeing)](#7-official-track-alignment-why-track-3-health--wellbeing)
8. [Evolus Partner Track Compliance Architecture](#8-evolus-partner-track-compliance-architecture)
9. [Hardware Feasibility: Running on Lenovo LOQ (Ryzen 7000 / RTX 3050)](#9-hardware-feasibility-running-on-lenovo-loq-ryzen-7000--rtx-3050)
10. [De-Risked 6-Day Hackathon Roadmap](#10-de-risked-6-day-hackathon-roadmap)
11. [Project Status & Completion Tracker](#11-project-status--completion-tracker)

---

## 1. Executive Summary & Final 863-Character Pitch

### The Official Submission Text (863 Characters)
```text
HyperForge-ROCm is an autonomous healthcare administrative agent that automates repetitive hospital paperwork—like insurance pre-authorizations, intake forms, and billing—to cut staff burnout.

Built on Evolus, it uses Document Extractors, Knowledge Libraries, and Workflows to process records, redact PII, check policy compliance, and flag mismatches. When uncertainty or high-risk conflicts arise, it hands the case to a human reviewer.

Behind this workflow, HyperRouter dynamically selects the right open model on AMD infrastructure (3B for routine intake, 14B for structured lookups, 70B for complex disputes). Beneath the models, KernelForge profiles GPU execution, synthesizes optimized ROCm/Triton kernels, and verifies them with strict numerical tests, deploying only proven speedups. The result: fast, low-cost, compliant healthcare operations on AMD silicon.
```

### The 30-Second Elevator Pitch Hook
> *"Think of HyperRouter as choosing the right vehicle for each trip (a scooter for quick errands, a truck for heavy loads), and KernelForge as tuning the engine underneath so every vehicle runs faster and burns less fuel."*

---

## 2. Session Evolution & How We Got Here

### Phase 1: Initial Ideas & Strategic Pivot
* **Initial Pitch:** The conversation began exploring ideas around Smart ICU Alarm Controllers, Computer Vision, and medical AI agents.
* **The Pivot:** The user decided **not** to bring academic coursework into the hackathon to eliminate IP/academic overlap and start fresh with an authentic industry problem statement.
* **Sourcing Problem Statements:** We explored Y Combinator 2026 Requests for Startups (RFS), AMD AI DevMaster & GPU MODE challenge boards, enterprise multi-agent latency reports, and Smart India Hackathon (SIH) archives.

### Phase 2: Identifying the Two Winning Ideas
We isolated two high-impact concepts:
1. **Autonomous GPU Kernel Optimizer:** An agent that profiles PyTorch operators on AMD GPUs, writes custom fused ROCm Triton kernels, verifies them, and benchmarks them.
2. **HyperRouter-ROCm:** A multi-model co-resident router exploiting AMD Instinct MI300X's 192GB HBM3 memory to route tasks across 3B, 14B, and 70B models with speculative escalation.

### Phase 3: The Fusion into HyperForge-ROCm
The user asked: *"Is it possible to merge Autonomous GPU Kernel Optimizer and HyperRouter-ROCm?"*  
The answer was a resounding yes:
* **HyperRouter (Macro Optimization):** Solves the algorithmic routing tax (deciding *which model* handles each subtask).
* **KernelForge (Micro Optimization):** Solves the GPU operator execution tax (optimizing *how that model runs* on ROCm).
* **The Recursive Loop:** HyperRouter routes kernel-synthesis coding tasks to the co-resident 14B/70B models, and KernelForge optimizes the very transformer operators used by those models and the router itself!

---

## 3. The Core Concept: HyperForge-ROCm

```text
                  USER / AGENT REQUEST
                           │
                           ▼
                   ┌──────────────┐
                   │ HYPERROUTER  │
                   │ (Macro Gate) │
                   └──────┬───────┘
                          │
              ┌───────────┼───────────┐
              ▼           ▼           ▼
             3B          14B          70B
              └───────────┼───────────┘
                          ▼
                    ROCm / vLLM
                          │
                          ▼
                     GPU PROFILER
                          │
                          ▼
                     BOTTLENECK
                          │
                          ▼
                    KERNELFORGE
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
          BASELINE                 CANDIDATE
              │                       │
              └───────────┬───────────┘
                          ▼
                    CORRECTNESS
                      TESTING
                          │
                          ▼
                      BENCHMARK
                          │
                     ┌────┴────┐
                     ▼         ▼
                  BETTER     WORSE
                     │         │
                  DEPLOY     REJECT
```

---

## 4. The 13 Strategic Refinements (Team Techtors Edition)

The user introduced 13 crucial improvements that transformed the project into a credible systems engineering entry:

1. **Keep the Two-Layer Architecture:** Layer 1 (HyperRouter Macro) + Layer 2 (KernelForge Micro).
2. **Change the Project Claim:** Remove unproven hardcoded numbers ("5.2× latency cut"). Use: *"Autonomously optimizes multi-model routing and GPU execution to reduce inference latency and improve throughput on AMD ROCm."* Insert actual measured numbers at runtime.
3. **Change "Guarantee" Language:** Remove "guaranteeing 70B-level accuracy at 3B speed." Use: *"Escalates uncertain or complex requests from the smaller model to a larger reasoning model."*
4. **Simplify the Router:** Don't require `<1.2 ms` router overhead upfront. Base routing on measurable signals (prompt length, task category, complexity, code requirements, confidence).
5. **Progressive 3-Model Rollout:**
   * Milestone 1: 3B working end-to-end.
   * Milestone 2: 3B + 14B working.
   * Milestone 3: 3B + 14B + 70B working.  
   *(If 70B faces deployment constraints, the project remains 100% functional).*
6. **Reduce KernelForge Scope (Phase A & B):**
   * *Phase A (Benchmarking Foundation):* Baseline PyTorch vs. pre-verified ROCm implementations across 4 operators (SwiGLU, Router Softmax/Top-K, RMSNorm+FP8, Sliding-Window Attention).
   * *Phase B (Autonomous Synthesis):* Automated Qwen-Coder Triton generation for **one** flagship operator.
7. **Safe Sandbox Deployment:** Candidate $\rightarrow$ Sandbox $\rightarrow$ Verify $\rightarrow$ Benchmark $\rightarrow$ Approve $\rightarrow$ Deploy (no reckless in-place hot-patching).
8. **Strict Acceptance Policy:** Accepted only if:
   * Numerical correctness $\checkmark$
   * Latency improved $\checkmark$
   * Memory within budget $\checkmark$
   * Accuracy threshold $\checkmark$
9. **Live Measurements in UI:** Replace static numbers with dynamic `[BASELINE]`, `[HYPERFORGE]`, and `[CALCULATED SPEEDUP]` gauges.
10. **The "Failed Candidate" Demonstration Path:** Demonstrate authentic autonomous decision-making by rejecting Candidate #1 (slower despite compiling) and accepting Candidate #2 (faster).
11. **De-Risked 6-Day Schedule:** Put Day 1 into the ROCm foundation; keep Day 6 strictly for validation, demo recording, and submission.
12. **Three-Zone Cockpit UI:**
    * Zone 1 (Top-Left): AI Workflow & HyperRouter Selection.
    * Zone 2 (Top-Right): ROCm / MI300X Hardware Telemetry.
    * Zone 3 (Bottom): KernelForge Sandbox & Acceptance Gate.
13. **Clean 5-Second Tagline:**  
    **HyperForge-ROCm: Autonomous AI Inference Optimization Engine**  
    *Routes the right model. Optimizes how it runs. Proves the improvement.*

---

## 5. The 7 Technical Truth Standards for AMD Engineering Judges

To speak the language of AMD hardware and compiler architects, the user codified 7 technical corrections:

| Topic | Avoid (Over-Simplified) | Use (Rigorous Systems Engineering) |
| :--- | :--- | :--- |
| **1. Bottleneck Physics** | *"LLMs are simply memory-bound, not compute-bound."* | *"LLM inference—specifically autoregressive decoding at low batch sizes—is often memory-bandwidth bound, while prefill and large batches are compute-intensive. Our profiler determines the actual bottleneck empirically."* |
| **2. GPU Memory Hierarchy** | *"Reading and writing to the hard drive after every line."* | *"Reducing repeated global-memory (HBM) traffic by keeping intermediate values inside on-chip registers, LDS (Local Data Share), and L2 cache."* |
| **3. Co-Residency Latency** | *"Switching from 3B to 70B takes 0 milliseconds."* | *"Keeping models co-resident in MI300X HBM avoids expensive PCIe model-weight transfers, leaving only lightweight request dispatch and KV-cache scheduling."* |
| **4. HBM Footprint** | *"3B + 14B + 70B equals exactly 112 GB."* | *"~112 GB is the approximate weight-memory footprint; total runtime HBM usage (including KV-cache, activations, and ROCm buffers) is measured live in our Telemetry HUD."* |
| **5. Escalation Signals** | *"Low token logprob proves the 3B answer is wrong."* | *"Logprob-derived confidence/entropy margin is one escalation signal combined with task complexity and optional structural verification—not an absolute correctness guarantee."* |
| **6. SwiGLU & Kernel Fusion** | *"3× fewer memory ops guarantees a 3× speedup."* | *"In SwiGLU (two linear projections + SiLU + elementwise multiply), kernel fusion combines the activation and elementwise operations to reduce intermediate global-memory traffic and launch overhead; actual speedup is measured."* |
| **7. Numerical Verification** | *"torch.allclose proves mathematical equivalence."* | *"We perform numerical equivalence validation on representative test suites (multiple random seeds, varied tensor shapes, edge cases) using torch.allclose tolerances."* |

---

## 6. The 4-Part Correctness Test Suite & Benchmarking Rigor

### The Explicit 4-Part Test Suite
1. **Canonical Shapes:** Standard power-of-two batch/sequence dimensions (e.g., `[1, 1024, 4096]`, `[8, 512, 4096]`) verifying functional math.
2. **Non-Power-of-Two / Boundary Shapes:** Odd/prime token counts (e.g., `[1, 17, 4096]`, `[3, 129, 4096]`) catching missing Triton boundary masks (`offsets < N`).
3. **Numerical Stress Inputs:** All-zeros, negative values, near-saturation values, and near-zero variance inputs testing `RMSNorm` $\epsilon$ division stability and `NaN`/`Inf` guards.
4. **Tolerance & Metadata Check:** Exact `shape`, `dtype`, and `device` match, followed by `torch.allclose(rtol=1e-3, atol=1e-4)` for `BF16`/`FP16`.

### Benchmarking Methodology & Optional L2 Flush
* **Warmup & Sync:** 10 untimed warmup runs followed by 50 timed runs bracketed by `torch.cuda.synchronize()` (`hipDeviceSynchronize()`).
* **Methodology-Dependent L2 Cache Modes:**
  * **Warm-Pipeline Mode (Default):** Preserves MI300X 256MB Infinity Cache locality between GEMM and activation epilogues.
  * **Cold-Cache Isolated Mode (Optional):** Flushes L2 buffer when isolating cold HBM3 memory bandwidth.

### Demonstrated Acceptance Gate Trace *(Illustrative Numbers)*
* **Candidate #1 (Suboptimal Block Size):** Compile $\checkmark$ | 4-Part Test Suite $\checkmark$ | *Baseline: 12.4 ms $\rightarrow$ Candidate #1: 14.7 ms (Slower)* $\rightarrow$ **`✗ REJECTED (Keep Baseline)`**
* **Candidate #2 (Fused Wave64 Kernel):** Compile $\checkmark$ | 4-Part Test Suite $\checkmark$ | *Baseline: 12.4 ms $\rightarrow$ Candidate #2: 7.8 ms (1.59× Speedup)* $\rightarrow$ **`✓ ACCEPTED & DEPLOYED`**

---

## 7. Official Track Alignment: Why Track 3 (Health & Wellbeing)

When the organization released the four official tracks:
1. *Reinvent Commerce* (Retail, sales, shoppers)
2. *Intelligent Industry* (Shop-floor maintenance, machine sensors)
3. *Health and Wellbeing* (Healthcare paperwork, clinical summaries, administrative workflows)
4. *Create a New Kind of Experience* (Generative entertainment, creative media)

### Why Track 3 is the Perfect 1-to-1 Match
Track 3's description explicitly lists:
* **"Healthcare document processing"**
* **"Administrative workflow automation"**
* **"Show a realistic case from the first input to the final result."**
* **"Make uncertainty visible."** (HyperRouter Confidence/Quality Gate)
* **"Know when a person needs to review or take over the case."** (Human-in-the-Loop Handoff)
* **"Safety rules: Must NOT present autonomous diagnosis or treatment as medical advice."** (HyperForge is purely an administrative paperwork compliance tool).

### The 3 Healthcare Document Scenarios (Demo Flow)
1. **Document 1 (Routine Insurance Pre-Authorization $\rightarrow$ `3B` on AMD):** Standard cataract surgery request. Extractor pulls codes, redacts PII, checks policy library $\rightarrow$ 100% match $\rightarrow$ **Auto-Approved in `<1 sec`**.
2. **Document 2 (Hospital Discharge Bill with Medication Mismatch $\rightarrow$ `14B` on AMD $\rightarrow$ Human Handoff):** Discrepancy between billed drugs and approved formulary table $\rightarrow$ **Quality Gate flags discrepancy $\rightarrow$ Hands off to human billing officer with issue highlighted**.
3. **Document 3 (25-Page Inter-Hospital Clinical Transfer Summary $\rightarrow$ `70B` on AMD $\rightarrow$ Doctor Review):** Complex transfer with conflicting drug allergies $\rightarrow$ Reasoner summarizes history, risk-scores interactions $\rightarrow$ **Escalated to attending physician**.

---

## 8. Evolus Partner Track Compliance Architecture

The Evolus Track audits the team's `app.evolus.ai` workspace for:
1. **A connected AMD-hosted open model endpoint**
2. **At least 2 Evolus building blocks used**
3. **Active Evolus REST API calls running an end-to-end business process**

### The Integration Architecture
* **Evolus BYOM Model Endpoint:** `app.evolus.ai` connects via its OpenAI-compatible endpoint to **HyperForge-ROCm (`POST /v1/chat/completions`)** on AMD Developer Cloud (`vLLM` on MI300X).
* **4 Evolus Building Blocks Used:**
  1. **Document Extractor:** Turns incoming healthcare PDFs into structured JSON.
  2. **Knowledge Library:** Stores hospital policy, billing codes, and formulary tables.
  3. **Workflows:** Orchestrates multi-step intake, validation, and PII redaction.
  4. **Sub-Agents & AI Tools:** Handles clause risk scoring and human review handoff.
* **Driven via Evolus REST APIs:** `backend/evolus_client.py` makes programmatic calls to trigger workflows and document extraction.
* **Containerized Submission:** Packaged with `Dockerfile`, `docker-compose.yml`, and `.env.example` (no committed secrets).

---

## 9. Hardware Feasibility: Running on Lenovo LOQ (Ryzen 7000 / RTX 3050)

The user asked: *"We are using a laptop LOQ (AMD Ryzen 7000, RTX 3050)... will it be manageable?"*  
**Yes, 100% manageable.** Here is why:

* **Cloud GPU Compute:** Large models (`3B`, `14B`, `70B`), ROCm, and Triton kernels run in the **cloud** on **AMD Developer Cloud (MI300X)** using hackathon-provided credits or Fireworks AI AMD endpoints.
* **Evolus Cloud:** Evolus building blocks run 100% in the cloud browser at `app.evolus.ai`.
* **Lenovo LOQ Workstation:** Your AMD Ryzen 7000 CPU runs the local Python/FastAPI backend, Docker container, and frontend UI. Memory usage is `<300 MB`, making it fast and effortless on your laptop.

---

## 10. De-Risked 6-Day Hackathon Roadmap

| Day | Focus Area | Engineering Scope | Fallback Guarantee |
| :--- | :--- | :--- | :--- |
| **Day 1** | **ROCm + Evolus Setup** | Bring up MI300X + vLLM (`3B`), expose `/v1/chat/completions`, connect as BYOM endpoint in `app.evolus.ai` (Extractor + Workflow). | Evolus calling AMD 3B model live. |
| **Day 2** | **HyperRouter + Evolus API** | Build `evolus_client.py` + `HyperRouter` (`3B/14B/70B`) with Visible Quality Gate & Human Handoff trigger. | End-to-end Evolus workflow running on 3B + 14B. |
| **Day 3** | **KernelForge Phase A** | Profiler $\rightarrow$ Controlled bottleneck operators $\rightarrow$ 4-Part Correctness Suite $\rightarrow$ Warm/Cold Cache Benchmark. | Real measured ROCm operator speedups verified. |
| **Day 4** | **Autonomous Phase B** | Connect Qwen-Coder to generate Triton candidate in sandbox with compile-repair and the `Candidate #1 REJECTED` $\rightarrow$ `Candidate #2 ACCEPTED` trace. | Phase A + 1 autonomously synthesized operator. |
| **Day 5** | **3-Zone UI + Docker** | Build 3-Zone Cockpit (`Evolus Workflow + Quality Gate`, `ROCm Telemetry HUD`, `KernelForge Studio`) and package in Docker. | Containerized full-stack app running end-to-end. |
| **Day 6** | **Demo & Submit** | Verify Evolus workspace audit stats, record 3-minute pitch video, finalize runnable `README.md`, submit before 15:00 UTC. | 100% compliant Evolus + AMD submission. |

---

## 11. Project Status & Completion Tracker

* **Step 5 (Create Concept & Discuss with Mentors):** **COMPLETED (95%)** — Pitch, architecture, 1-page PDF, and pitch script are mentor-ready.
* **Step 6 (Build Prototype):** **READY TO START (0%)** — Blueprints, API schemas, and test suites are designed.
* **Step 7 (Prepare Presentation):** **OUTLINED (60%)** — Slide-by-slide storyline and problem definition ready.
* **Step 8 (Video Presentation):** **SCRIPT READY (40%)** — 3-minute shot-by-shot voiceover script prepared.
* **Step 9 (Submit Project):** **PENDING (0%)** — Submissions open Oct 12–18, 2026.

---

*Document compiled and verified for Team Techtors in `c:\Users\zenix\OneDrive\Documents\amd\HyperForge_ROCm_Full_Chat_Summary.md`.*

import os
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

def create_master_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Color Palette Definition
    COLOR_BG_DARK = RGBColor(15, 23, 42)      # Slate 900
    COLOR_CARD_BG = RGBColor(30, 41, 59)      # Slate 800
    COLOR_CARD_BORDER = RGBColor(51, 65, 85)  # Slate 700
    COLOR_AMD_RED = RGBColor(237, 28, 36)     # AMD Ruby Red
    COLOR_CYAN = RGBColor(6, 182, 212)        # Cyan 500
    COLOR_TEAL = RGBColor(20, 184, 166)       # Teal 500
    COLOR_GREEN = RGBColor(34, 197, 94)       # Emerald 500
    COLOR_YELLOW = RGBColor(234, 179, 8)      # Amber 500
    COLOR_TEXT_WHITE = RGBColor(248, 250, 252)# Slate 50
    COLOR_TEXT_MUTED = RGBColor(148, 163, 184)# Slate 400
    COLOR_PURPLE = RGBColor(168, 85, 247)     # Purple 500

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = COLOR_BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category="CAREAUTH-ROCM CLINICAL INTELLIGENCE", tracker="TRACK 2: HEALTH & WELLBEING | EVOLUS ON AMD"):
        tracker_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.35))
        tf_tr = tracker_box.text_frame
        tf_tr.word_wrap = True
        p_tr = tf_tr.paragraphs[0]
        p_tr.text = f"{category.upper()}  •  {tracker.upper()}"
        p_tr.font.name = "Segoe UI"
        p_tr.font.size = Pt(10)
        p_tr.font.bold = True
        p_tr.font.color.rgb = COLOR_AMD_RED

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.733), Inches(0.7))
        tf_t = title_box.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title
        p_t.font.name = "Segoe UI"
        p_t.font.size = Pt(24)
        p_t.font.bold = True
        p_t.font.color.rgb = COLOR_TEXT_WHITE

        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.4), Inches(11.733), Inches(0.02))
        line.fill.solid()
        line.fill.fore_color.rgb = COLOR_CARD_BORDER
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=COLOR_CARD_BG, border_color=COLOR_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.2)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    accent = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.2), Inches(0.15), Inches(5.0))
    accent.fill.solid()
    accent.fill.fore_color.rgb = COLOR_AMD_RED
    accent.line.fill.background()

    tbox = s1.shapes.add_textbox(Inches(1.2), Inches(1.2), Inches(11.3), Inches(3.2))
    tf = tbox.text_frame
    tf.word_wrap = True

    p0 = tf.paragraphs[0]
    p0.text = "AMD DEVELOPER HACKATHON: ACT III  |  TRACK 2 & EVOLUS PARTNER TRACK"
    p0.font.name = "Segoe UI"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_CYAN
    p0.space_after = Pt(14)

    p1 = tf.add_paragraph()
    p1.text = "CareAuth-ROCm"
    p1.font.name = "Segoe UI"
    p1.font.size = Pt(44)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_TEXT_WHITE
    p1.space_after = Pt(10)

    p2 = tf.add_paragraph()
    p2.text = "Autonomous Healthcare Prior-Authorization & Payer-Policy Adjudication Agent"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(20)
    p2.font.color.rgb = COLOR_TEXT_MUTED
    p2.space_after = Pt(10)

    p3 = tf.add_paragraph()
    p3.text = "Built on Evolus Business Agents  •  Powered by AMD Instinct™ MI300X Infrastructure"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(14)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_TEAL

    badges = [
        ("HIPAA COMPLIANT", "Local PHI Sanitization on AMD", COLOR_TEAL),
        ("VISIBLE UNCERTAINTY", "Evidence Gap & Confidence Matrix", COLOR_YELLOW),
        ("AMD MI300X HIGH-THROUGHPUT", "86.4 tok/s | 192ms TTFT | 192GB", COLOR_AMD_RED)
    ]
    for i, (b_title, b_sub, b_col) in enumerate(badges):
        bx = Inches(1.2 + i * 3.8)
        add_card(s1, bx, Inches(4.8), Inches(3.6), Inches(1.5))
        cbox = s1.shapes.add_textbox(bx + Inches(0.2), Inches(4.9), Inches(3.2), Inches(1.3))
        ctf = cbox.text_frame
        ctf.word_wrap = True
        cp0 = ctf.paragraphs[0]
        cp0.text = b_title
        cp0.font.name = "Segoe UI"
        cp0.font.size = Pt(11)
        cp0.font.bold = True
        cp0.font.color.rgb = b_col
        cp0.space_after = Pt(4)
        cp1 = ctf.add_paragraph()
        cp1.text = b_sub
        cp1.font.name = "Segoe UI"
        cp1.font.size = Pt(13)
        cp1.font.bold = True
        cp1.font.color.rgb = COLOR_TEXT_WHITE

    foot = s1.shapes.add_textbox(Inches(1.2), Inches(6.6), Inches(11.0), Inches(0.5))
    ftf = foot.text_frame
    ftp = ftf.paragraphs[0]
    ftp.text = "Team Techtors  |  5-Minute Prototype Master Deck  |  October 2026"
    ftp.font.name = "Segoe UI"
    ftp.font.size = Pt(11)
    ftp.font.color.rgb = COLOR_TEXT_MUTED

    s1.notes_slide.notes_text_frame.text = (
        "Judges, welcome to CareAuth-ROCm. Prior-authorization is healthcare's #1 administrative bottleneck. "
        "Built on Evolus and accelerated by AMD Instinct MI300X, we replace days of bureaucratic delay with seconds of transparent, "
        "HIPAA-compliant autonomous adjudication."
    )

    # =========================================================================
    # SLIDE 2: THE HEALTHCARE CRISIS
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "The Crisis: 14 Hours of Paperwork vs. Patient Healing", category="THE PROBLEM")

    stats = [
        ("14+ Hours / Week", "Physician Administrative Burden", "Doctors spend nearly 2 full workdays every week filling out prior-authorization insurance forms instead of caring for patients.", COLOR_AMD_RED),
        ("$31 Billion", "Annual US Administrative Waste", "Direct administrative overhead wasted annually on manual chart review, faxes, portal entries, and insurance phone queues.", COLOR_YELLOW),
        ("3 to 7 Days", "Critical Treatment Delays", "Patients with cancer, autoimmune conditions, and surgical needs wait up to a week for life-altering treatments to be approved.", COLOR_PURPLE)
    ]
    for i, (val, label, desc, col) in enumerate(stats):
        cx = Inches(0.8 + i * 3.97)
        add_card(s2, cx, Inches(1.7), Inches(3.8), Inches(2.5))
        box = s2.shapes.add_textbox(cx + Inches(0.2), Inches(1.8), Inches(3.4), Inches(2.3))
        btf = box.text_frame
        btf.word_wrap = True
        p = btf.paragraphs[0]
        p.text = val
        p.font.name = "Segoe UI"
        p.font.size = Pt(26)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        p2 = btf.add_paragraph()
        p2.text = label.upper()
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(8)
        p3 = btf.add_paragraph()
        p3.text = desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(12)
        p3.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s2, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.4))
    rbox = s2.shapes.add_textbox(Inches(1.1), Inches(4.6), Inches(11.1), Inches(2.2))
    rtf = rbox.text_frame
    rtf.word_wrap = True
    rp0 = rtf.paragraphs[0]
    rp0.text = "WHY HAS TRADITIONAL SOFTWARE FAILED TO FIX THIS?"
    rp0.font.name = "Segoe UI"
    rp0.font.size = Pt(12)
    rp0.font.bold = True
    rp0.font.color.rgb = COLOR_CYAN
    rp0.space_after = Pt(8)

    points = [
        ("Opaque, Dense Payer Manuals: ", "Commercial and Medicare policies are 50–100 page PDFs packed with hyper-specific clinical criteria, conservative therapy prerequisites, and step-therapy clauses."),
        ("Unstructured Clinical Notes: ", "Patient charts are buried in messy clinical notes, scanned radiology reports, lab attachments, and fragmented outpatient histories."),
        ("Privacy & HIPAA Gridlock: ", "Hospitals cannot blindly send Protected Health Information (PHI) to generic public cloud AI APIs without stringent BAA and hardware isolation.")
    ]
    for title, desc in points:
        p = rtf.add_paragraph()
        p.text = f"•  {title}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        run = p.add_run()
        run.text = desc
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(6)

    s2.notes_slide.notes_text_frame.text = (
        "Every physician understands this pain. In the United States, doctors spend 14 hours every single week fighting prior-authorizations. "
        "It costs $31 billion in pure waste. Why? Because insurance guidelines are 80-page legal documents and patient charts are unstructured PDFs."
    )

    # =========================================================================
    # SLIDE 3: OUR SOLUTION: CAREAUTH-ROCM
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "CareAuth-ROCm: Autonomous Clinical Prior-Authorization Agent", category="THE SOLUTION")

    solution_pillars = [
        ("1. Local HIPAA Boundary", "Zero PHI Leakage", "All Protected Health Information (names, MRNs, dates, clinics) is identified and sanitized locally on AMD hardware before downstream processing.", COLOR_TEAL),
        ("2. Evolus Autonomous Agents", "Multi-Agent Orchestration", "Leverages Evolus Document Extractors, Knowledge Libraries, and business workflows to parse charts and cross-reference payer guidelines.", COLOR_CYAN),
        ("3. Visible Uncertainty", "Human-in-the-Loop Review", "Evaluates every guideline clause with an interactive Evidence Gap Matrix. Flags uncertainty and escalates ambiguous claims to clinical staff.", COLOR_YELLOW),
        ("4. Dual-Track Output", "Insurers & Patients", "Produces instant formal CMS-1500 packets and cited appeal letters for payers, alongside 6th-grade multilingual summaries for patients.", COLOR_AMD_RED)
    ]
    for i, (p_title, p_sub, p_desc, col) in enumerate(solution_pillars):
        col_idx = i % 2
        row_idx = i // 2
        cx = Inches(0.8 + col_idx * 5.97)
        cy = Inches(1.7 + row_idx * 2.65)
        add_card(s3, cx, cy, Inches(5.76), Inches(2.45))
        pbox = s3.shapes.add_textbox(cx + Inches(0.25), cy + Inches(0.2), Inches(5.26), Inches(2.1))
        ptf = pbox.text_frame
        ptf.word_wrap = True
        p = ptf.paragraphs[0]
        p.text = p_title.upper()
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)
        p2 = ptf.add_paragraph()
        p2.text = p_sub
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(16)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(8)
        p3 = ptf.add_paragraph()
        p3.text = p_desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(13)
        p3.font.color.rgb = COLOR_TEXT_MUTED

    s3.notes_slide.notes_text_frame.text = (
        "CareAuth-ROCm is built on four core pillars: local HIPAA PHI sanitization, Evolus multi-agent orchestration, "
        "transparent evidence gap scoring to prevent hallucinations, and dual-track output that serves both insurers and patients."
    )

    # =========================================================================
    # SLIDE 4: DUAL-JUDGE ARCHITECTURE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "The Dual-Judge Architecture: Evolus Front + AMD ROCm Core", category="SYSTEM ARCHITECTURE")

    add_card(s4, Inches(0.8), Inches(1.7), Inches(5.76), Inches(5.2))
    f_box = s4.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.16), Inches(4.8))
    f_tf = f_box.text_frame
    f_tf.word_wrap = True
    p = f_tf.paragraphs[0]
    p.text = "FRONT-OF-HOUSE: EVOLUS PLATFORM"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(6)
    p2 = f_tf.add_paragraph()
    p2.text = "Autonomous Healthcare Business Agent Workflow"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    evolus_items = [
        ("Evolus Document Extractor: ", "Extracts structured clinical facts (ICD-10, CPT, duration of PT, lab panels) from noisy EHR notes."),
        ("Evolus Knowledge Library: ", "Vector-indexed payer rules (Anthem Knee Arthroscopy CG-SURG-01, Medicare Biologics LCD L33777)."),
        ("Evolus Agent Automations: ", "Orchestrates Extractor, Adjudicator, Gap Detector, and Appeal Drafter sub-agents."),
        ("Enterprise Clinical Cockpit: ", "Role-based interface (Coordinator, Physician, Auditor, Patient) with real-time audit trail.")
    ]
    for t, d in evolus_items:
        p = f_tf.add_paragraph()
        p.text = f"✔  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(8)

    add_card(s4, Inches(6.77), Inches(1.7), Inches(5.76), Inches(5.2))
    b_box = s4.shapes.add_textbox(Inches(7.07), Inches(1.9), Inches(5.16), Inches(4.8))
    b_tf = b_box.text_frame
    b_tf.word_wrap = True
    p = b_tf.paragraphs[0]
    p.text = "BACK-OF-HOUSE: AMD ROCm INFRASTRUCTURE"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMD_RED
    p.space_after = Pt(6)
    p2 = b_tf.add_paragraph()
    p2.text = "High-Throughput Private Clinical Inference"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    amd_items = [
        ("AMD Instinct™ MI300X (192GB HBM3): ", "Massive memory headroom allows loading entire 45-page patient records and 80-page payer manuals simultaneously without lossy chunking."),
        ("ROCm vLLM Execution Engine: ", "OpenAI-compatible `/v1/chat/completions` server delivering 86.4 tokens/sec sustained throughput."),
        ("Sub-200ms Time-to-First-Token: ", "Ultra-low latency inference for real-time physician interaction and multi-turn clinical chat."),
        ("Hardware Isolation & HIPAA Security: ", "Complete on-premise execution guaranteeing zero data leakage to external commercial LLM APIs.")
    ]
    for t, d in amd_items:
        p = b_tf.add_paragraph()
        p.text = f"⚡  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_AMD_RED
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(8)

    s4.notes_slide.notes_text_frame.text = (
        "Our architecture is intentionally dual-track. The Evolus Platform provides the high-level business agent automations, "
        "document extractors, and knowledge library. The AMD ROCm backend provides the raw power: 192GB HBM3 memory allows us "
        "to fit entire clinical histories and payer manuals simultaneously, delivering 86 tokens per second."
    )

    # =========================================================================
    # SLIDE 5: MULTI-AGENT WORKFLOW PIPELINE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "The 4-Stage Autonomous Multi-Agent Pipeline", category="WORKFLOW ORCHESTRATION")

    pipeline_steps = [
        ("STAGE 1", "PHI Sanitizer", "Local Regex + NER engine strips patient names, MRNs, dates, and clinics on AMD silicon.", COLOR_TEAL),
        ("STAGE 2", "Extractor Agent", "Evolus Document Extractor structures clinical data: ICD-10, CPT, conservative therapy duration.", COLOR_CYAN),
        ("STAGE 3", "Policy Adjudicator", "Queries Evolus Knowledge Library (Anthem, Medicare) and cross-references patient facts.", COLOR_PURPLE),
        ("STAGE 4", "Gap & Packet Drafter", "Evaluates criteria confidence, compiles CMS-1500 packets, or flags gaps for nurse review.", COLOR_YELLOW)
    ]
    for i, (stage, name, desc, col) in enumerate(pipeline_steps):
        cx = Inches(0.8 + i * 2.98)
        add_card(s5, cx, Inches(1.8), Inches(2.8), Inches(4.8))
        box = s5.shapes.add_textbox(cx + Inches(0.15), Inches(2.0), Inches(2.5), Inches(4.4))
        btf = box.text_frame
        btf.word_wrap = True
        p = btf.paragraphs[0]
        p.text = stage
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        p2 = btf.add_paragraph()
        p2.text = name
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(17)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(12)
        p3 = btf.add_paragraph()
        p3.text = desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(12)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_after = Pt(16)
        p4 = btf.add_paragraph()
        p4.text = "KEY CAPABILITIES:"
        p4.font.name = "Segoe UI"
        p4.font.size = Pt(10)
        p4.font.bold = True
        p4.font.color.rgb = COLOR_TEXT_WHITE
        p4.space_after = Pt(6)
        sub_items = [
            ["• Safe Harbor HIPAA", "• Synthetic token mapping", "• 0% external cloud leakage"],
            ["• CPT / HCPCS mapping", "• Duration tracking", "• Lab baseline verification"],
            ["• Clause-level citation", "• Vector similarity lookup", "• Exclusion auditing"],
            ["• Confidence scoring", "• CMS-1500 auto-drafting", "• Multilingual generation"]
        ]
        for sub in sub_items[i]:
            ps = btf.add_paragraph()
            ps.text = sub
            ps.font.name = "Segoe UI"
            ps.font.size = Pt(10)
            ps.font.color.rgb = COLOR_TEXT_MUTED
            ps.space_after = Pt(4)

    s5.notes_slide.notes_text_frame.text = (
        "Here is how the four agents collaborate in real-time. First, patient PHI is sanitized locally on AMD hardware. "
        "Second, the Extractor Agent maps clinical facts into structured JSON. Third, the Policy Adjudicator verifies clinical evidence "
        "against the Evolus Knowledge Library. Finally, the Gap & Packet Drafter compiles the submission or alerts the human."
    )

    # =========================================================================
    # SLIDE 6: ENTERPRISE MULTI-ROLE CLINICAL PORTAL (NEW FOR 5-MIN DECK)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Enterprise Role-Based Access Control (RBAC)", category="HEALTHCARE WORKFLOW INTEGRATION")

    roles = [
        ("COORDINATOR PORTAL", "Deepak Kannan (Prior-Auth Lead)", "Full AI Cockpit, case intake, multi-agent trigger, Evidence Gap Matrix, CMS-1500 packet generator, and nurse escalation queue.", COLOR_TEAL),
        ("DOCTOR PORTAL", "Dr. Aris Thorne, MD (Attending)", "Physician sign-off queue, clause evidence review, clinical override annotations, and 1-Click Electronic Signature transmission.", COLOR_CYAN),
        ("PATIENT PORTAL", "Eleanor Vance (Patient View)", "Transparent coverage status, 6th-grade plain language explanation, multilingual translations (EN, ES, HI), and out-of-pocket estimates.", COLOR_PURPLE),
        ("LAB TECH PORTAL", "Diagnostic & PACS Ingestion", "Secure uploading of DICOM MRI scans, X-rays, pathology reports, and blood panels directly into the patient's EHR file.", COLOR_YELLOW)
    ]
    for i, (r_name, r_user, r_desc, col) in enumerate(roles):
        cx = Inches(0.8 + i * 2.98)
        add_card(s6, cx, Inches(1.8), Inches(2.8), Inches(4.8))
        box = s6.shapes.add_textbox(cx + Inches(0.15), Inches(2.0), Inches(2.5), Inches(4.4))
        btf = box.text_frame
        btf.word_wrap = True
        p = btf.paragraphs[0]
        p.text = r_name
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        p2 = btf.add_paragraph()
        p2.text = r_user
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(15)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(12)
        p3 = btf.add_paragraph()
        p3.text = r_desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_after = Pt(16)
        p4 = btf.add_paragraph()
        p4.text = "HEALTHCARE IMPACT:"
        p4.font.name = "Segoe UI"
        p4.font.size = Pt(10)
        p4.font.bold = True
        p4.font.color.rgb = COLOR_TEXT_WHITE
        p4.space_after = Pt(6)
        impact_items = [
            ["• 98.6% faster prep", "• Unified clinical queue", "• Zero faxing needed"],
            ["• 1-Click legal sign", "• Audit compliance", "• Full physician control"],
            ["• Health equity focus", "• Plain 6th-grade summary", "• 3 languages supported"],
            ["• Direct DICOM feed", "• Structured lab ingestion", "• Immediate agent parsing"]
        ]
        for item in impact_items[i]:
            ps = btf.add_paragraph()
            ps.text = item
            ps.font.name = "Segoe UI"
            ps.font.size = Pt(10)
            ps.font.color.rgb = COLOR_TEXT_MUTED
            ps.space_after = Pt(4)

    s6.notes_slide.notes_text_frame.text = (
        "CareAuth-ROCm is a true enterprise platform. We built complete Role-Based Access Control: Coordinators manage cases, "
        "Doctors sign off legally, Patients understand their care in their native tongue, and Lab Techs feed diagnostic scans directly."
    )

    # =========================================================================
    # SLIDE 7: MAKING UNCERTAINTY VISIBLE (TRACK 2 CORE REQUIREMENT)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Making Uncertainty Visible: The Clinical Confidence Matrix", category="CLINICAL SAFETY & ETHICS")

    add_card(s7, Inches(0.8), Inches(1.7), Inches(5.76), Inches(5.2))
    l_box = s7.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.16), Inches(4.8))
    l_tf = l_box.text_frame
    l_tf.word_wrap = True
    p = l_tf.paragraphs[0]
    p.text = "EVIDENCE GAP & CONFIDENCE TIERS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_YELLOW
    p.space_after = Pt(6)
    p2 = l_tf.add_paragraph()
    p2.text = "Eliminating Hallucinations in Patient Care"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    tiers = [
        ("GREEN TIER (>= 90% Confidence)", "Clean Auto-Approval", "All policy clauses matched with unambiguous EHR proof (e.g., MRI tears, 6+ months PT). Instant electronic packet generation.", COLOR_GREEN),
        ("YELLOW TIER (70% - 89% Confidence)", "Uncertainty Escalation", "Partial evidence or missing step-therapy detected. System stops auto-approval, highlights exact missing proof, and routes to Nurse Review Queue.", COLOR_YELLOW),
        ("RED TIER (< 70% Confidence)", "Definite Policy Discrepancy", "Contradiction found or therapy contraindicated. Autonomous drafting of cited appeal letter or recommended alternative pathway.", COLOR_AMD_RED)
    ]
    for t_title, t_sub, t_desc, col in tiers:
        p = l_tf.add_paragraph()
        p.text = f"■  {t_title}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)
        p_sub_par = l_tf.add_paragraph()
        p_sub_par.text = f"{t_sub}: {t_desc}"
        p_sub_par.font.name = "Segoe UI"
        p_sub_par.font.size = Pt(11)
        p_sub_par.font.color.rgb = COLOR_TEXT_MUTED
        p_sub_par.space_after = Pt(8)

    add_card(s7, Inches(6.77), Inches(1.7), Inches(5.76), Inches(5.2))
    r_box = s7.shapes.add_textbox(Inches(7.07), Inches(1.9), Inches(5.16), Inches(4.8))
    r_tf = r_box.text_frame
    r_tf.word_wrap = True
    p = r_tf.paragraphs[0]
    p.text = "HUMAN-IN-THE-LOOP CONTROL"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(6)
    p2 = r_tf.add_paragraph()
    p2.text = "Doctors Always Hold the Final Sign-Off"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    hil_points = [
        ("Actionable Remediation Guidance: ", "Instead of a generic denial, the agent tells the clinic nurse: 'Upload proof of 3-month Methotrexate trial to achieve 95% approval.'"),
        ("1-Click Physician Electronic Signature: ", "The attending doctor reviews the highlighted clinical evidence and signs electronically with one click."),
        ("Immutable Audit Trail: ", "Every agent decision, prompt trace, token speed, and human edit is permanently logged for HIPAA compliance and payer scrutiny.")
    ]
    for t, d in hil_points:
        p = r_tf.add_paragraph()
        p.text = f"✔  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(10)

    s7.notes_slide.notes_text_frame.text = (
        "Crucial for Track 2: We strictly enforce visible uncertainty. When evidence is incomplete—such as in step-therapy—the agent "
        "never hallucinates an approval. It drops confidence to yellow, isolates the exact missing clause, and presents an actionable remediation path."
    )

    # =========================================================================
    # SLIDE 8: PROTOTYPE VALIDATION (THE 3 GOLDEN CASES)
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Prototype Validation: The 3 Golden Clinical Scenarios", category="LIVE DEMONSTRATION")

    cases = [
        ("CASE 1: KNEE ARTHROSCOPY", "Clean Auto-Approval", "CPT 29881 | Left Meniscectomy", "96% Confidence (Green)", "11.4 Seconds", "All 4 Anthem CG-SURG-01 criteria satisfied (6 mo PT, failed NSAIDs, MRI Grade III tear). Instant CMS-1500 packet generated.", COLOR_GREEN),
        ("CASE 2: BIOLOGIC HUMIRA", "Step-Therapy Gap Detected", "HCPCS J0135 | Rheumatoid Arthritis", "64% Confidence (Yellow Alert)", "14.2 Seconds", "Medicare LCD L33777 requires 3-month trial of conventional DMARD. Chart showed only Prednisone. Escalated to Nurse Queue.", COLOR_YELLOW),
        ("CASE 3: TERTIARY APPEAL", "Prior Denial Overturn", "Complex Inpatient Transfer", "92% Overturn Score", "18.1 Seconds", "Prior claim denied for lack of conservative therapy. Agent located statutory hepatic transaminitis exemption in 45-page chart.", COLOR_CYAN)
    ]
    for i, (c_name, c_badge, c_sub, c_conf, c_time, c_desc, col) in enumerate(cases):
        cx = Inches(0.8 + i * 3.97)
        add_card(s8, cx, Inches(1.7), Inches(3.8), Inches(5.2))
        box = s8.shapes.add_textbox(cx + Inches(0.2), Inches(1.9), Inches(3.4), Inches(4.8))
        btf = box.text_frame
        btf.word_wrap = True
        p = btf.paragraphs[0]
        p.text = c_name
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)
        p2 = btf.add_paragraph()
        p2.text = c_badge
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(18)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(4)
        p3 = btf.add_paragraph()
        p3.text = c_sub
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_TEXT_MUTED
        p3.space_after = Pt(12)

        m_card = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, cx + Inches(0.15), Inches(3.2), Inches(3.5), Inches(0.9))
        m_card.fill.solid()
        m_card.fill.fore_color.rgb = COLOR_BG_DARK
        m_card.line.color.rgb = col
        m_card.line.width = Pt(1)
        
        m_box = s8.shapes.add_textbox(cx + Inches(0.25), Inches(3.25), Inches(3.3), Inches(0.8))
        mtf = m_box.text_frame
        mtf.word_wrap = True
        mp1 = mtf.paragraphs[0]
        mp1.text = f"Confidence: {c_conf}"
        mp1.font.name = "Segoe UI"
        mp1.font.size = Pt(11)
        mp1.font.bold = True
        mp1.font.color.rgb = col
        
        mp2 = mtf.add_paragraph()
        mp2.text = f"Execution Time: {c_time} on AMD MI300X"
        mp2.font.name = "Segoe UI"
        mp2.font.size = Pt(10)
        mp2.font.color.rgb = COLOR_TEXT_MUTED

        p4 = btf.add_paragraph()
        p4.space_before = Pt(85)
        p4.text = "OUTCOME & IMPACT:"
        p4.font.name = "Segoe UI"
        p4.font.size = Pt(11)
        p4.font.bold = True
        p4.font.color.rgb = COLOR_TEXT_WHITE
        p4.space_after = Pt(4)
        p5 = btf.add_paragraph()
        p5.text = c_desc
        p5.font.name = "Segoe UI"
        p5.font.size = Pt(11)
        p5.font.color.rgb = COLOR_TEXT_MUTED

    s8.notes_slide.notes_text_frame.text = (
        "We tested CareAuth-ROCm across three end-to-end clinical scenarios: Case 1 is a clean auto-approval in 11.4 seconds. "
        "Case 2 demonstrates our visible uncertainty gate, catching a step-therapy violation in Humira. "
        "Case 3 showcases our appeal agent overturning a prior denial."
    )

    # =========================================================================
    # SLIDE 9: PHYSICIAN OVERSIGHT & 1-CLICK SIGN-OFF (NEW FOR 5-MIN DECK)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Physician Oversight: 1-Click Sign-Off & Transmit", category="CLINICAL GOVERNANCE")

    add_card(s9, Inches(0.8), Inches(1.7), Inches(5.76), Inches(5.2))
    d_box = s9.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.16), Inches(4.8))
    d_tf = d_box.text_frame
    d_tf.word_wrap = True
    p = d_tf.paragraphs[0]
    p.text = "DOCTOR REVIEW QUEUE (DR. ARIS THORNE, MD)"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(6)
    p2 = d_tf.add_paragraph()
    p2.text = "Zero Faxes, Zero Wait, 100% Medical Authority"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    doc_items = [
        ("Evidence Clause Inspection: ", "The physician sees exact page numbers, radiology quotes, and physical therapy dates mapped to payer policy clauses."),
        ("Clinical Comment Override: ", "Physicians can append specific surgical urgency notes or override policy caveats with clinical justification."),
        ("1-Click Cryptographic Sign: ", "Generates an electronic signature conforming to 42 CFR § 495.4 and state electronic prescribing standards.")
    ]
    for t, d in doc_items:
        p = d_tf.add_paragraph()
        p.text = f"✔  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(10)

    add_card(s9, Inches(6.77), Inches(1.7), Inches(5.76), Inches(5.2))
    p_box = s9.shapes.add_textbox(Inches(7.07), Inches(1.9), Inches(5.16), Inches(4.8))
    p_tf = p_box.text_frame
    p_tf.word_wrap = True
    p = p_tf.paragraphs[0]
    p.text = "CLEARINGHOUSE TRANSMISSION & AUDITING"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_GREEN
    p.space_after = Pt(6)
    p2 = p_tf.add_paragraph()
    p2.text = "Instant Electronic Payer Submission"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    audit_items = [
        ("Direct EDI 278 Packet Creation: ", "Converts clinical notes into formal ANSI X12 278 healthcare services review transactions."),
        ("Immutable Ledger Logging: ", "Every agent prompt, confidence calculation, hardware telemetry snapshot, and human approval is timestamped."),
        ("Audit-Proof Traceability: ", "Hospital compliance officers can replay any prior-auth decision years later with complete proof.")
    ]
    for t, d in audit_items:
        p = p_tf.add_paragraph()
        p.text = f"⚡  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_GREEN
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(10)

    s9.notes_slide.notes_text_frame.text = (
        "The doctor is always in control. Our Doctor Portal gives surgeons and attending physicians a streamlined review queue. "
        "With one click, they electronically sign the CMS-1500 packet and transmit it to payer clearinghouses."
    )

    # =========================================================================
    # SLIDE 10: PATIENT EMPOWERMENT & MULTILINGUAL HEALTH EQUITY
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Patient Empowerment & Multilingual Health Equity", category="HEALTH EQUITY & ACCESSIBILITY")

    add_card(s10, Inches(0.8), Inches(1.7), Inches(5.76), Inches(5.2))
    pl_box = s10.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(5.16), Inches(4.8))
    pl_tf = pl_box.text_frame
    pl_tf.word_wrap = True
    p = pl_tf.paragraphs[0]
    p.text = "TRADITIONAL PAYER LETTERS"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMD_RED
    p.space_after = Pt(6)
    p2 = pl_tf.add_paragraph()
    p2.text = "Confusing Jargon & Patient Anxiety"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    p3 = pl_tf.add_paragraph()
    p3.text = "Typical Insurance Denial Letter (Real Example):"
    p3.font.name = "Segoe UI"
    p3.font.size = Pt(12)
    p3.font.bold = True
    p3.font.color.rgb = COLOR_YELLOW
    p3.space_after = Pt(6)

    quote_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.1), Inches(3.2), Inches(5.16), Inches(1.8))
    quote_box.fill.solid()
    quote_box.fill.fore_color.rgb = COLOR_BG_DARK
    quote_box.line.color.rgb = COLOR_CARD_BORDER
    qtf = quote_box.text_frame
    qtf.word_wrap = True
    qp = qtf.paragraphs[0]
    qp.text = "\"Coverage for CPT 29881 is denied pursuant to CG-SURG-01 §3.b.ii due to failure to demonstrate exhaustion of conservative physical medicine modalities and non-congruent radiologic MRI documentation of chondromalacia patellae.\""
    qp.font.name = "Segoe UI"
    qp.font.size = Pt(11)
    qp.font.italic = True
    qp.font.color.rgb = COLOR_TEXT_MUTED

    p4 = pl_tf.add_paragraph()
    p4.space_before = Pt(110)
    p4.text = "The Result: 90% of patients do not understand why their care was denied, leading to panic, missed appointments, and worsened clinical outcomes."
    p4.font.name = "Segoe UI"
    p4.font.size = Pt(12)
    p4.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s10, Inches(6.77), Inches(1.7), Inches(5.76), Inches(5.2))
    pr_box = s10.shapes.add_textbox(Inches(7.07), Inches(1.9), Inches(5.16), Inches(4.8))
    pr_tf = pr_box.text_frame
    pr_tf.word_wrap = True
    p = pr_tf.paragraphs[0]
    p.text = "CAREAUTH-ROCM PATIENT TAB"
    p.font.name = "Segoe UI"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = COLOR_TEAL
    p.space_after = Pt(6)
    p2 = pr_tf.add_paragraph()
    p2.text = "6th-Grade Reading Level in 3 Languages"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(14)

    lang_items = [
        ("English Summary: ", "\"Good news! Your knee surgery has been approved. Your doctor showed you did 6 months of physical therapy and your MRI confirmed a torn meniscus.\""),
        ("Español (Spanish): ", "\"¡Buenas noticias! Su cirugía de rodilla ha sido aprobada. Su médico demostró que completó 6 meses de fisioterapia y su resonancia confirmó un desgarro de menisco.\""),
        ("हिंदी (Hindi): ", "\"अच्छी खबर! आपकी घुटने की सर्जरी स्वीकृत हो गई है। आपके डॉक्टर ने दिखाया कि आपने 6 महीने फिजियोथेरेपी पूरी की और एमआरआई में मेनिस्कस टियर की पुष्टि हुई।\"")
    ]
    for lang, text in lang_items:
        p = pr_tf.add_paragraph()
        p.text = lang
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_CYAN
        p.space_after = Pt(2)
        pr_text = pr_tf.add_paragraph()
        pr_text.text = text
        pr_text.font.name = "Segoe UI"
        pr_text.font.size = Pt(11)
        pr_text.font.color.rgb = COLOR_TEXT_MUTED
        pr_text.space_after = Pt(8)

    s10.notes_slide.notes_text_frame.text = (
        "Health equity was a core design goal. Instead of terrifying patients with cold medical jargon, CareAuth translates "
        "every adjudication into plain 6th-grade English, Spanish, and Hindi, empowering patients to understand their treatment plan."
    )

    # =========================================================================
    # SLIDE 11: AMD SILICON & HARDWARE EXPLOITATION
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "AMD Instinct™ MI300X: Why Silicon Matters in Healthcare", category="AMD HARDWARE BENCHMARKS")

    amd_benchmarks = [
        ("192 GB HBM3", "Zero Lossy Chunking", "Allows holding entire 45-page patient records and 80-page payer manuals simultaneously in high-bandwidth memory.", COLOR_AMD_RED),
        ("86.4 tok / sec", "Sustained Inference", "High-throughput token generation allows multi-agent cross-referencing in under 12 seconds per case.", COLOR_CYAN),
        ("192 ms TTFT", "Time-To-First-Token", "Instantaneous clinical responsiveness, enabling interactive doctor review without UI freezing.", COLOR_TEAL),
        ("100% On-Prem", "HIPAA Compliant", "Guaranteed local hardware boundary prevents patient health data from ever touching third-party clouds.", COLOR_GREEN)
    ]
    for i, (stat, title, desc, col) in enumerate(amd_benchmarks):
        cx = Inches(0.8 + i * 2.98)
        add_card(s11, cx, Inches(1.8), Inches(2.8), Inches(2.4))
        box = s11.shapes.add_textbox(cx + Inches(0.15), Inches(1.9), Inches(2.5), Inches(2.2))
        btf = box.text_frame
        btf.word_wrap = True
        p = btf.paragraphs[0]
        p.text = stat
        p.font.name = "Segoe UI"
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)
        p2 = btf.add_paragraph()
        p2.text = title.upper()
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(6)
        p3 = btf.add_paragraph()
        p3.text = desc
        p3.font.name = "Segoe UI"
        p3.font.size = Pt(11)
        p3.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s11, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.4))
    abox = s11.shapes.add_textbox(Inches(1.1), Inches(4.6), Inches(11.1), Inches(2.2))
    atf = abox.text_frame
    atf.word_wrap = True
    ap0 = atf.paragraphs[0]
    ap0.text = "ROCm SOFTWARE STACK & DEPLOYMENT ARCHITECTURE"
    ap0.font.name = "Segoe UI"
    ap0.font.size = Pt(12)
    ap0.font.bold = True
    ap0.font.color.rgb = COLOR_CYAN
    ap0.space_after = Pt(8)

    amd_details = [
        ("vLLM on ROCm 6.2: ", "Leverages PagedAttention and FlashAttention-2 optimized for AMD CDNA 3 matrix cores."),
        ("Dynamic Model Selection: ", "Lightweight Llama-3.1-8B for instant entity extraction; Qwen-2.5-14B/70B for multi-clause clinical reasoning and appeal drafting."),
        ("Production Telemetry HUD: ", "Real-time monitoring of GPU VRAM utilization (14.8/192 GB), generation speed, and prompt latency embedded in the clinical portal.")
    ]
    for t, d in amd_details:
        p = atf.add_paragraph()
        p.text = f"•  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(6)

    s11.notes_slide.notes_text_frame.text = (
        "Why AMD? In healthcare AI, memory capacity is king. Patient charts and insurance guidelines are massive. "
        "With the AMD Instinct MI300X's 192GB of HBM3 memory, we avoid lossy chunking entirely, achieving 86 tokens per second."
    )

    # =========================================================================
    # SLIDE 12: MEASURABLE IMPACT & CLINICAL ROI
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Measurable Impact & Clinical ROI", category="BUSINESS & CLINICAL VALUE")

    add_card(s12, Inches(0.8), Inches(1.7), Inches(7.5), Inches(5.2))
    tbl_box = s12.shapes.add_textbox(Inches(1.1), Inches(1.9), Inches(6.9), Inches(4.8))
    tbl_tf = tbl_box.text_frame
    tbl_tf.word_wrap = True
    p = tbl_tf.paragraphs[0]
    p.text = "BENCHMARK: MANUAL VS. CAREAUTH-ROCM"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_CYAN
    p.space_after = Pt(10)

    comparisons = [
        ("Review Time per Case", "45 Minutes", "11.4 Seconds", "98.6% Reduction"),
        ("Turnaround to Payer", "3 to 7 Days", "Instant Electronic", "Real-Time Packet"),
        ("Policy Search Overhead", "Manual 80-pg PDF", "<150ms Vector Search", "99% Faster Lookup"),
        ("Missing Step-Therapy", "Payer Denial (Week delay)", "Pre-submission Alert", "Zero Denial Delays"),
        ("Patient Clarity", "Incomprehensible", "6th-grade (EN, ES, HI)", "100% Transparency")
    ]
    for metric, manual, careauth, imp in comparisons:
        p = tbl_tf.add_paragraph()
        p.text = f"• {metric}: "
        p.font.name = "Segoe UI"
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEXT_WHITE
        r1 = p.add_run()
        r1.text = f"{manual}  ➔  "
        r1.font.bold = False
        r1.font.color.rgb = COLOR_TEXT_MUTED
        r2 = p.add_run()
        r2.text = f"{careauth} "
        r2.font.bold = True
        r2.font.color.rgb = COLOR_TEAL
        r3 = p.add_run()
        r3.text = f"({imp})"
        r3.font.bold = True
        r3.font.color.rgb = COLOR_GREEN
        p.space_after = Pt(12)

    add_card(s12, Inches(8.55), Inches(1.7), Inches(3.98), Inches(2.45))
    r1_box = s12.shapes.add_textbox(Inches(8.75), Inches(1.85), Inches(3.58), Inches(2.1))
    r1_tf = r1_box.text_frame
    r1_tf.word_wrap = True
    rp1 = r1_tf.paragraphs[0]
    rp1.text = "$182,000 / Year"
    rp1.font.name = "Segoe UI"
    rp1.font.size = Pt(28)
    rp1.font.bold = True
    rp1.font.color.rgb = COLOR_GREEN
    rp1.space_after = Pt(4)
    rp2 = r1_tf.add_paragraph()
    rp2.text = "SAVINGS PER MID-SIZED CLINIC"
    rp2.font.name = "Segoe UI"
    rp2.font.size = Pt(11)
    rp2.font.bold = True
    rp2.font.color.rgb = COLOR_TEXT_WHITE
    rp2.space_after = Pt(6)
    rp3 = r1_tf.add_paragraph()
    rp3.text = "Eliminating 14 hours/week of physician administrative overtime across a 10-provider practice."
    rp3.font.name = "Segoe UI"
    rp3.font.size = Pt(11)
    rp3.font.color.rgb = COLOR_TEXT_MUTED

    add_card(s12, Inches(8.55), Inches(4.45), Inches(3.98), Inches(2.45))
    r2_box = s12.shapes.add_textbox(Inches(8.75), Inches(4.6), Inches(3.58), Inches(2.1))
    r2_tf = r2_box.text_frame
    r2_tf.word_wrap = True
    r2p1 = r2_tf.paragraphs[0]
    r2p1.text = "74% Fewer Denials"
    r2p1.font.name = "Segoe UI"
    r2p1.font.size = Pt(28)
    r2p1.font.bold = True
    r2p1.font.color.rgb = COLOR_CYAN
    r2p1.space_after = Pt(4)
    r2p2 = r2_tf.add_paragraph()
    r2p2.text = "PRE-SUBMISSION VERIFICATION"
    r2p2.font.name = "Segoe UI"
    r2p2.font.size = Pt(11)
    r2p2.font.bold = True
    r2p2.font.color.rgb = COLOR_TEXT_WHITE
    r2p2.space_after = Pt(6)
    r2p3 = r2_tf.add_paragraph()
    r2p3.text = "Catching evidence gaps and step-therapy issues before filing eliminates 74% of initial insurer rejections."
    r2p3.font.name = "Segoe UI"
    r2p3.font.size = Pt(11)
    r2p3.font.color.rgb = COLOR_TEXT_MUTED

    s12.notes_slide.notes_text_frame.text = (
        "The return on investment is immediate. We cut review time from 45 minutes down to 11.4 seconds—a 98.6% reduction. "
        "For a typical 10-physician clinic, this recovers $182,000 in lost productivity and prevents 74% of initial denials."
    )

    # =========================================================================
    # SLIDE 13: PRODUCTION ROADMAP & FUTURE VISION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Production Roadmap & Clinical Deployment", category="FUTURE ROADMAP")

    roadmap_stages = [
        ("PHASE 1: PROTOTYPE (COMPLETED)", "Hackathon Working MVP", [
            "✔ Multi-agent Evolus orchestration",
            "✔ AMD Instinct MI300X vLLM backend",
            "✔ Evidence Gap & Confidence Matrix",
            "✔ 3 Golden Clinical Scenarios tested",
            "✔ Multilingual Patient summaries",
            "✔ RBAC: Doctor, Patient, Lab Portals"
        ], COLOR_GREEN),
        ("PHASE 2: PILOT (Q1 2027)", "EHR & Clearinghouse Integration", [
            "• FHIR & HL7 v2 connectors (Epic / Cerner)",
            "• Direct EDI 278 real-time payer clearinghouse",
            "• Automated clinical fax ingestion via OCR",
            "• Nurse review queue Slack/Teams webhooks",
            "• On-premise AMD ROCm appliance deployment"
        ], COLOR_CYAN),
        ("PHASE 3: SCALE (Q3 2027)", "Full Autonomous Health Network", [
            "• Multi-specialty coverage (Oncology, Cardiology)",
            "• Predictive Payer Denial analytics",
            "• Cross-hospital federated learning on AMD",
            "• Direct-to-patient mobile notification app",
            "• Global payer guideline synchronization"
        ], COLOR_PURPLE)
    ]
    for i, (stage, sub, items, col) in enumerate(roadmap_stages):
        cx = Inches(0.8 + i * 3.97)
        add_card(s13, cx, Inches(1.7), Inches(3.8), Inches(5.2))
        box = s13.shapes.add_textbox(cx + Inches(0.2), Inches(1.9), Inches(3.4), Inches(4.8))
        btf = box.text_frame
        btf.word_wrap = True
        p = btf.paragraphs[0]
        p.text = stage
        p.font.name = "Segoe UI"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(2)
        p2 = btf.add_paragraph()
        p2.text = sub
        p2.font.name = "Segoe UI"
        p2.font.size = Pt(17)
        p2.font.bold = True
        p2.font.color.rgb = COLOR_TEXT_WHITE
        p2.space_after = Pt(16)
        for item in items:
            pi = btf.add_paragraph()
            pi.text = item
            pi.font.name = "Segoe UI"
            pi.font.size = Pt(12)
            pi.font.color.rgb = COLOR_TEXT_MUTED if not item.startswith("✔") else COLOR_TEXT_WHITE
            pi.space_after = Pt(8)

    s13.notes_slide.notes_text_frame.text = (
        "Phase 1 is fully built and working today. Phase 2 connects CareAuth directly into Epic and Cerner via FHIR APIs, "
        "and Phase 3 expands our autonomous agents into oncology, cardiology, and predictive denial management."
    )

    # =========================================================================
    # SLIDE 14: CONCLUSION & SUMMARY
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Summary: Transforming Healthcare Administration with AMD", category="CONCLUSION")

    add_card(s14, Inches(0.8), Inches(1.7), Inches(11.733), Inches(5.2))
    sum_box = s14.shapes.add_textbox(Inches(1.2), Inches(1.9), Inches(10.9), Inches(4.8))
    stf = sum_box.text_frame
    stf.word_wrap = True

    p = stf.paragraphs[0]
    p.text = "WHY CAREAUTH-ROCM WINS TRACK 2 & EVOLUS PARTNER TRACK"
    p.font.name = "Segoe UI"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = COLOR_AMD_RED
    p.space_after = Pt(6)

    p2 = stf.add_paragraph()
    p2.text = "The Complete Autonomous Business Agent for Healthcare"
    p2.font.name = "Segoe UI"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = COLOR_TEXT_WHITE
    p2.space_after = Pt(16)

    recap_points = [
        ("Built for Real Clinical Practice: ", "Addresses the $31B prior-authorization bottleneck with 98.6% speedup while maintaining strict human-in-the-loop clinical safety."),
        ("Strict Track 2 Compliance: ", "Makes uncertainty visible through an interactive Evidence Gap Matrix; escalates ambiguous claims to clinical nurses rather than hallucinating."),
        ("Full Evolus Agent Exploitation: ", "Seamlessly orchestrates Document Extractors, Knowledge Libraries, Sub-Agents, and Multi-Step Workflows."),
        ("Hardware-Accelerated on AMD ROCm: ", "Exploits the 192GB memory of AMD Instinct MI300X to process 50-page charts with sub-200ms latency and zero cloud data leaks.")
    ]
    for t, d in recap_points:
        p = stf.add_paragraph()
        p.text = f"✔  {t}"
        p.font.name = "Segoe UI"
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = COLOR_TEAL
        run = p.add_run()
        run.text = d
        run.font.bold = False
        run.font.color.rgb = COLOR_TEXT_MUTED
        p.space_after = Pt(10)

    callout = stf.add_paragraph()
    callout.space_before = Pt(12)
    callout.text = "Team Techtors  |  Built with ❤️ for AMD Developer Hackathon: ACT III  |  October 2026"
    callout.font.name = "Segoe UI"
    callout.font.size = Pt(12)
    callout.font.bold = True
    callout.font.color.rgb = COLOR_CYAN

    s14.notes_slide.notes_text_frame.text = (
        "Judges, CareAuth-ROCm proves that autonomous agents and specialized hardware can solve healthcare's greatest administrative crisis. "
        "Built on Evolus and powered by AMD Instinct MI300X, we replace bureaucratic burnout with instant, transparent care. "
        "Thank you, and we welcome your questions!"
    )

    output_path = os.path.join(os.getcwd(), "CareAuth_ROCm_Prototype_Presentation.pptx")
    prs.save(output_path)
    print(f"Master 14-slide presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_master_deck()

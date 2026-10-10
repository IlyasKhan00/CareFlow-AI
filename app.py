from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st

from ai_engine import analyze_request, analyze_bed_flow


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="CareFlow AI | Operations Intelligence",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

st.markdown(
    """
    <style>
    @import url(
      'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap'
    );

    :root {
      --cf-bg: #08111f;
      --cf-panel: #101c2d;
      --cf-panel-2: #142338;
      --cf-border: rgba(153,185,215,.16);
      --cf-muted: #9baec3;
      --cf-text: #edf5ff;
      --cf-teal: #5eead4;
      --cf-blue: #78aaff;
      --cf-violet: #b7a2ff;
    }

    html, body, [class*="css"] {
      font-family: 'DM Sans', sans-serif;
    }

    .stApp {
      background:
        radial-gradient(
          ellipse at 82% 0%,
          rgba(42,105,140,.18),
          transparent 36%
        ),
        radial-gradient(
          ellipse at 8% 16%,
          rgba(93,74,158,.12),
          transparent 28%
        ),
        var(--cf-bg);
      color: var(--cf-text);
    }

    [data-testid="stHeader"] {
      background: rgba(8,17,31,.78);
    }

    [data-testid="stSidebar"] {
      background: linear-gradient(
        180deg,
        #0c1828 0%,
        #0a1422 100%
      );
      border-right: 1px solid var(--cf-border);
    }

    [data-testid="stSidebar"] > div {
      padding-top: 1.4rem;
    }

    h1, h2, h3 {
      font-family: 'Manrope', sans-serif !important;
      letter-spacing: -.035em;
    }

    h1 {
      font-weight: 800 !important;
    }

    h2, h3 {
      font-weight: 700 !important;
    }

    p, label, .stMarkdown {
      color: var(--cf-text);
    }

    .block-container {
      padding-top: 1.7rem;
      padding-bottom: 2.8rem;
      max-width: 1500px;
    }

    div[data-testid="stMetric"] {
      background: linear-gradient(
        145deg,
        rgba(20,35,56,.96),
        rgba(13,26,43,.96)
      );
      border: 1px solid var(--cf-border);
      padding: 17px 19px;
      border-radius: 17px;
      box-shadow: 0 10px 30px rgba(0,0,0,.10);
    }

    div[data-testid="stMetricLabel"] {
      color: var(--cf-muted) !important;
      font-size: .82rem;
    }

    div[data-testid="stMetricValue"] {
      color: var(--cf-text) !important;
      font-family: 'Manrope', sans-serif;
      font-weight: 800;
    }

    div[data-testid="stForm"],
    div[data-testid="stExpander"],
    div[data-testid="stDataFrame"] {
      border: 1px solid var(--cf-border);
      border-radius: 16px;
      background: rgba(16,28,45,.58);
    }

    div[data-testid="stExpander"] summary {
      font-weight: 600;
    }

    .cf-eyebrow {
      color: var(--cf-teal);
      text-transform: uppercase;
      letter-spacing: .15em;
      font-size: .72rem;
      font-weight: 800;
      margin-bottom: .45rem;
    }

    .cf-title {
      font-family: 'Manrope', sans-serif;
      font-size: 2.45rem;
      font-weight: 800;
      letter-spacing: -.06em;
      line-height: 1.08;
      color: #f2f7ff;
    }

    .cf-subtitle {
      color: var(--cf-muted);
      font-size: 1rem;
      margin-top: .65rem;
      max-width: 780px;
      line-height: 1.6;
    }

    .cf-banner {
      background: linear-gradient(
        115deg,
        rgba(26,58,75,.95),
        rgba(29,35,68,.92)
      );
      border: 1px solid rgba(94,234,212,.22);
      border-radius: 19px;
      padding: 22px 24px;
      margin: 1rem 0 1.25rem 0;
    }

    .cf-banner-title {
      font-family: 'Manrope', sans-serif;
      font-size: 1.15rem;
      font-weight: 800;
      margin-bottom: .45rem;
      color: #f2f7ff;
    }

    .cf-banner-copy {
      color: #c2d4e7;
      line-height: 1.55;
      font-size: .93rem;
    }

    .cf-panel {
      background: linear-gradient(
        150deg,
        rgba(18,32,51,.98),
        rgba(13,25,41,.98)
      );
      border: 1px solid var(--cf-border);
      border-radius: 18px;
      padding: 20px 21px;
      height: 100%;
    }

    .cf-panel-label {
      color: var(--cf-muted);
      font-size: .78rem;
      text-transform: uppercase;
      letter-spacing: .1em;
      font-weight: 700;
    }

    .cf-panel-value {
      font-family: 'Manrope', sans-serif;
      font-size: 1.65rem;
      font-weight: 800;
      margin-top: .5rem;
      color: #f2f7ff;
    }

    .cf-small {
      color: var(--cf-muted);
      font-size: .82rem;
      line-height: 1.5;
      margin-top: .3rem;
    }

    .cf-section-note {
      color: var(--cf-muted);
      margin-top: -.5rem;
      margin-bottom: 1rem;
      font-size: .91rem;
    }

    .cf-side-brand {
      font-family: 'Manrope', sans-serif;
      font-size: 1.32rem;
      font-weight: 800;
      letter-spacing: -.04em;
      color: #f2f7ff;
    }

    .cf-side-sub {
      color: var(--cf-muted);
      font-size: .8rem;
      line-height: 1.45;
      margin-top: .35rem;
    }

    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button {
      border-radius: 10px;
      font-weight: 700;
      border: 1px solid rgba(120,170,255,.25);
      transition: all .15s ease;
    }

    div.stButton > button[kind="primary"],
    div.stFormSubmitButton > button[kind="primary"] {
      background: linear-gradient(
        100deg,
        #54dbc8,
        #83aaff
      );
      color: #071521;
      border: none;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
      transform: translateY(-1px);
      border-color: var(--cf-teal);
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea,
    div[data-baseweb="select"] > div {
      background-color: #0c1929 !important;
    }

    hr {
      border-color: var(--cf-border) !important;
    }

    .cf-footer {
      color: #8399b1;
      font-size: .78rem;
      border-top: 1px solid var(--cf-border);
      padding-top: 1rem;
      margin-top: 2rem;
    }

    /* CareFlow opening sequence + page-transition motion */
    @keyframes cfSplashFadeOut {
      0%, 72% { opacity: 1; visibility: visible; }
      100% { opacity: 0; visibility: hidden; pointer-events: none; }
    }

    @keyframes cfLogoRise {
      0% {
        opacity: 0;
        transform: translateY(18px) scale(.96);
        filter: blur(7px);
      }
      65% { opacity: 1; filter: blur(0); }
      100% {
        opacity: 1;
        transform: translateY(0) scale(1);
        filter: blur(0);
      }
    }

    @keyframes cfOrbPulse {
      0%, 100% {
        transform: scale(.94);
        box-shadow: 0 0 22px rgba(94,234,212,.18),
                    0 0 55px rgba(120,170,255,.10);
      }
      50% {
        transform: scale(1.06);
        box-shadow: 0 0 36px rgba(94,234,212,.35),
                    0 0 85px rgba(120,170,255,.22);
      }
    }

    @keyframes cfLoadingSweep {
      0% { transform: translateX(-110%); }
      100% { transform: translateX(240%); }
    }

    @keyframes cfPageEnter {
      0% {
        opacity: .12;
        transform: translateY(22px);
        filter: blur(5px);
      }
      55% {
        opacity: .78;
        filter: blur(1.5px);
      }
      100% {
        opacity: 1;
        transform: translateY(0);
        filter: blur(0);
      }
    }

    .cf-intro-overlay {
      position: fixed;
      inset: 0;
      z-index: 999999;
      display: flex;
      align-items: center;
      justify-content: center;
      background:
        radial-gradient(
          ellipse at 50% 42%,
          rgba(24,73,91,.42),
          transparent 34%
        ),
        radial-gradient(
          ellipse at 50% 55%,
          rgba(65,55,123,.24),
          transparent 50%
        ),
        #07101d;
      animation: cfSplashFadeOut 2.65s ease forwards;
      pointer-events: none;
    }

    .cf-intro-content {
      text-align: center;
      padding: 24px;
      animation: cfLogoRise 1.15s cubic-bezier(.2,.8,.2,1) both;
    }

    .cf-intro-orb {
      width: 82px;
      height: 82px;
      margin: 0 auto 25px;
      border-radius: 26px;
      display: grid;
      place-items: center;
      font-size: 38px;
      color: #071521;
      background: linear-gradient(135deg, #5eead4, #78aaff 68%, #b7a2ff);
      animation: cfOrbPulse 1.65s ease-in-out infinite;
    }

    .cf-intro-title {
      font-family: 'Manrope', sans-serif;
      color: #f2f7ff;
      font-weight: 800;
      letter-spacing: -.055em;
      font-size: clamp(2.25rem, 6vw, 4rem);
    }

    .cf-intro-title span {
      color: #5eead4;
    }

    .cf-intro-sub {
      margin-top: 11px;
      color: #9baec3;
      font-size: .8rem;
      letter-spacing: .22em;
      font-weight: 700;
    }

    .cf-intro-track {
      height: 3px;
      width: 180px;
      margin: 28px auto 0;
      border-radius: 9px;
      overflow: hidden;
      background: rgba(153,185,215,.15);
    }

    .cf-intro-track span {
      display: block;
      width: 42%;
      height: 100%;
      border-radius: inherit;
      background: linear-gradient(90deg, #5eead4, #78aaff);
      animation: cfLoadingSweep 1.05s ease-in-out infinite;
    }

    @media (prefers-reduced-motion: reduce) {
      .cf-intro-overlay,
      .cf-intro-content,
      .cf-intro-orb {
        animation: none !important;
      }
      .cf-intro-overlay {
        opacity: 0;
        visibility: hidden;
      }
    }

    @media (max-width: 800px) {
      .cf-title {
        font-size: 2rem;
      }

      .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
      }
    }
    </style>
    """,
    unsafe_allow_html=True,
)
# ============================================================
# SESSION STATE
# ============================================================

show_careflow_intro = not st.session_state.get("cf_intro_seen", False)

if "tickets" not in st.session_state:
    st.session_state.tickets = []

if "inventory" not in st.session_state:
    st.session_state.inventory = [
        {
            "item": "Disposable gloves",
            "category": "PPE",
            "stock": 30,
            "minimum": 150,
            "unit": "boxes",
            "status": "Review needed",
        },
        {
            "item": "Portable monitors",
            "category": "Equipment",
            "stock": 7,
            "minimum": 5,
            "unit": "units",
            "status": "In range",
        },
        {
            "item": "Cleaning kits",
            "category": "Facilities",
            "stock": 18,
            "minimum": 25,
            "unit": "kits",
            "status": "Review needed",
        },
        {
            "item": "Hand sanitiser",
            "category": "PPE",
            "stock": 46,
            "minimum": 30,
            "unit": "bottles",
            "status": "In range",
        },
        {
            "item": "Printer labels",
            "category": "Supplies",
            "stock": 9,
            "minimum": 20,
            "unit": "rolls",
            "status": "Review needed",
        },
    ]

if "beds" not in st.session_state:
    st.session_state.beds = [
        {"bed_id": "A-01", "unit": "Unit A", "status": "Available"},
        {"bed_id": "A-02", "unit": "Unit A", "status": "Occupied"},
        {"bed_id": "A-03", "unit": "Unit A", "status": "Cleaning"},
        {"bed_id": "A-04", "unit": "Unit A", "status": "Blocked"},
        {"bed_id": "B-01", "unit": "Unit B", "status": "Available"},
        {"bed_id": "B-02", "unit": "Unit B", "status": "Occupied"},
        {"bed_id": "B-03", "unit": "Unit B", "status": "Available"},
        {"bed_id": "B-04", "unit": "Unit B", "status": "Cleaning"},
        {"bed_id": "C-01", "unit": "Unit C", "status": "Occupied"},
        {"bed_id": "C-02", "unit": "Unit C", "status": "Available"},
        {"bed_id": "C-03", "unit": "Unit C", "status": "Blocked"},
        {"bed_id": "C-04", "unit": "Unit C", "status": "Occupied"},
    ]

URGENCY_ORDER = {"High": 0, "Medium": 1, "Low": 2}

EXAMPLES = {
    "Equipment unavailable": (
        "The portable monitoring device in Ward B is unavailable. "
        "The operations team needs to check whether a replacement is "
        "available and confirm the expected repair time."
    ),
    "Delayed bed cleaning": (
        "A bed is awaiting cleaning, but the cleaning team has not "
        "confirmed when it will be ready. The ward coordinator needs "
        "an updated status."
    ),
    "Facilities problem": (
        "The air conditioning in the outpatient waiting area is not "
        "working. Facilities staff have not provided an estimated "
        "repair time."
    ),
    "Supply shortage": (
        "The central store reports that several boxes of gloves are "
        "running low. The inventory team needs to verify stock and "
        "arrange replenishment."
    ),
    "Staffing request": (
        "The evening shift coordinator reports that one scheduled "
        "operations support worker has not arrived. The staffing "
        "coordinator needs to confirm coverage."
    ),
}


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown(
        '<div class="cf-side-brand">✦ CareFlow '
        '<span style="color:#5eead4">AI</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="cf-side-sub">'
        'HOSPITAL OPERATIONS INTELLIGENCE</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "WORKSPACE",
        ["Overview", "Operations requests", "Bed flow", "Inventory"],
    )

    st.divider()
    st.markdown("#### Quick test scenarios")

    selected_example = st.selectbox(
        "Load an example",
        ["Write my own"] + list(EXAMPLES.keys()),
    )

    if selected_example != "Write my own":
        st.caption(EXAMPLES[selected_example])

    st.divider()
    st.markdown("#### Responsible AI")
    st.caption(
        "Synthetic demo data only. AI recommendations require "
        "human review and are not clinical triage."
    )
    st.info(
        "Never enter real patient identifiers, confidential medical "
        "information, or sensitive operational data."
    )


# Animate the main workspace when the selected section changes.
previous_page = st.session_state.get("cf_previous_page")
if previous_page is not None and previous_page != page:
    st.markdown(
        "<style>.main .block-container { animation: cfPageEnter 1.6s "
        "cubic-bezier(.16,1,.3,1) both; }</style>",
        unsafe_allow_html=True,
    )
st.session_state.cf_previous_page = page


# One-time branded opening sequence for each fresh Streamlit session.
if show_careflow_intro:
    st.markdown(
        '<div class="cf-intro-overlay" aria-hidden="true">'
        '<div class="cf-intro-content">'
        '<div class="cf-intro-orb">✦</div>'
        '<div class="cf-intro-title">CareFlow <span>AI</span></div>'
        '<div class="cf-intro-sub">HOSPITAL OPERATIONS INTELLIGENCE</div>'
        '<div class="cf-intro-track"><span></span></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )
    st.session_state.cf_intro_seen = True
# ============================================================
# INVENTORY INTELLIGENCE HELPERS
# ============================================================

def inventory_status(item):
    """Return a deterministic stock status from configured thresholds.

    Critical: zero stock, or at/below 25% of the configured minimum.
    Low: below minimum but not critical.
    In range: at or above minimum.
    """
    stock = max(0, int(item.get("stock", 0)))
    minimum = max(0, int(item.get("minimum", 0)))

    if stock == 0:
        return "CRITICAL — OUT OF STOCK"
    if minimum > 0 and stock <= max(1, minimum * 0.25):
        return "CRITICAL — RESTOCK NOW"
    if stock < minimum:
        return "LOW — RESTOCK REVIEW"
    return "IN RANGE"


def inventory_context_text(items):
    """Create a factual inventory snapshot for Gemini; no actions are taken."""
    lines = []
    for item in items:
        lines.append(
            f"- {item['item']} | category: {item['category']} | "
            f"available stock: {int(item['stock'])} {item['unit']} | "
            f"minimum threshold: {int(item['minimum'])} {item['unit']} | "
            f"status: {inventory_status(item)}"
        )
    return "\n".join(lines) if lines else "No inventory records are available."


def inventory_alerts(items):
    """Return critical and low-stock records using Python-calculated rules."""
    return [
        item for item in items
        if inventory_status(item).startswith(("CRITICAL", "LOW"))
    ]


# ============================================================
# SHARED DATA AND METRICS
# ============================================================

tickets = st.session_state.tickets
inventory = st.session_state.inventory
beds = st.session_state.beds

open_tickets = [
    ticket for ticket in tickets
    if ticket["status"] == "Open"
]

high_tickets = [
    ticket for ticket in open_tickets
    if ticket["analysis"].get("urgency") == "High"
]

resolved_tickets = [
    ticket for ticket in tickets
    if ticket["status"] == "Resolved"
]

stock_alerts = inventory_alerts(inventory)
critical_stock = [
    item for item in inventory
    if inventory_status(item).startswith("CRITICAL")
]
low_stock = [
    item for item in inventory
    if inventory_status(item).startswith(("CRITICAL", "LOW"))
]
inventory_context = inventory_context_text(inventory)

bed_counts = {
    status: sum(
        1 for bed in beds if bed["status"] == status
    )
    for status in ["Available", "Occupied", "Cleaning", "Blocked"]
}


def bed_flow_context_text(beds):
    """Create a compact snapshot of bed states for Gemini, without patient data."""
    statuses = ["Available", "Occupied", "Cleaning", "Blocked"]
    lines = [f"Total tracked demo beds: {len(beds)}"]

    for status in statuses:
        count = sum(1 for bed in beds if bed.get("status") == status)
        lines.append(f"{status}: {count}")

    units = sorted({str(bed.get("unit", "Unknown")) for bed in beds})
    lines.append("Counts by unit:")

    for unit in units:
        unit_beds = [
            bed for bed in beds
            if str(bed.get("unit", "Unknown")) == unit
        ]
        unit_counts = {
            status: sum(
                1 for bed in unit_beds
                if bed.get("status") == status
            )
            for status in statuses
        }
        lines.append(
            f"- {unit}: "
            + ", ".join(
                f"{status}={count}"
                for status, count in unit_counts.items()
            )
        )

    lines.append("Bed records (ID, unit, operational status):")
    for bed in beds:
        lines.append(
            f"- {bed.get('bed_id', 'Unknown')}, "
            f"{bed.get('unit', 'Unknown')}, "
            f"{bed.get('status', 'Unknown')}"
        )

    return "\n".join(lines)


def page_header(eyebrow, title, subtitle):
    st.markdown(
        f'<div class="cf-eyebrow">{eyebrow}</div>'
        f'<div class="cf-title">{title}</div>'
        f'<div class="cf-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def render_metrics():
    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Open requests",
        len(open_tickets),
        help="Unresolved operational requests in this session",
    )

    c2.metric(
        "High urgency · review",
        len(high_tickets),
        help="AI-suggested urgency; human review required",
    )

    c3.metric(
        "Beds available",
        bed_counts["Available"],
        help="Synthetic bed board",
    )

    c4.metric(
        "Stock alerts",
        len(low_stock),
        delta=f"{len(critical_stock)} critical",
        delta_color="inverse" if critical_stock else "off",
        help="Critical and low-stock items based on configured thresholds",
    )


# ============================================================
# REQUEST INTAKE
# ============================================================

def ticket_intake():
    st.markdown("### ✦ Capture an operational issue")

    st.markdown(
        '<div class="cf-section-note">'
        'Gemini structures the request into a reviewable operational record.'
        '</div>',
        unsafe_allow_html=True,
    )

    initial_text = (
        EXAMPLES[selected_example]
        if selected_example != "Write my own"
        else ""
    )

    with st.form("request_form", clear_on_submit=False):
        request_text = st.text_area(
            "Describe the operational issue",
            value=initial_text,
            height=150,
            max_chars=4000,
            placeholder=(
                "Example: A piece of equipment is unavailable "
                "and a replacement has not been confirmed."
            ),
            help="Use fictional, non-identifiable examples only.",
        )

        submitted = st.form_submit_button(
            "✦ Analyze with Gemini",
            type="primary",
            use_container_width=True,
        )

    if not submitted:
        return

    if not request_text.strip():
        st.warning("Please enter an operational request.")
        return

    # Basic phrase-based safeguard for obvious examples; this is NOT a reliable
    # emergency detector. Real incidents must be reported through facility procedures.
    emergency_phrases = [
        "killing the patients",
        "killing patients",
        "attacking patients",
        "dog attacking",
        "animal attacking",
        "active shooter",
        "person with a weapon",
        "bomb threat",
        "fire in the hospital",
        "explosion in the hospital",
        "patients are being attacked",
    ]
    normalized_request = request_text.casefold()

    if any(phrase in normalized_request for phrase in emergency_phrases):
        st.error("🚨 Potential life-safety emergency")
        st.write(
            "If this describes a real event, immediately alert hospital security "
            "and activate the facility’s emergency response procedure. Contact "
            "local emergency services if required, keep away from the danger, and "
            "follow authorized emergency personnel’s instructions. Do not wait for AI analysis."
        )
        st.warning(
            "This basic safeguard has not verified the incident. No AI assessment "
            "was performed and no ticket was created."
        )
        return

    with st.spinner(
        "Analyzing the request with Gemini… This may take up to 30 seconds."
    ):
        try:
            analysis = analyze_request(
                request_text.strip(),
                inventory_context=inventory_context,
            )
            analysis_data = analysis.model_dump()

            if not analysis_data.get("in_scope", True):
                st.markdown("### CareFlow AI response")

                explanation = (
                    analysis_data.get("plain_language_explanation")
                    or analysis_data.get("scope_reason")
                    or (
                        "CareFlow handles non-clinical hospital operations, "
                        "including equipment, supplies, facilities, staffing, "
                        "and bed-flow coordination."
                    )
                )

                st.write(explanation)
                st.info(
                    "This request is outside CareFlow's scope. "
                    "No ticket was created."
                )
                return

            ticket = {
                "id": str(uuid4())[:8].upper(),
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "request": request_text.strip(),
                "analysis": analysis_data,
                "status": "Open",
                "owner": "Unassigned",
            }

            st.session_state.tickets.append(ticket)

            st.markdown("### CareFlow AI response")
            st.write(
                analysis_data.get("plain_language_explanation")
                or analysis_data.get("summary")
                or "Analysis completed. Please review the ticket."
            )

            badge_col1, badge_col2 = st.columns(2)
            badge_col1.metric(
                "Category",
                analysis_data.get("category", "Other"),
            )
            badge_col2.metric(
                "Suggested urgency",
                analysis_data.get("urgency", "Low"),
            )

            with st.expander("Review the analysis details", expanded=True):
                st.markdown("**What happened**")
                st.write(
                    analysis_data.get("summary") or "No summary supplied."
                )

                st.markdown("**Why this urgency was suggested**")
                st.write(
                    analysis_data.get("reason") or "Human review is required."
                )

                st.markdown("**Recommended next step**")
                st.write(
                    analysis_data.get("suggested_action")
                    or "Refer to the relevant operations team."
                )

                missing = analysis_data.get("missing_information", [])
                if missing:
                    st.markdown("**Information still needed**")
                    for item in missing[:3]:
                        st.write(f"• {item}")

                st.caption(
                    "AI-generated operational guidance. Human review is required; "
                    "this is not clinical triage."
                )

            st.success(
                f"Ticket #{ticket['id']} created. "
                "Review the recommendation before acting."
            )

            # Do not rerun here: it would clear the immediate response.
            # The ticket appears in the queue on the next interaction or rerun.

        except Exception as exc:
            st.error(
                "CareFlow could not analyze this request. No ticket was created."
            )
            st.write(str(exc))
            with st.expander("Technical details"):
                st.code(f"{type(exc).__name__}: {exc}")


# ============================================================
# TICKET DETAILS
# ============================================================

def show_ticket(ticket):
    analysis = ticket["analysis"]
    urgency = analysis.get("urgency", "Medium")

    icon = (
        "🔴" if urgency == "High"
        else "🟡" if urgency == "Medium"
        else "🟢"
    )

    with st.expander(
        f"{icon} {urgency} · "
        f"{analysis.get('category', 'Other')} · "
        f"#{ticket['id']}"
    ):
        st.markdown("**What this means**")
        st.write(
            analysis.get("plain_language_explanation")
            or analysis.get("summary")
            or "No explanation available."
        )

        st.markdown("**Quick summary**")
        st.write(analysis.get("summary", "No summary available."))

        st.markdown("**Original request**")
        st.write(ticket["request"])

        a, b = st.columns(2)

        with a:
            st.markdown("**Why this urgency was suggested**")
            st.write(analysis.get("reason", "No reason supplied."))

        with b:
            st.markdown("**Suggested operational action**")
            st.write(
                analysis.get(
                    "suggested_action",
                    "Human review required.",
                )
            )

        st.markdown("**Missing information**")
        missing = analysis.get("missing_information", [])

        if missing:
            for item in missing:
                st.write(f"• {item}")
        else:
            st.write("No missing information identified by the AI.")

        st.caption(
            f"Created {ticket['created_at']} · "
            f"Owner: {ticket.get('owner', 'Unassigned')} · "
            f"Status: {ticket['status']}"
        )

        st.warning(
            "Human review required. This is an operational suggestion, "
            "not a clinical triage or diagnostic decision."
        )

        col1, col2 = st.columns(2)

        owners = [
            "Unassigned",
            "Operations",
            "Facilities",
            "Inventory",
            "Bed management",
            "Staffing",
        ]

        with col1:
            current_owner = ticket.get("owner", "Unassigned")
            if current_owner not in owners:
                current_owner = "Unassigned"

            owner = st.selectbox(
                "Request owner",
                owners,
                index=owners.index(current_owner),
                key=f"owner_{ticket['id']}",
            )
            ticket["owner"] = owner

        with col2:
            if ticket["status"] == "Open":
                if st.button(
                    "✓ Mark resolved",
                    key=f"resolve_{ticket['id']}",
                    use_container_width=True,
                ):
                    ticket["status"] = "Resolved"
                    st.rerun()
            else:
                st.success("Resolved")
# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":
    page_header(
        "OPERATIONS INTELLIGENCE / LIVE SESSION",
        "Operations command center",
        (
            "A unified view of operational requests, bed flow and supply "
            "risks — designed to support staff coordination, "
            "not clinical decisions."
        ),
    )

    banner_copy = (
        f"There are <b>{len(open_tickets)} open requests</b>, including "
        f"<b>{len(high_tickets)} AI-flagged high-urgency items</b>. "
        f"The synthetic bed board shows "
        f"<b>{bed_counts['Available']} available beds</b> and "
        f"<b>{bed_counts['Cleaning']} awaiting cleaning</b>. "
        f"<b>{len(low_stock)} inventory items</b> are below their "
        "configured minimum. Verify these signals with the responsible teams."
    )

    st.markdown(
        '<div class="cf-banner">'
        '<div class="cf-banner-title">✦ CareFlow intelligence brief</div>'
        f'<div class="cf-banner-copy">{banner_copy}</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    render_metrics()
    st.write("")

    left, right = st.columns([1.15, 0.85], gap="large")

    with left:
        st.markdown("### Request activity")

        if tickets:
            df = pd.DataFrame([
                {
                    "Created": ticket["created_at"],
                    "Category": ticket["analysis"].get("category", "Other"),
                    "Suggested urgency": ticket["analysis"].get(
                        "urgency", "Medium"
                    ),
                    "Status": ticket["status"],
                    "ID": ticket["id"],
                }
                for ticket in tickets
            ])

            counts = (
                df["Category"]
                .value_counts()
                .rename_axis("Category")
                .reset_index(name="Requests")
            )

            st.bar_chart(
                counts.set_index("Category"),
                use_container_width=True,
            )

            st.dataframe(
                df.sort_values("Created", ascending=False),
                use_container_width=True,
                hide_index=True,
            )

        else:
            st.markdown(
                '<div class="cf-panel">'
                '<div class="cf-panel-label">Request analytics</div>'
                '<div class="cf-panel-value">'
                'Ready for your first request</div>'
                '<div class="cf-small">'
                'As requests are analyzed, this area will chart categories '
                'and show the session queue.</div></div>',
                unsafe_allow_html=True,
            )

    with right:
        st.markdown("### Bed-flow snapshot")

        bed_df = pd.DataFrame([
            {"Status": status, "Beds": count}
            for status, count in bed_counts.items()
        ])

        st.bar_chart(
            bed_df.set_index("Status"),
            use_container_width=True,
        )

        st.markdown("### Inventory watchlist")

        if low_stock:
            for item in low_stock:
                status = inventory_status(item)
                is_critical = status.startswith("CRITICAL")

                if is_critical:
                    st.error(
                        f"🚨 {status}: {item['item']} — "
                        f"{item['stock']} {item['unit']} left "
                        f"(minimum: {item['minimum']})."
                    )
                else:
                    st.warning(
                        f"⚠️ {status}: {item['item']} — "
                        f"{item['stock']} {item['unit']} left "
                        f"(minimum: {item['minimum']})."
                    )
        else:
            st.success(
                "No inventory items are below their configured minimums."
            )

    st.caption(
        "Inventory and bed figures are synthetic demo records. "
        "Request metrics come from the current session."
    )


# ============================================================
# OPERATIONS REQUESTS
# ============================================================

elif page == "Operations requests":
    page_header(
        "WORK QUEUE",
        "Operations requests",
        (
            "Capture requests, review operational follow-up, "
            "assign ownership and track resolution."
        ),
    )

    render_metrics()
    st.write("")

    intake_col, queue_col = st.columns([0.9, 1.1], gap="large")

    with intake_col:
        ticket_intake()

    with queue_col:
        st.markdown("### Request queue")

        filters = st.columns(2)

        with filters[0]:
            status_filter = st.selectbox(
                "Status",
                ["All", "Open", "Resolved"],
                key="request_status_filter",
            )

        with filters[1]:
            urgency_filter = st.selectbox(
                "Suggested urgency",
                ["All", "High", "Medium", "Low"],
                key="request_urgency_filter",
            )

        ordered = sorted(
            tickets,
            key=lambda ticket: (
                ticket["status"] != "Open",
                URGENCY_ORDER.get(
                    ticket["analysis"].get("urgency", "Medium"),
                    1,
                ),
                ticket["created_at"],
            ),
        )

        visible = [
            ticket for ticket in ordered
            if (
                status_filter == "All"
                or ticket["status"] == status_filter
            )
            and (
                urgency_filter == "All"
                or ticket["analysis"].get("urgency") == urgency_filter
            )
        ]

        if not visible:
            st.info(
                "No matching requests yet. Load a sample from the sidebar "
                "or submit your own fictional scenario."
            )

        for ticket in visible:
            show_ticket(ticket)

    st.divider()
    st.markdown("### Exportable request register")

    if tickets:
        rows = [
            {
                "Request ID": ticket["id"],
                "Category": ticket["analysis"].get("category"),
                "Suggested urgency": ticket["analysis"].get("urgency"),
                "Owner": ticket.get("owner", "Unassigned"),
                "Status": ticket["status"],
                "Created": ticket["created_at"],
            }
            for ticket in tickets
        ]

        frame = pd.DataFrame(rows)

        st.dataframe(
            frame,
            use_container_width=True,
            hide_index=True,
        )

        st.download_button(
            "Download request register (CSV)",
            frame.to_csv(index=False),
            "careflow_requests.csv",
            "text/csv",
        )
    else:
        st.caption(
            "The register will populate when you analyze a request."
        )


# ============================================================
# BED FLOW
# ============================================================

elif page == "Bed flow":
    page_header(
        "CAPACITY COORDINATION",
        "Bed flow & transfer readiness",
        (
            "A simple operational board for availability, cleaning "
            "and blocked-bed follow-up. All records are synthetic."
        ),
    )

    st.markdown(
        '<div class="cf-banner">'
        '<div class="cf-banner-title">Coordination principle</div>'
        '<div class="cf-banner-copy">'
        'This board tracks operational states only. It does not contain '
        'patient assignments or make admission, discharge or clinical decisions.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    cols = st.columns(4)

    for col, label in zip(
        cols,
        ["Available", "Occupied", "Cleaning", "Blocked"],
    ):
        col.metric(label, bed_counts[label])

    st.markdown("### ✦ AI Bed Flow Insights")
    st.caption(
        "Gemini reviews the current synthetic bed-board snapshot and suggests "
        "operational follow-ups. It does not make admission, discharge, "
        "or clinical decisions."
    )

    if "bed_flow_insights" not in st.session_state:
        st.session_state.bed_flow_insights = ""

    if st.button(
        "Analyze current bed flow with Gemini",
        type="primary",
        key="analyze_bed_flow",
    ):
        current_context = bed_flow_context_text(beds)

        with st.spinner("Gemini is reviewing the bed-flow snapshot…"):
            try:
                st.session_state.bed_flow_insights = analyze_bed_flow(
                    current_context
                )
                st.session_state.bed_flow_insights_error = ""
            except Exception as exc:
                st.session_state.bed_flow_insights = ""
                st.session_state.bed_flow_insights_error = str(exc)

    if st.session_state.get("bed_flow_insights_error"):
        st.error(st.session_state.bed_flow_insights_error)

    if st.session_state.bed_flow_insights:
        st.markdown(st.session_state.bed_flow_insights)
        st.info(
            "AI-generated operational suggestions only. Verify the bed board "
            "and obtain authorized human approval before taking action."
        )

    status_options = [
        "Available",
        "Occupied",
        "Cleaning",
        "Blocked",
    ]

    with st.expander("Update a demo bed status"):
        with st.form("bed_update_form"):
            bed_ids = [bed["bed_id"] for bed in beds]

            chosen_bed = st.selectbox("Demo bed", bed_ids)
            new_status = st.selectbox(
                "New operational status",
                status_options,
            )

            update_bed = st.form_submit_button(
                "Save bed status",
                type="primary",
            )

        if update_bed:
            for bed in beds:
                if bed["bed_id"] == chosen_bed:
                    bed["status"] = new_status
                    break

            st.success(f"Demo bed {chosen_bed} updated.")
            st.rerun()

    status_color = {
        "Available": "#5eead4",
        "Occupied": "#78aaff",
        "Cleaning": "#fbbf24",
        "Blocked": "#fb7185",
    }

    unit_cols = st.columns(3)

    for idx, unit in enumerate(sorted(set(bed["unit"] for bed in beds))):
        with unit_cols[idx % 3]:
            st.markdown(f"#### {unit}")

            for bed in [
                bed for bed in beds
                if bed["unit"] == unit
            ]:
                color = status_color[bed["status"]]

                st.markdown(
                    '<div class="cf-panel" '
                    'style="padding:13px 15px;margin-bottom:9px">'
                    '<div style="display:flex;justify-content:space-between;'
                    'align-items:center">'
                    f'<b>{bed["bed_id"]}</b>'
                    f'<span style="color:{color};font-size:.78rem;'
                    f'font-weight:800">● {bed["status"]}</span>'
                    '</div>'
                    '<div class="cf-small">'
                    'Synthetic bed record · no patient data'
                    '</div></div>',
                    unsafe_allow_html=True,
                )

    st.markdown("### Transfer follow-up checklist")
    st.caption("Illustrative checklist; it is not a live hospital feed.")

    st.checkbox("Confirm receiving unit's operational readiness")
    st.checkbox("Verify cleaning completion with the responsible team")
    st.checkbox(
        "Confirm any blocked-bed reason with an authorized coordinator"
    )
    st.checkbox("Record a human-approved status update")


# ============================================================
# INVENTORY
# ============================================================

elif page == "Inventory":
    page_header(
        "RESOURCE READINESS",
        "Inventory & shortage intelligence",
        (
            "Monitor demo stock against configured minimums and "
            "prepare restock actions for human approval."
        ),
    )

    st.markdown(
        '<div class="cf-banner">'
        '<div class="cf-banner-title">Inventory watch</div>'
        '<div class="cf-banner-copy">'
        'Shortage flags are calculated from the synthetic stock values below. '
        'They are not connected to a real inventory system.'
        '</div></div>',
        unsafe_allow_html=True,
    )

    low_stock = inventory_alerts(inventory)
    critical_stock = [
        item for item in inventory
        if inventory_status(item).startswith("CRITICAL")
    ]

    if critical_stock:
        st.error(
            "🚨 CRITICAL STOCK WARNING — review replenishment immediately."
        )

        for item in critical_stock:
            st.error(
                f"{item['item']}: only {item['stock']} {item['unit']} remain. "
                f"Minimum threshold: {item['minimum']} {item['unit']}. "
                "Notify the authorized inventory team and verify stock before ordering."
            )
    elif low_stock:
        st.warning(
            "⚠️ Some supplies are below their configured minimum. "
            "Review restocking."
        )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Tracked items", len(inventory))
    c2.metric("Critical", len(critical_stock))
    c3.metric("Below minimum", len(low_stock))
    c4.metric("Inventory items", len(inventory))
)
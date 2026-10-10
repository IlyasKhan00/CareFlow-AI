# CareFlow AI 🏥
### AI-Powered Healthcare Operations Assistant

**Built by Team THE TECHIES | AICON’26 — Build With AI | Health Operations**

CareFlow AI is an AI-powered healthcare operations dashboard designed to help hospital teams organize operational requests, understand bed-flow bottlenecks, and monitor critical medical inventory.

By combining Google's Gemini AI with structured operational data, CareFlow AI transforms operational requests into understandable summaries and actionable recommendations, helping staff make more informed decisions while keeping humans in control.

> **Important:** CareFlow AI is a prototype for healthcare operations support. It uses synthetic demonstration data and is not intended for diagnosis, treatment decisions, or autonomous emergency response.

---

## ✨ Key Features

### 1. AI-Powered Operations Request Analysis
- Converts operational requests into clear, plain-language explanations.
- Categorizes incoming requests.
- Assesses urgency and explains the reasoning behind the assessment.
- Identifies missing information.
- Suggests practical next steps.
- Flags requests that require human review.

### 2. Intelligent Bed-Flow Insights
- Presents a hospital bed-board overview.
- Helps identify potential bed-flow bottlenecks.
- Uses Gemini to generate operational insights from the available bed context.
- Supports staff in understanding where operational attention may be needed.

### 3. Medical Inventory Monitoring
- Displays available inventory and stock levels.
- Highlights low-stock items and inventory concerns.
- Provides a centralized view of inventory status.

### 4. Operations Dashboard
- Summarizes key operational indicators.
- Organizes requests, beds, and inventory in one interface.
- Provides a unified view of the demonstration hospital's operational data.

### 5. Human-in-the-Loop Safeguards
- AI-generated assessments are recommendations, not final decisions.
- Human review remains essential.
- Inventory alerts and other deterministic checks are handled by application logic where implemented.
- Emergency phrase detection, where present, is only a basic safeguard and must not be relied upon as an emergency detection system.

---

## 🧠 How It Works

1. **Operational input:** A user provides an operational request or views existing demonstration data.
2. **Context preparation:** The application prepares the relevant information for analysis.
3. **AI analysis:** Google's Gemini model interprets supported requests and produces structured insights.
4. **Validation:** The application validates AI output against predefined data schemas.
5. **Operational presentation:** Results are displayed in the dashboard for staff to review.
6. **Human oversight:** Authorized staff evaluate recommendations and decide what action to take.

The application combines AI-generated insights with conventional application logic. AI is not used as a substitute for clinical judgment or established hospital procedures.

---

## 🛠️ Technology Stack

- **Python** — application logic and data processing
- **Streamlit** — interactive web dashboard
- **Google Gemini** — AI-powered request analysis and bed-flow insights
- **Google Gen AI SDK** — model integration
- **Pydantic** — structured output validation
- **Pandas** — tabular data handling

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12 recommended
- A Google Gemini API key
- Internet access for Gemini API calls

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd careflow-ai
```

Replace the placeholder with your actual GitHub repository URL.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can run the virtual environment's Python executable directly instead.

### 3. Install dependencies

If the repository contains a `requirements.txt` file:

```powershell
python -m pip install -r requirements.txt
```

### 4. Configure your API key

Create the following file:

```text
.streamlit/secrets.toml
```

Add your Gemini API key and the model configuration used by the project:

```toml
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GEMINI_MODEL = "gemini-3.1-flash-lite"
```

Replace `YOUR_GEMINI_API_KEY` with your own key.

**Security:** Never commit `secrets.toml`, API keys, or other credentials to GitHub. Keep secrets in Streamlit's deployment secrets configuration when hosting the application.

### 5. Run the application

```powershell
python -m streamlit run app.py
```

Streamlit will display a local URL, usually:

```text
http://localhost:8501
```

Open the URL in your browser to use CareFlow AI.

---

## 📁 Project Structure

```text
careflow-ai/
├── app.py                  # Streamlit dashboard and user interface
├── ai_engine.py            # Gemini integration and AI analysis
├── schemas.py              # Structured output models and validation
├── requirements.txt        # Python dependencies
├── .streamlit/
│   └── secrets.toml        # Local secrets; do not commit
├── .gitignore              # Files excluded from version control
└── README.md               # Project documentation
```

*The structure above describes the expected core project files. Adjust it if your repository uses a different layout.*

---

## 🔐 Privacy, Safety & Limitations

CareFlow AI is a demonstration prototype, not a certified hospital information system.

- **Synthetic data:** Demonstration records should not contain real patient information.
- **Human oversight:** Staff must verify AI-generated recommendations before acting on them.
- **No clinical diagnosis:** The system is designed for operational support, not medical diagnosis or treatment.
- **AI limitations:** Model output can be incomplete, incorrect, or inconsistent.
- **Emergency limitations:** Basic keyword detection cannot reliably identify every emergency. Existing emergency procedures must always take priority.
- **Data security:** API credentials must be stored securely and excluded from source control.
- **Validation:** Structured output validation helps enforce expected formats but does not guarantee that an AI recommendation is factually correct.

Before any real-world deployment, the system would require appropriate security reviews, privacy safeguards, operational validation, reliability testing, and institutional approval.

---

## 🎯 Project Goal

CareFlow AI explores how generative AI can support healthcare operations by making operational information easier to interpret and helping teams identify issues that may need attention.

The goal is to demonstrate a practical human-in-the-loop AI workflow that brings together operational visibility, structured analysis, and actionable insights.

---

## 🏆 Built for AICON’26

**Event:** Build With AI  
**Category:** Health Operations  
**Team:** THE TECHIES  
**Project:** CareFlow AI

Built to explore the responsible use of AI in healthcare operations.

---

## 📌 Future Improvements

- Role-based access controls and audit trails
- Integration with validated hospital information systems
- More comprehensive bed-flow analytics
- Configurable inventory thresholds and replenishment workflows
- Automated testing and monitoring of AI output quality
- Accessibility and multilingual support
- Stronger operational safeguards and deployment security

---

*CareFlow AI is an educational prototype. All operational recommendations require human verification.*

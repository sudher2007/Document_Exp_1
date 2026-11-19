# Document-Grounded Q&A Chatbot (SRS v1.0 Compliance)

A full-stack web application chatbot developed with **Django REST Framework** and **React.js (Vite)**, strictly adhering to the **Software Requirements Specification (SRS v1.0)** and Google Gemini API guidelines.

---

## 🌟 Key Features

### 1. Meridian College Policy Manual Fed for RAG
- The complete 12-page **Meridian College of Arts and Science Institutional Policy Manual (First Edition, 2026-27)** provided in the SRS is generated and indexed for Retrieval-Augmented Generation (RAG).
- **1-Click Preloading**: The college policy manual is indexed out-of-the-box or can be reloaded at any time with one click.
- **Direct PDF Download**: Users can download the generated 12-page PDF file directly from the UI or API endpoint (`/api/download-policy-pdf/`).
- **Custom Uploads**: Supports uploading any other PDF, DOCX, or TXT document (drag-and-drop or file picker) up to 20 MB and 100 pages with magic-byte verification (rejects masked executables).

### 2. Complete Feed of SRS System Prompts & Guardrails
- **SRS Reference System Prompt (v1.0)** enforced on every request:
  - Answers only questions relating to the provided document.
  - Retrieves passages to summarize, explain, and answer questions.
  - Quotes short passages and cites source pages and section headings.
  - Strictly adheres to document ground truth; no outside guessing.
  - Treats documents as data, not instructions.
- **SRS Standard Refusal Messages (Section 4.3)**:
  - *Information not found*: `"I couldn't find that information in the uploaded document. You can try rephrasing your question or ask about something the document covers."`
  - *Unrelated question*: `"I can only help with questions about the uploaded document. Please ask something related to its content."`
- **Low Temperature (0.2)**: Configured in Django settings and UI modal for zero unsupported statements.
- **Multi-layered Guardrails**:
  - Prompt injection detection (TC-07, TC-08).
  - Out-of-domain / general knowledge query detection (TC-05).
  - Retrieval score threshold (FR-R-04).
  - Multi-turn conversation history (last 10 turns per FR-H-01, FR-H-02).
  - Expandable source citation cards showing page numbers and quoted snippets.

---

## 🏗️ Project Architecture

```
EXP_4/
├── backend/
│   ├── backend/
│   │   ├── settings.py           # Django settings, CORS, Gemini config, limits
│   │   ├── urls.py               # API route definitions and static/dist serving
│   │   └── wsgi.py
│   ├── chatbot/
│   │   ├── models.py             # ChatSession, Document, Chunk, Message
│   │   ├── serializers.py        # DRF Serializers
│   │   ├── views.py              # REST API endpoints (Upload, Chat, Policy, Settings)
│   │   ├── services/
│   │   │   ├── extractor.py      # Magic-byte check, PDF/DOCX/TXT text extraction
│   │   │   ├── chunker.py        # Overlapping chunker with page & heading tracking
│   │   │   └── rag_engine.py     # Gemini API client, Guardrails, local fallback
│   │   ├── tests.py              # Acceptance tests (TC-01 through TC-08)
│   │   └── urls.py
│   ├── generate_policy_pdf.py    # ReportLab script generating the 12-page policy PDF
│   └── meridian_college_policy_manual.pdf
├── frontend/
│   ├── src/
│   │   ├── App.jsx               # React UI with document panel, chat & settings
│   │   ├── App.css               # Modern design system & responsive styling
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .env                          # Server environment configuration
├── .env.example
└── README.md
```

---

## 🚀 Running the Application

### Prerequisites
- Python 3.11+
- Node.js 18+ and npm

### 1. Start the Django Back End
```bash
cd backend
python manage.py migrate
python manage.py runserver 127.0.0.1:8000
```
The Django API will be live at `http://127.0.0.1:8000/`.

### 2. Start the React Front End
In a separate terminal:
```bash
cd frontend
npm run dev
```
Open your browser at `http://localhost:5173/`.
*(Alternatively, Django also serves the production-built React app directly at `http://127.0.0.1:8000/`)*.

---

## 🧪 Running Automated Tests

To run the automated acceptance test suite verifying all SRS requirements (TC-01 through TC-08):
```bash
cd backend
python manage.py test chatbot
```

Test Results:
- `test_tc01_load_college_policy_manual`: Validates 12 pages and chunk indexing.
- `test_tc02_reject_fake_pdf`: Validates magic-byte validation rejecting executable disguised as PDF.
- `test_tc03_ask_grounded_question_attendance`: Grounded retrieval on page 4 attendance condonation.
- `test_tc04_summarize_section`: Section 2 admission policy summary with page citations.
- `test_tc05_offtopic_question_refusal`: Refuses general knowledge query with standard SRS refusal message.
- `test_tc06_info_not_found_refusal`: Refuses missing topics with standard SRS missing info message.
- `test_tc07_prompt_injection_resistance`: Resists instruction overrides.
- `test_tc08_clear_chat_history`: Clears conversation while preserving document context.

---

## 🔑 Setting the Google Gemini API Key

You can configure your Google Gemini API key in two convenient ways:
1. **Via UI**: Click **Settings** in the top navigation bar, paste your API key, select your preferred model (`gemini-2.5-flash`, `gemini-1.5-flash`, `gemini-2.0-flash`, or `gemini-2.5-pro`), and click **Save**.
2. **Via `.env` file**: Add your key to `.env` in the root directory:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
*Note: If no API key is configured, the application automatically uses its built-in high-accuracy grounded extraction engine so it remains fully interactive, grounded, and testable.*

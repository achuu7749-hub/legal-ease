# LegalEase — AI-Powered Legal Document Generator

A complete Streamlit + FastAPI application for drafting editable legal documents with Google Gemini and exporting TXT, DOCX, and PDF.

## Features
- Draft employment contracts, NDAs, leases, service agreements, and custom documents.
- FastAPI `POST /generate` endpoint with Pydantic validation.
- Gemini model configured via `.env` (`GEMINI_MODEL`).
- Editable Streamlit preview and TXT/DOCX/PDF exports.
- DOCX/PDF formatting and API error handling.

> **Important:** This is a drafting aid, not a lawyer or legal advice. AI output can be inaccurate or incomplete. Review all details and obtain qualified local legal review before signing. Do not submit highly sensitive personal information unless you understand the provider's data handling terms.

## Requirements
- Python 3.10+ (Python 3.11 recommended)
- VS Code and Python extension
- Gemini API key from Google AI Studio

The source documentation specifies Gemini 1.5 Pro. Model availability can change, so this implementation defaults to configurable `gemini-2.5-flash`. Set `GEMINI_MODEL` to a model currently available to your key.

## VS Code setup (Windows PowerShell)
1. Extract this folder and open it in VS Code (`File → Open Folder`).
2. Open **Terminal → New Terminal**.
3. Create and activate a virtual environment:
   ```powershell
   py -3.11 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt and run `.venv\Scripts\activate.bat`.
4. Install dependencies:
   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env` and add your real `GEMINI_API_KEY`. Never commit `.env`.

### macOS/Linux environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
```
Edit `.env` with your Gemini key.

## Run the app
Open **two VS Code terminals**, activate `.venv` in each.

**Terminal 1 — backend:**
```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Check `http://127.0.0.1:8000/` and interactive API docs at `http://127.0.0.1:8000/docs`.

**Terminal 2 — frontend:**
```bash
streamlit run app.py
```
Open the local Streamlit URL shown in the terminal (usually `http://localhost:8501`).

## Test
```bash
pytest -q
```
Then test manually:
1. Enter document type, parties, and semicolon-separated terms.
2. Click **Generate Document**.
3. Edit the returned text.
4. Download TXT, DOCX, and PDF; open each file to verify formatting.
5. Visit `/docs`, expand `POST /generate`, and submit a JSON body such as:
   ```json
   {"document_type":"NDA","parties":"A (Discloser), B (Recipient)","terms":"Keep business information confidential;Term: 2 years","effective_date":"2026-09-24","jurisdiction":"India","additional_instructions":"Use plain English"}
   ```

## API
- `GET /` — health/status
- `POST /generate` — validates inputs and returns `{ "document": "...", "model": "..." }`

## Docker (optional)
With Docker Desktop running and `.env` configured:
```bash
docker compose up --build
```
Frontend: `http://localhost:8501`; backend: `http://localhost:8000`.

## Project structure
```text
legalease/
├── ai_core/gemini_generator.py
├── services/formatters.py
├── tests/test_formatters.py
├── app.py                 # Streamlit frontend
├── main.py                # FastAPI app
├── routes.py              # API routes and validation
├── requirements.txt
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── Procfile
```

## Troubleshooting
- **API key not configured:** ensure `.env` is in the project root and contains `GEMINI_API_KEY=...`; restart backend.
- **Model not found/access denied:** set `GEMINI_MODEL` to a currently supported model enabled for your API key.
- **Frontend cannot connect:** backend must be running on port 8000; check `BACKEND_URL`.
- **PDF font limitations:** the built-in PDF font replaces unsupported glyphs; DOCX is preferable for multilingual text.

import os
from datetime import date
import requests
import streamlit as st
from dotenv import load_dotenv
from services.formatters import format_docx, format_pdf, sanitize_text

load_dotenv()
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "120"))
st.set_page_config(page_title="LegalEase", page_icon="⚖️", layout="wide")
st.markdown("<style>.stApp{background:#0e1117}.block-container{max-width:1100px;padding-top:2rem}.legal-card{background:#171b24;border:1px solid #303644;border-radius:12px;padding:20px;color:#e8eaf0}</style>", unsafe_allow_html=True)
st.title("⚖️ LegalEase")
st.caption("AI-powered legal document drafting • Create, edit, and export a draft")
st.warning("LegalEase creates AI-generated drafts, not legal advice. Verify every clause and consult a qualified lawyer before signing or relying on a document.")

with st.form("document_form"):
    c1, c2 = st.columns(2)
    with c1:
        doc_type = st.selectbox("Document type", ["Employment Contract", "Non-Disclosure Agreement (NDA)", "Lease Agreement", "Freelance Work Contract", "Service Agreement", "Employment Offer Letter", "General Agreement", "Other"])
        if doc_type == "Other": doc_type = st.text_input("Specify document type", "")
        parties = st.text_area("Parties involved", placeholder="Name and role for each party", height=100)
        effective_date = st.date_input("Effective date", value=date.today()).isoformat()
    with c2:
        jurisdiction = st.text_input("Jurisdiction (optional)", placeholder="e.g., Tamil Nadu, India")
        terms = st.text_area("Terms & conditions", placeholder="Separate each term with a semicolon", height=160)
        extra = st.text_area("Additional instructions (optional)", height=75)
    submitted = st.form_submit_button("Generate Document", type="primary", use_container_width=True)

if submitted:
    if not doc_type.strip() or len(parties.strip()) < 2 or len(terms.strip()) < 3:
        st.error("Please provide a document type, parties, and at least one term.")
    else:
        payload = {"document_type": doc_type, "parties": parties, "terms": terms, "effective_date": effective_date, "jurisdiction": jurisdiction, "additional_instructions": extra}
        with st.spinner("Drafting your document…"):
            try:
                response = requests.post(f"{BACKEND_URL}/generate", json=payload, timeout=TIMEOUT)
                if response.ok:
                    st.session_state["legal_document"] = response.json()["document"]
                    st.session_state["doc_type"] = doc_type
                else:
                    try: detail = response.json().get("detail", response.text)
                    except Exception: detail = response.text
                    st.error(f"Backend error ({response.status_code}): {detail}")
            except requests.RequestException as exc:
                st.error(f"Could not connect to FastAPI at {BACKEND_URL}. Start the backend and try again. Details: {exc}")

if "legal_document" in st.session_state:
    st.subheader("Document preview & editor")
    st.caption("Edit the draft below before downloading. Generated content may contain errors or placeholders.")
    edited = st.text_area("Editable document", value=st.session_state["legal_document"], height=440, key="edited_document")
    st.session_state["legal_document"] = edited
    safe = sanitize_text(edited).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    with st.expander("Styled preview"):
        st.markdown(f"<div class='legal-card' style='white-space:pre-wrap'>{safe}</div>", unsafe_allow_html=True)
    base = (st.session_state.get("doc_type", "legal_document").lower().replace(" ", "_").replace("/", "_") or "legal_document")
    a,b,c = st.columns(3)
    with a: st.download_button("Download TXT", edited.encode("utf-8"), f"{base}.txt", "text/plain", use_container_width=True)
    with b: st.download_button("Download DOCX", format_docx(edited, st.session_state.get("doc_type", "Legal Document")), f"{base}.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", use_container_width=True)
    with c: st.download_button("Download PDF", format_pdf(edited, st.session_state.get("doc_type", "Legal Document")), f"{base}.pdf", "application/pdf", use_container_width=True)

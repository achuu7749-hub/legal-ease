from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str = Field(..., min_length=2, max_length=120)
    parties: str = Field(..., min_length=2, max_length=4000)
    terms: str = Field(..., min_length=3, max_length=12000)
    effective_date: str = Field(default="", max_length=100)
    jurisdiction: str = Field(default="Not specified", max_length=200)
    additional_instructions: str = Field(default="", max_length=4000)

class DocumentResponse(BaseModel):
    document: str
    model: str

@router.post("/generate", response_model=DocumentResponse)
def generate(request: DocumentRequest):
    generator = GeminiDocumentGenerator()
    try:
        result = generator.generate_document(**request.model_dump())
        return DocumentResponse(document=result, model=generator.model)
    except RuntimeError as exc:
        message = str(exc)
        status = 503 if "not configured" in message.lower() else 502
        raise HTTPException(status_code=status, detail=message) from exc

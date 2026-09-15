from pydantic import BaseModel, Field
from typing import List, Optional

class DocumentUpload(BaseModel):
    title: str = Field(..., description="Title of the coaching document or note")
    content: str = Field(..., description="The raw text content to be stored/indexed")

class QueryRequest(BaseModel):
    question: str = Field(..., description="The user's question for the AI coach")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="The AI's generated response")
    sources: List[str] = Field(..., description="Retrieved context sources used for the answer")
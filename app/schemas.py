from pydantic import BaseModel, EmailStr
from typing import Optional

class AgentSchema(BaseModel):
    name: str
    description: str
    llm: Optional[str] = None

class UpdateAgentSchema(BaseModel):
    description: Optional[str] = None
    llm: Optional[str] = None

class LLMRequest(BaseModel):
    prompt: str

class LLMRequestWithMemory(BaseModel):
    prompt: str
    conversation_id : Optional[str] = None

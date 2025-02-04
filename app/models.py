from typing import Optional
from pydantic import BaseModel

class AgentDB(BaseModel):
    id: str
    name: str
    description: str
    llm: Optional[str] = None
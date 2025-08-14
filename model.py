from pydantic import BaseModel
from typing import Optional

class ReportItem(BaseModel):
    title: str
    description: str
    category: Optional[str] = "Uncategorized"
    location: str
    status: str  # "Lost" or "Found"
    name: Optional[str] = "Anonymous"
    contact: str

from pydantic import BaseModel
from typing import Optional

class ReportItem(BaseModel):
    title: str
    description: Optional[str] = ""  # Make description optional with empty string default
    category: Optional[str] = "Uncategorized"
    location: str
    status: str  # "Lost" or "Found"
    name: Optional[str] = "Anonymous"
    contact: str

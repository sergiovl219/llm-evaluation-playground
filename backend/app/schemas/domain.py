from pydantic import BaseModel, Field
from typing import List, Optional

class SupportTicket(BaseModel):
    ticket_id: Optional[str] = Field(description="Unique identifier for the ticket, if present", default=None)
    customer_name: Optional[str] = Field(description="Name of the customer reporting the issue", default=None)
    issue_category: str = Field(description="Category of the issue: e.g. billing, technical, login, bug, feature_request, other")
    priority: str = Field(description="Priority level: low, medium, high, critical")
    summary: str = Field(description="A brief 1-sentence summary of the core issue")
    mentioned_products: List[str] = Field(description="List of products or features mentioned in the ticket", default_factory=list)

"""
AI audit event models.
"""


from dataclasses import dataclass
from datetime import datetime




@dataclass
class AuditRecord:
    """
    Represents one AI governance audit event.
    """


    user_id: str


    tenant_id: str


    model: str


    action: str


    result: str


    reason: str


    timestamp: datetime
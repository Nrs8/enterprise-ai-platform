"""
AI audit logging service.
"""


from datetime import datetime

from app.audit.models import AuditRecord



class AuditLogger:
    """
    Stores AI governance audit records.
    """



    def __init__(
        self,
    ) -> None:


        self._records: list[
            AuditRecord
        ] = []




    def record(
        self,
        user_id: str,
        tenant_id: str,
        model: str,
        action: str,
        result: str,
        reason: str,
    ) -> None:
        """
        Create audit record.
        """


        record = AuditRecord(

            user_id=user_id,

            tenant_id=tenant_id,

            model=model,

            action=action,

            result=result,

            reason=reason,

            timestamp=datetime.utcnow(),

        )


        self._records.append(
            record
        )




    def get_all(
        self,
    ) -> list[AuditRecord]:
        """
        Return all audit records.
        """


        return self._records.copy()
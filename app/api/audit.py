"""
Audit API endpoints.

Provides access to AI governance audit records.
"""


from fastapi import APIRouter, Request


router = APIRouter()



@router.get("/audit")
async def get_audit_records(
    http_request: Request,
):
    """
    Return all AI audit records.
    """


    container = (
        http_request
        .app
        .state
        .container
    )


    records = (
        container.audit_logger
        .get_all()
    )


    return [

        {

            "user_id": record.user_id,

            "tenant_id": record.tenant_id,

            "model": record.model,

            "action": record.action,

            "result": record.result,

            "reason": record.reason,

            "timestamp":
                record.timestamp.isoformat(),

        }

        for record in records

    ]
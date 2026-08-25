from app.mcp.audit import (
    MCPAuditEvent,
    MCPAuditLogger,
)


def test_audit_event_created():

    event = MCPAuditEvent(
        tenant_id="tenant-a",
        server_name="calculator",
        tool_name="add",
        success=True,
    )

    assert event.tenant_id == "tenant-a"
    assert event.success is True



def test_audit_logger_records_event():

    logger = MCPAuditLogger()

    event = MCPAuditEvent(
        tenant_id="tenant-a",
        server_name="calculator",
        tool_name="add",
        success=True,
    )

    logger.record(event)

    events = logger.list_events()

    assert len(events) == 1
    assert events[0].tool_name == "add"



def test_failed_event_contains_error():

    event = MCPAuditEvent(
        tenant_id="tenant-a",
        server_name="calculator",
        tool_name="divide",
        success=False,
        error="division failed",
    )

    assert event.success is False
    assert event.error == "division failed"



def test_audit_clear():

    logger = MCPAuditLogger()

    logger.record(
        MCPAuditEvent(
            tenant_id="tenant-a",
            server_name="calculator",
            tool_name="add",
            success=True,
        )
    )

    logger.clear()

    assert logger.list_events() == []
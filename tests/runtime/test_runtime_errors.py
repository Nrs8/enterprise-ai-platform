from app.runtime.errors import (
    build_error_info,
    ToolExecutionError,
    ErrorCategory,
)


def test_runtime_error_conversion():

    exc = ToolExecutionError(
        "calculator failed"
    )


    error = build_error_info(
        exc
    )


    assert error.code == (
        "tool_execution_failed"
    )


    assert error.category == (
        ErrorCategory.TOOL_FAILURE
    )


    assert error.message == (
        "calculator failed"
    )


    assert error.retryable is False
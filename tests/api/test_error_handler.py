"""
API error handler tests.
"""

from __future__ import annotations


import asyncio


from fastapi import (
    Request,
)


from app.api.error_handler import (
    runtime_exception_handler,
)


from app.runtime.errors import (
    LLMExecutionError,
)



def test_runtime_error_handler():

    exception = LLMExecutionError(
        "LLM provider failed",
        retryable=True,
    )


    response = asyncio.run(

        runtime_exception_handler(
            Request(
                {
                    "type": "http",
                    "method": "GET",
                    "path": "/test",
                    "headers": [],
                    "query_string": b"",
                    "server": (
                        "testserver",
                        80,
                    ),
                    "client": (
                        "testclient",
                        80,
                    ),
                    "scheme": "http",
                    "http_version": "1.1",
                }
            ),
            exception,
        )
    )


    assert response.status_code == 502


    assert response.body == (
        b'{"error":{"code":"llm_execution_failed",'
        b'"message":"LLM provider failed",'
        b'"category":"llm_failure",'
        b'"retryable":true}}'
    )
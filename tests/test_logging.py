
"""
Logging tests.
"""

import logging


logger = logging.getLogger(__name__)


def test_function(caplog):
    """
    Verify that the test function emits an informational log message.
    """

    with caplog.at_level(logging.INFO):
        result = 10 / 2
        logger.info("Calculation result: %s", result)

    assert result == 5
    assert "Calculation result: 5" in caplog.text

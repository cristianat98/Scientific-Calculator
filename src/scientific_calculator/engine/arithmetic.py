"""Basic arithmetic operations."""

import logging

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> float:
    """Return the sum of ``a`` and ``b``."""
    result = a + b
    logger.debug("add(%r, %r) = %r", a, b, result)
    return result

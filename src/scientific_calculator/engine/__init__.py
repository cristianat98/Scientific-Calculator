"""Calculation engine, free of UI dependencies.

Each maths domain (arithmetic, complex numbers, matrices, ...) lives in its own module or
subpackage, so a new domain is added without editing existing ones. Nothing here may import
the ``ui`` package or Qt.
"""

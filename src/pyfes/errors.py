"""Custom error classes for pyfes"""


class PyFesError(Exception):
    pass


class ValidationError(PyFesError):
    pass


class InvalidOperatorError(PyFesError):
    pass


class InvalidExpressionError(PyFesError):
    pass


class InvalidBoundaryTypeError(PyFesError):
    pass

"""
Validators for pyfes

These functions should raise a ValidationError when they do not
validate.
"""

from __future__ import absolute_import
import logging

from .errors import ValidationError


logger = logging.getLogger(__name__)


def gml_property_name_validator(value):
    """Validate a GML property name """
    # TODO
    pass

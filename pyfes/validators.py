"""Validators for pyfes expression types"""

from .errors import ValidationError


def validate_gml_property_name(item):
    """Check that the input conforms to GML naming rules for properties"""
    raise ValidationError
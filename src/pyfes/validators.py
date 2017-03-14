"""Validators for pyfes expression types"""

from .errors import ValidationError


def validate_gml_property_name(item):
    """Check that the input conforms to GML naming rules for properties"""
    raise ValidationError

def validate_wkt(item):
    """Check that the input is a valid WKT string."""
    # TODO - perform a stricter validation by checking coordinates
    wkt_types = [
        "GEOMETRY",
        "GEOMETRYCOLLECTION",
        "POINT",
        "MULTIPOINT",
        "LINESTRING",
        "MULTILINESTRING",
        "POLYGON",
        "MULTIPOLYGON",
        "TRIANGLE",
        "CIRCULARSTRING",
        "CURVE",
        "MULTICURVE",
        "COMPOUNDCURVE",
        "CURVEPOLYGON",
        "SURFACE",
        "MULTISURFACE",
        "POLYHEDRALSURFACE",
        "TIN",
    ]
    for type_ in wkt_types:
        if item.startswith(type_):
            break
    else:
        raise ValidationError

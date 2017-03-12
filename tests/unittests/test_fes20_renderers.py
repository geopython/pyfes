"""Unit tests for pyfes.fes20.renderers"""

from lxml import etree
import pytest

from pyfes.fes20 import expressions
from pyfes.fes20 import renderers
from pyfes.fes20.namespaces import NAMESPACES

pytestmark = pytest.mark.unit


def test_fes_filter_renderer_render_value_reference():
    renderer = renderers.FesFilterRenderer()
    result = renderer._render_value_reference(
        expressions.ValueReference("something")
    )
    expected = etree.fromstring(
        "<fes:ValueReference xmlns:fes={!r}>something"
        "</fes:ValueReference>".format(NAMESPACES["fes"])
    )
    assert etree.tostring(result) == etree.tostring(expected)

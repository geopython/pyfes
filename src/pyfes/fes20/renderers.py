from lxml import etree

from .namespaces import NAMESPACES


class FesFilterRenderer(object):

    def render(self, operator):
        raise NotImplementedError

    def _render_value_reference(self, value_reference):
        element = etree.Element(
            "{{{fes}}}ValueReference".format(**NAMESPACES),
            nsmap={"fes": NAMESPACES["fes"]}
        )
        element.text = value_reference.value
        return element

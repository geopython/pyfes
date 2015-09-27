"""base classes for pyfes"""

import logging

from lxml import etree

from .schemaparsers import schema_parser

logger = logging.getLogger(__name__)


class PyfesBase(object):

    @classmethod
    def from_xml(cls, xml_element, schema_path=None, validate_xml=True):
        """Return a new instance by parsing the input XML

        Child classes should not reimplement this method. They should
        reimplement `_from_xml` instead.

        :arg xml_element: The xml element to be parsed
        :type xml_element: etree.Element or str
        :arg schema_path: Full path to the xsd file to use when validating 
            the input xml
        :type schema_path: str
        :arg validate_xml: Turn on XML schema validation
        :type validate_xml: bool
        """

        if isinstance(xml_element, basestring):
            xml_element = etree.fromstring(xml_element)
        if validate_xml:
            if schema_path is not None:
                schema_parser.parse_schema(schema_path)
            try:
                schema_parser.validate_xml(xml_element)
            except etree.DocumentInvalid:
                raise
        return cls._from_xml(xml_element)

    @classmethod
    def from_ogc_common(cls, expression):
        """Return a new instance by parsing the input OGC_Common expression

        The default implementation does nothing so this method must be
        reimplemented in child classes.
        """
        raise NotImplementedError

    def to_xml(self, as_string=True):
        """Serialize to XML"""
        result = self._to_xml()
        if as_string:
            result = etree.tostring(result, pretty_print=True)
        return result

    @classmethod
    def _from_xml(cls, xml_element):
        """Reimplement this in child classes.

        :arg xml_element: the already validated XML
        :type xml_element: etree.Element
        """

        raise NotImplementedError

    def _to_xml(self):
        """Reimplement this method in child classes

        :returns: An xml Element
        :rtype: etree.Element
        """

        raise NotImplementedError

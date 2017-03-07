"""Base serializer classes for fesxml"""

from __future__ import absolute_import
import logging

from lxml import etree

logger = logging.getLogger(__name__)


class BaseSerializer(object):
    """Base class for all FES serializers."""

    TYPE_ = None  # the pyfes.types type that is being serialized

    @classmethod
    def deserialize(cls, xml_element, validate_schema=True):
        if isinstance(xml_element, basestring):
            xml_element = etree.fromstring(xml_element)
        # then validate the xml_element with the fes2_0 schema, if needed
        tag = etree.QName(xml_element).localname
        type_matches = tag == cls.TYPE_.__name__
        in_extra_type_names = tag in getattr(cls, "EXTRA_TYPE_NAMES", [])
        if not type_matches and not in_extra_type_names:
            raise Exception  # use a more specific exception
        return cls._deserialize(xml_element)

    @classmethod
    def _deserialize(cls, xml_element):
        raise NotImplementedError

    @classmethod
    def serialize(cls, fes_element, as_string=True, **kwargs):
        result = cls._serialize(fes_element, **kwargs)
        if as_string:
            result = etree.tostring(result, pretty_print=True)
        return result

    @classmethod
    def _serialize(cls, fes_element):
        raise NotImplementedError

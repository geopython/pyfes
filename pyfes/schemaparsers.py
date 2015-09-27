"""Schema parser for pyfes"""

import logging
import os

from lxml import etree

logger = logging.getLogger(__name__)


class SchemaParser(object):
    _schema = None

    @property
    def schema(self):
        return self._schema

    def __init__(self, schema_path=None):
        """
        Create a parser for XML data.

        This class is flexible in how it tries to find the XML schema
        document, if the input `schema_path` is provided, it is used.
        Alternatively, if `schema_path` is not provided the `PYFES_SCHEMA_PATH`
        environment variable is used, if available.

        :arg schema_path: The full path to the main fes schema file.
        :type schema_path: str
        """
        schema_path = schema_path or os.getenv("PYFES_SCHEMA_PATH")
        if schema_path is not None:
            self.parse_schema(schema_path)

    def parse_schema(self, schema_path):
        """Parse an xsd path"""
        try:
            self._schema = etree.XMLSchema(file=schema_path)
        except Exception:  # replace with more specific exception
            logger.warning("Could not parse {}".format(schema_path))
        return self._schema

    def validate_xml(self, element):
        """Validate an XML element"""
        if self._schema is not None:
            self._schema.assertValid(element)
        else:
            logger.warning("Cannot validate element. No schema parser "
                           "available.")


schema_parser = SchemaParser()
"""A singleton-like instance to perform schema parsing on exml elements"""

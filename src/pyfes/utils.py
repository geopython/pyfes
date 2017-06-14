"""Assorted utility functions for pyfes."""

from __future__ import absolute_import
import importlib
import logging

from lxml import etree

logger = logging.getLogger(__name__)

XML_PARSER = etree.XMLParser(resolve_entities=False)


def lazy_load(path, package="pyfes"):
    """Lazily load a module"""
    module_path, sep, class_name = path.rpartition(".")
    the_module = importlib.import_module(module_path, package=package)
    return getattr(the_module, class_name)


class ReadOnlyList(object):
    _data = []


    def __init__(self, arguments=None):
        self._data = list(arguments) if arguments is not None else []

    def __iter__(self):  # making objects iterable
        return iter(self._data)

    def __getitem__(self, item):  # implementing the sequence protocol
        return self._data[item]

    def __len__(self):  # implementing the sequence protocol
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

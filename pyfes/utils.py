"""
Assorted utility functions for pyfes.
"""

from __future__ import absolute_import
import importlib
import logging

logger = logging.getLogger(__name__)


def lazy_load(path, package="pyfes"):
    """Lazily load a module"""
    module_path, sep, class_name = path.rpartition(".")
    the_module = importlib.import_module(module_path, package=package)
    return getattr(the_module, class_name)

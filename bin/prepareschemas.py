"""
Prepare the XML Schemas used by pyfes in order to allow schema validation
"""

import os
import logging
import argparse

from lxml import etree

logging.getLogger(__name__)

OGC_SCHEMA


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--schemas-location",
        help="Absolute path to the root directory that has the "
             "OGC fes schemas"
    )
    parser.add_argument(
        "-f", "--fes-version", default="2.0",
        help="What version of the schemas should be prepared. "
             "Defaults to %(default)s"
    )
    return None


def _download_filter_schemas():
    """Download the official OGC FES schemas"""
    schema_dir = ""
    return schema_dir


def _get_main_schema_path(schema_dir, version):
    return {
        "2.0": os.path.join(schema_dir, version, "filterAll.xsd"),
    }.get(version)


def main(fes_version=None, schema_dir=None):
    if schema_dir is None:
        # download the schemas
        schema_dir = ""
        # lets try lxml's way first
        schema_url = ""
        schema_el = etree.parse()
    else:
        pass
    main_schema_path = _get_main_schema_path(schema_dir, fes_version)
    schema_el = etree.parse(main_schema_path)



if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(fes_version=args.fes_version, schema_dir=args.schemas_location)

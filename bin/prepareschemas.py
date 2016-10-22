"""
Prepare the XML Schemas used by pyfes in order to allow schema validation

fes requires the following schemas:

* http://www.w3.org/2001/xml.xsd
* http://schemas.opengis.net/ows/1.1.0/owsAll.xsd
"""

import os
import logging
import argparse

from lxml import etree

logging.getLogger(__name__)

OGC_SCHEMA_REPOSITORY_URL = "http://schemas.opengis.net"


def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "output_dir",
        help="Absolute path to the root directory where the "
             "OGC fes schemas are to be downloaded"
    )
    parser.add_argument(
        "-f", "--fes-versions", default="2.0", action="store_list",
        help="What version of the schemas should be downloaded. "
             "Defaults to %(default)s"
    )
    return None


def _download_schemas(fes_version, output_dir):
    """Download the official OGC FES schemas"""
    handler = {
        "2.0": _download_fes_2_0_schemas,
    }.get(fes_version)
    return handler(output_dir)

def _download_fes_2_0_schemas(output_dir):
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)
    raise NotImplementedError


def main(output_dir, fes_versions):
    for version in fes_versions:
        _download_schemas(version, output_dir)


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    main(fes_versions=args.fes_versions, schema_dir=args.output_dir)

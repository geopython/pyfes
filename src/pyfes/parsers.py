"""Parser helpers for pyfes"""

import logging

from .fes20 import filterparsers as fes20_filterparsers

logger = logging.getLogger(__name__)

FILTER_PARSER_CLASSES = [
    fes20_filterparsers.FesFilterParser,
    fes20_filterparsers.OgcCqlParser,
]


def parse_filter(data, **kwargs):
    """Parse FES filters

    Examples
    --------

    >>> data = '''
    ... <fes:Filter
    ...       xmlns:fes="http://www.opengis.net/fes/2.0"
    ...       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    ...       xsi:schemaLocation="http://www.opengis.net/fes/2.0
    ...         http://schemas.opengis.net/filter/2.0/filterAll.xsd"
    ... >
    ...         <fes:PropertyIsLessThan>
    ...             <fes:ValueReference>DEPTH</fes:ValueReference>
    ...             <fes:Literal>30</fes:Literal>
    ...       </fes:PropertyIsLessThan>
    ...     </fes:Filter>
    ... '''
    >>> filter_ = parse_filter(data=data)
    >>> filter_.operator_type.value
    'PropertyIsLessThan'

    """

    for cls in FILTER_PARSER_CLASSES:
        parser = cls(**kwargs)
        try:
            logger.debug("Trying to parse with parser {}...".format(parser))
            result = parser.parse(data)
            break
        except Exception:
            logger.debug("Parsing with parser {} failed".format(parser))
    else:
        logger.error("Could not parse data")
    return result

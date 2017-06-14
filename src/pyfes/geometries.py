from lxml import etree


def parse_gml(gml_element):
    """Parse a GML element into a WKT representation."""
    qname = etree.QName(gml_element)
    try:
        handler = {
            "Point": parse_gml_point,
            "LineString": parse_gml_linestring,
            "Polygon": parse_gml_polygon,
            "Box": parse_gml_box,
        }[qname]
    except KeyError:
        raise RuntimeError("Invalid GML geometry element: {!r}".format(qname))
    else:
        return handler(gml_element)


def parse_gml_point(gml_element):
    coordinates, srs = get_ordered_coordinates(gml_element)
    wkt = "POINT ({x} {y})".format(x=coordinates[0], y=coordinates[1])
    return wkt, srs


def parse_gml_linestring(gml_element):
    coordinates, srs = get_ordered_coordinates(gml_element)
    wkt = "LINESTRING ("
    for x_coord_index in range(0, len(coordinates), 2):
        x = coordinates[x_coord_index]
        y = coordinates[x_coord_index + 1]
        wkt += "{} {},".format(x, y)
    wkt = wkt[:-1] + ")"
    return wkt


def parse_gml_polygon(gml_element):
    raise NotImplementedError


def parse_gml_box(gml_element):
    coordinates, srs = _get_gml_coordinates(gml_element)
    wkt = "POLYGON (("
    for x_coord_index in range(0, len(coordinates), 2):
        x = coordinates[x_coord_index]
        y = coordinates[x_coord_index + 1]
        wkt += "{} {},".format(x, y)
    wkt += "{first_x} {first_y}))".format(
        first_x=coordinates[0],
        first_y=coordinates[1]
    )
    return wkt


def get_ordered_coordinates(gml_element):
    coordinates, srs = _get_gml_coordinates(gml_element)
    ordered_coordinates = _order_coordinates(srs, coordinates)
    return ordered_coordinates, srs


def _get_axes_order(srs):
    order = {
        "http://www.opengis.net/def/crs/EPSG/0/4326": "yx",
    }
    return order.get(srs, "yx")


def _get_gml_coordinates(gml_element):
    namespaces = {
        "gml32": "http://www.opengis.net/gml/3.2",
        "gml2": "http://www.opengis.net/gml",
    }
    srs = gml_element.get(
        "srsName", "http://www.opengis.net/def/crs/EPSG/0/4326")
    try:
        coordinates = gml_element.xpath(
            "gml32:pos/text()", namespaces=namespaces)[0]
    except IndexError:
        try:
            coordinates = gml_element.xpath(
                "gml2:coordinates/text()", namespaces=namespaces)[0]
            coordinates = coordinates.replace(",", " ")
        except IndexError:
            raise RuntimeError("Invalid GML element")
    return coordinates.split(), srs


def _order_coordinates(srs, coordinates):
    if _get_axes_order(srs) == "yx":
        ordered = list(reversed(coordinates))
    else:
        ordered = list(coordinates)
    return ordered

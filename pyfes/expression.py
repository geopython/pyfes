"""Expression types for pyfes"""

import logging

logger = logging.getLogger(__name__)


class FesString:
    _counter = 0

    def __init__(self):
        self.storage_name = (
            "_{0.__class__.__name__}#{0.__class__._counter}".format(self))
        self.__class__._counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)

    def _validate_gml_property_name(self, value):


class Expression(object):
    pass


# Add some form of validation (perhaps by implementing a descriptor) for:
# - GML property names,
# - XPath expressions
# - The FES XPath subset
class ValueReference(Expression):
    value = FesString()

    def __init__(self, value):
        self.value = str(value)

    def __repr__(self):
        return ("{0.__class__.__name__}(value={0.value!r})".format(self))

    def __str__(self):
        return self.value


# - It would be cool to provide automatic conversion to common types, like
#   datetime.datetime for dates. A descriptors seems like a good fit for this
#   too.
class Literal(Expression):
    """FES Literal type.

    According to FES v2.0.0, a literal value is any part of a statement or
    expression which should be used as provided

    Examples
    --------
    >>> weight = Literal(30.0)
    >>> date_creation = Literal("1963-10-13", "xs:date")

    """

    value = None
    type_ = ""

    def __init__(self, value, type_=""):
        self.value = value
        self.type_ = str(type_)

    def __repr__(self):
        return (
            "{0.__class__.__name__}(value={0.value!r}, "
            "type={0.type_!r})".format(self)
        )

    def __str__(self):
        return str(self.value)


class Function(Expression):
    """FES Function type.

    According to FES v2.0.0, a function is a named procedure that performs a
    distinct computation. A function can accept zero or more arguments as
    input and generates a single result.

    Examples
    --------

    """

    expressions = []

    def __init__(self, expressions=None):
        for expression in expressions or []:
            if isinstance(expression, Expression):
                self.expressions.append(expression)
            else:
                raise RuntimeError(
                    "Expression {0!r} must be a pyfes.expressionExpression "
                    "subtype".format(expression))

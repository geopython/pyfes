"""Expression types for FES version 2.0"""

from itertools import product

from ..utils import ReadOnlyList


class Expression(object):
    """Base class for FES v2.0 expression types"""

    def __init__(self, validators=None):
        self.validators = list(validators) if validators is not None else []


class Literal(Expression):
    """FES Literal type.

    According to FES v2.0.0, a literal value is any part of a statement or
    expression which should be used as provided

    Examples
    --------
    >>> weight = Literal(30.0)

    """

    _value = None
    _type = None

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        for validator in self.validators:
                validator(new_value)
        self._value = new_value
        self._type = type(new_value)

    @property
    def type_(self):
        return self._type

    def __init__(self, value, validators=None):
        super(Literal, self).__init__(validators=validators)
        self.value = value

    def __str__(self):
        return "{0.__class__.__name__} <{0.value}, {0.type_}>".format(self)

    def __repr__(self):
        return ("{0.__class__.__name__}(value={0.value!r}, type_={0.type_!r}, "
                "validators={0.validators!r})".format(self))


class ValueReference(Expression):
    _value = ""

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        value_str = str(new_value)
        for validator in self.validators:
            validator(value_str)
        self._value = value_str

    def __init__(self, value, validators=None):
        super(ValueReference, self).__init__(validators=validators)
        self.value = value


class Function(Expression):
    """FES Function type.

    According to FES v2.0.0, a function is a named procedure that performs a
    distinct computation. A function can accept zero or more arguments as
    input and generates a single result.

    Examples
    --------

    >>> f1 = Function("make_cofee", arguments=[Literal("with_sugar")])

    """

    _name = ""
    _arguments = ReadOnlyList()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        for validator in self.validators:
            validator(new_name)
        self._name = new_name

    @property
    def arguments(self):
        return self._arguments

    @arguments.setter
    def arguments(self, new_arguments):
        self._arguments = ReadOnlyList()
        for argument, validator in product(new_arguments, self.validators):
            self.add_argument(argument)

    def __init__(self, name, arguments=None, validators=None):
        super(Function, self).__init__(validators=validators)
        self.name = name
        self.arguments = list(arguments) if arguments is not None else []

    def add_argument(self, argument):
        if not isinstance(argument, Expression):
            raise errors.InvalidBoundaryTypeError
        self._arguments._data.append(argument)

    def remove_argument(self, argument):
        self._arguments._data.remove(argument)

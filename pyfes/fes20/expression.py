import datetime as dt
from itertools import product

from shapely import geometry


class Expression(object):

    def __init__(self, validators=None):
        self.validators = validators or []


class Literal(Expression):
    _value = None

    recognized_types = {
        int: "xs:integer",
        float: "xs:float",
        str: "xs:string",
        dt.datetime: "xs:DateTime",
        dt.date: "xs:Date",
        dt.time: "xs:Time",
        geometry.Point: "gml:Point",
    }

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        for validator in self.validators:
                validator(new_value)
        self._value = new_value
        self.type_ = self._guess_type(new_value) or self.type_

    def __init__(self, value, type_=None, validators=None):
        super(Literal, self).__init__(validators=validators)
        self.value = value
        self.type_ = type_ if type_ is not None else self.type_

    def _guess_type(self, value):
        for recognized_type, xsd_type in self.recognized_types.items():
            if isinstance(value, recognized_type):
                type_ = xsd_type
                break
        else:
            type_ = None
        return type_


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


class Function(Expression):
    _name = ""
    _arguments = []

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
        for argument, validator in product(new_arguments, self.validators):
            validator(argument)
        self._arguments = new_arguments

    def __init__(self, name, *args, validators=None):
        super(Function, self).__init__(validators=validators)
        self.name = name
        self.arguments = args

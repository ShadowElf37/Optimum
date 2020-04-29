"""
All datatypes must define build().
"""
import ctypes
from abc import ABC, abstractmethod
class Type(ABC):
    NAMED = False
    @abstractmethod
    def build(self, resolver): pass

class String(Type):
    def __init__(self, value):
        self.value = value.strip('"')
    def build(self, resolver):
        return '"'+self.value+'"'

class Int(Type):
    def __init__(self, value):
        self.value = int(value)
    def build(self, resolver):
        return self.value
class Float(Type):
    def __init__(self, value):
        self.value = float(value)
    def build(self, resolver):
        return self.value

class List(Type):
    def __init__(self, value):
        self.value = value.split(',')
    def build(self, resolver):
        built = []
        for obj in self.value:
            built.append(resolver(obj))
        return '['+','.join(built)+']'
class TupleAndParentheses(Type):
    def __init__(self, value):
        self.value = value.split(',')
    def build(self, resolver):
        built = []
        for obj in self.value:
            built.append(resolver(obj))
        return '('+','.join(built)+')'

class Bool(Type):
    def __init__(self, value):
        self.value = value
    def build(self, resolver):
        return self.value.title()

class Null(Type):
    def __init__(self):
        pass
    def build(self, resolver):
        return 'None'

class Undefined(Type):
    UNDEFINED = object()
    def __init__(self):
        pass
    def build(self, resolver):
        return 'UNDEFINED'


class Name(Type):
    def __init__(self, name):
        self.name = name
    def build(self, resolver):
        return self.name

class InstanceName(Name):
    def build(self, resolver):
        return 'self.'+self.name

class NonlocalName(Name):
    def build(self, resolver):
        return 'global.'+self.name
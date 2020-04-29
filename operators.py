from abc import ABC, abstractmethod
class Operator(ABC):
    NAMED = False
    def __init__(self, left, right):
        self.left = left
        self.right = right
    @abstractmethod
    def build(self, resolver): pass

class Add(Operator):
    def build(self, resolver):
        return resolver(self.left) + '+' + resolver(self.right)
class Subtract(Operator):
    def build(self, resolver):
        return resolver(self.left) + '-' + resolver(self.right)
class Multiply(Operator):
    def build(self, resolver):
        return resolver(self.left) + '*' + resolver(self.right)
class Divide(Operator):
    def build(self, resolver):
        return resolver(self.left) + '/' + resolver(self.right)
class Modulo(Operator):
    def build(self, resolver):
        return resolver(self.left) + '%' + resolver(self.right)

class Ternary:
    NAMED = False
    def __init__(self, condition, yes, no):
        self.condition = condition
        self.yes = yes
        self.no = no
    def build(self, resolver):
        return '(' + resolver(self.yes) + ' if ' + resolver(self.condition) + ' else ' + resolver(self.no) + ')'

class TernaryOptional(Ternary):
    def __init__(self, condition, yes):
        super().__init__(condition, yes, 'undefined')
class TernaryForced(Ternary):
    def __init__(self, condition, yes):
        super().__init__(condition, yes, '0')

class Kwarg(Operator):
    def build(self, resolver):
        return self.left + '=' + resolver(self.right)
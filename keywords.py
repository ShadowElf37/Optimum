from datatypes import Type, Undefined
from errors import CompilerError
import codeobjects

UNDEFINED = Undefined.UNDEFINED

class Let(Type):
    NAMED = True
    def __init__(self, name, value):
        self.name = name.strip()
        self.value = value.strip()
        if self.name in Constant.NAMES:
            raise CompilerError('Can\'t set {0}, {0} is {1}'.format(self.name, Constant.NAMES[self.name]))
    def build(self, resolver):
        return resolver(self.name) + '=' + resolver(self.value)

class LetOptional(Let):
    def __init__(self, name):
        super().__init__(name.strip(), 'undefined')
class LetForced(Let):
    def __init__(self, name):
        super().__init__(name.strip(), '0')

class LetCodeObject(Let):
    pass


class Constant(Type):
    NAMED = True
    NAMES = {}
    def __init__(self, name, value):
        self.name = name.strip()
        self.value = value.strip()
        if self.name in self.NAMES:
            raise CompilerError('Can\'t set {0}, {0} is {1}'.format(self.name, Constant.NAMES[self.name]))
        self.NAMES[self.name] = self.value
    def build(self, resolver):
        return resolver(self.name) + '=' + resolver(self.value)

class Temp(Type):
    def __init__(self, name, value, after=''):
        self.name = name.strip()
        self.value = value.strip()
        self.after = after.strip()
    def build(self, resolver):
        after = resolver(self.after)
        if after: after += '()'
        return self.name + '=' + resolver(self.value) + '\n' + after + '\n' + 'del ' + self.name


class With(Type):
    def __init__(self, temp, code):
        self.temp = temp
        self.code = code
    def build(self, resolver):
        return resolver(self.temp, after=self.code)

class For(Type):
    def __init__(self, x, iterable, code):
        self.x = x
        self.iterable = iterable
        self.code = code
    def build(self, resolver):
        print(self.x, self.iterable, self.code)
        return 'for {} in {}:\n\t{}'.format(resolver(self.x), resolver(self.iterable), resolver(self.code.strip('{').strip('}')))

class Import(Type):
    def __init__(self, path):...

class Return(Type):
    def __init__(self, value):
        self.value = value
    def build(self, resolver):
        print(self.value)
        return 'return ' + resolver(self.value)
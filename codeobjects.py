from abc import ABC, abstractmethod
import re

class CodeObject(ABC):
    NAMED = False
    @abstractmethod
    def build(self, resolver, compiler, objectdict): pass


class Call:
    NAMED = False
    def __init__(self, f, args):
        self.f = f
        self.args = args
    def build(self, resolver):
        args = resolver(self.args)
        if len(args) == 0 or args[0] != '(':
            return self.f + '(' + args + ')'
        return self.f + args

class Class(CodeObject):
    def __init__(self, code, args=''):
        self.code = code
        self.args = ''
        print('@', self.code)
        if args and args.strip()[:5] == 'from ':
            self.args = args.strip()[5:].strip(':').strip(';')
    def build(self, resolver, compiler, objectdict):
        # Create class template up top
        name = '__Optimum_Object_{}'.format(len(objectdict))
        # Reserve a space in the object dictionary
        objectdict[name] = None

        # Generate compiled class
        cls = ('class {}:\n\tdef __new__(cls,'+self.args+'):\n\t\t{new}\n\t').format(name, new='{new}')
        # Compile internals
        print(self.code)
        cls += '\n\t'.join(compiler(self.code.replace('::', ';')).split('\n'))

        # Move instance variables to __new__()
        new_override = ['self = super().__new__(cls)']
        returned = False
        for line in cls.split('\n'):
            if 'self' in line or 'return ' in line:
                new_override.append(line.strip()) #.replace('self', 'cls')
                cls = cls.replace(line, '')
                if 'return ' in line:
                    returned = True

            elif 'global' in line:
                s = re.search('global\.(\w*)', line)
                n = s.groups()[0]
                cls = cls.replace(line, '\n\t' + 'nonlocal ' + n + '\n' + line.replace('global.', ''))

        # Because the return value of __new__() can be overridden, calling the class can effectively work like a function call, removing the need for a separate function data type
        if not returned:
            new_override.append('return self')
        cls = cls.format(new='\n\t\t'.join(new_override))

        objectdict[name] = cls
        return name
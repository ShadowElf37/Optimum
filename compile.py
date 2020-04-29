import datatypes
import keywords
import operators
import errors
import codeobjects
import re
from parse import StatefulMatcher

UNDEFINED = datatypes.Undefined.UNDEFINED

COMMENTS_ONELINE = re.compile('(//.*)')
COMMENTS_MULTILINE = re.compile('((?:/\*).*(?:\*/))')

CONSTRUCTORS_DICT = {
    # Data types
    re.compile('^(?<!\\\\)["\']([^"]*)(?<!\\\\)["\'];?$'): datatypes.String,
    re.compile('^(?!\.)([0-9]*);?$'): datatypes.Int,
    re.compile('^([0-9]+\.[0-9]*);?$'): datatypes.Float,
    re.compile('^\[(.*)\];?$'): datatypes.List,
    re.compile('^\((.*)\);?$'): datatypes.TupleAndParentheses,
    re.compile('^(true|false);?$'): datatypes.Bool,

    re.compile('^null;?$'): datatypes.Null,
    re.compile('^undefined;?$'): datatypes.Undefined,

    # Keywords
    re.compile('^let\s+([a-zA-Z_.]\w*)\s*=\s*(.+);?$'): keywords.Let,
    re.compile('^let\s+([a-zA-Z_.]\w*)\s*!;?$'): keywords.LetForced,
    re.compile('^let\s+([a-zA-Z_.]\w*);?$'): keywords.LetOptional,
    re.compile('^let\s+([a-zA-Z_.]\w*)\s*(.*);?$'): keywords.Let,
    re.compile('^([a-zA-Z_.]\w*)\s+is\s*(.+);?$'): keywords.Constant,
    re.compile('^([a-zA-Z_.]\w*)\s+of\s*(.+);?$'): keywords.Temp,
    re.compile('^return\s*(.*)$'): keywords.Return,
    re.compile('^with\s*((?:[a-zA-Z_.]\w*)\s+of\s*(?:[^\s{]+))\s*(.*)'): keywords.With,
    re.compile('^for\s+([a-zA-Z_.]\w*)\s+in\s*(.*)\s+(.*)'): keywords.For,

    # Operators
    re.compile('^(.+)\+(.*);?$'): operators.Add,
    re.compile('^(.+)-(.*);?$'): operators.Subtract,
    re.compile('^(.+)\*(.*);?$'): operators.Multiply,
    re.compile('^(.+)/(.*);?$'): operators.Divide,
    re.compile('^(.+)%(.*);?$'): operators.Modulo,
    re.compile('^([a-zA-Z_.]\w*)=(.*);?$'): operators.Kwarg,
    re.compile('^(.+)\s*\?\s*(.+)\s*:\s*(.+);?$'): operators.Ternary,
    re.compile('^(.+)\s*\?\s*(.+)\s*!;?$'): operators.TernaryForced,
    re.compile('^(.+)\s*\?\s*(.+);?$'): operators.TernaryOptional,

    # Names
    re.compile('^([a-zA-Z_][\w.]*);?$'): datatypes.Name,
    re.compile('^\.?([a-zA-Z_][\w.]*);?$'): datatypes.InstanceName,
    re.compile('^\$\.?([a-zA-Z_][\w.]*);?$'): datatypes.NonlocalName,

    # Code objects
    StatefulMatcher('{', '}'): codeobjects.Class,
    re.compile('^(\w*)\s*\((.*)\);?$'): codeobjects.Call,
}

CONSTRUCTORS = CONSTRUCTORS_DICT.items()

OBJECTS = {}
CODEOBJECTS = {}

scope = None
def resolve(chunk, *args, **kwargs):
    if chunk.strip() == '':
        return ''
    for keyword, constructor in CONSTRUCTORS:
        m = keyword.match(chunk.strip())
        if m:
            obj = constructor(*m.groups(), *args, **kwargs)
            if obj.NAMED:
                OBJECTS[obj.name] = obj
            if isinstance(obj, codeobjects.CodeObject):
                return str(obj.build(resolve, compile, CODEOBJECTS))
            return str(obj.build(resolve))

    # return chunk.strip()  # Variable name etc.
    raise errors.CompilerError('Cannot resolve "%s"' % chunk.strip())

def compile(block, scope_=scope, with_objects=False):
    global scope
    scope = scope_
    compiled = []

    for comment in COMMENTS_ONELINE.findall(block):
        block = block.replace(comment, '')

    block = block.replace('\n', ' ').replace('\t', ' ')

    for comment in COMMENTS_MULTILINE.findall(block):
        block = block.replace(comment, '')

    for line in StatefulMatcher('{','}').match(block).groups(False):
        block = block.replace(line, line.replace(';', '::'))

    block = re.split(';', block)
    for lineno, statement in enumerate(block):
        try:
            compiled.append(resolve(statement).strip())
        except errors.CompilerError as e:
            raise e.again('(line %s)' % (lineno+1)) from None

    if with_objects:
        return '\n'.join(CODEOBJECTS.values()) + '\n# PROGRAM' + '-'*50 + '\n' + '\n'.join(compiled)
    return '\n'.join(compiled)


if __name__ == "__main__":
    exec(compile(open('test.o').read(), with_objects=True))
from sys import argv
from compile import compile

result = compile(open(argv).read())

file = None

if len(argv) > 2:
    open(argv[-1], 'w+').write(result)
else:
    print(result)
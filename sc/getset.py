"""

Contract History
- v1: 0x2248b952de35e6b8b297e043e1e82546fdf50c84
- v2:

Testing:
- build sc/getset.py test 0710 07 True False False set ["abcd", "123somevalue"]
- build sc/getset.py test 0710 07 True False False get ["abcd"]


Importing:
- build sc/getset.py
- import contract sc/getset.avm 0710 07 True False False


Testinvoke:

- testinvoke 0x2248b952de35e6b8b297e043e1e82546fdf50c84 set ["abcd", "testresult"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
- testinvoke 0x2248b952de35e6b8b297e043e1e82546fdf50c84 get ["abcd"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y

"""
from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.Neo.Storage import Get, Put, GetContext
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness
from boa.builtins import concat


def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No arguments supplied")
        return 0

    elif operation == 'set':
        key = args[0]
        value = args[1]

        context = GetContext()
        Put(context, key, value)
        return key

    elif operation == 'get':
        key = args[0]
        context = GetContext()
        result = Get(context, key)
        return result

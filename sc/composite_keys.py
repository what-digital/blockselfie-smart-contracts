"""

Contract History
- v0.2: 0xf798badaa47c3d7df8b6a927208ec71608dcc884
- v0.3: 0xe22f21368fa8ae7808a658784eedb4f5d88fa83d
- v0.5: 0xe22f21368fa8ae7808a658784eedb4f5d88fa83d
- v0.9: 0xe904b30a3d576ab66ed712559357f97e12a7eba1
- v010: 0x4e24294d8a3fb9d3b5636003396e4ad42f5a3ef4

Testing:
- build sc/composite_keys.py test 0710 05 True False False set_key_by_composites ["ab", "cd", "123somevalue"]
- build sc/composite_keys.py test 0710 05 True False False get_key_by_composites ["ab", "cd"]
- build sc/composite_keys.py test 0710 05 True False False get_key ["abcd"]
- build sc/composite_keys.py test 0710 05 True False False set_key ["abcd", "testresult2"]

Importing:
- build sc/composite_keys.py
- import contract sc/composite_keys.avm 0710 05 True False False


Testinvoke:

- testinvoke 0x4e24294d8a3fb9d3b5636003396e4ad42f5a3ef4 set_key_by_composites ["ab", "cde", "testresult"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
- testinvoke 0x4e24294d8a3fb9d3b5636003396e4ad42f5a3ef4 set_key ["abcde", "testresult4"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
- testinvoke 0x4e24294d8a3fb9d3b5636003396e4ad42f5a3ef4 get_key_by_composites ["ab", "cde"]
- testinvoke 0x4e24294d8a3fb9d3b5636003396e4ad42f5a3ef4 get_key ["abcde"]

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

    if operation == 'set_key_by_composites':
        part1 = args[0]
        part2 = args[1]
        value = args[2]

        Notify(part1)
        Notify(part2)
        Notify(value)

        key = concat(part1, part2)
        context = GetContext()
        Put(context, key, value)
        return key

    elif operation == 'get_key_by_composites':
        part1 = args[0]
        part2 = args[1]

        Notify(part1)
        Notify(part2)

        key = concat(part1, part2)
        context = GetContext()
        result = Get(context, key)
        return result

    elif operation == 'set_key':
        key = args[0]
        value = args[1]

        context = GetContext()
        Put(context, key, value)
        return key

    elif operation == 'get_key':
        key = args[0]
        context = GetContext()
        result = Get(context, key)
        return result

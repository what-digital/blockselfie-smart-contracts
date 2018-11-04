"""
Testing:
- build sc/composite_keys.py test 0710 05 True False False set_composite_key ["ab", "cd", "123somevalue"]
- build sc/composite_keys.py test 0710 05 True False False get_composite_key ["ab", "cd"]

Importing:
- build sc/composite_keys.py
- import contract sc/composite_keys.avm 0710 05 True False False


Testinvoke:

- testinvoke 0xce0fb320187933b8fa5ef91b2b64ad6bb827ace0 set_composite_key ["ab", "cd"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y


"""
from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.Neo.Storage import Get, Put, GetContext
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness
from boa.builtins import concat


def Main(operation, args):
    nargs = len(args)
    if nargs == 0:
        print("No domain name supplied")
        return 0

    if operation == 'set_composite_key':
        part1 = args[0]
        part2 = args[1]
        value = args[2]
        key = _build__composite_key(part1, part2)
        context = GetContext()
        Put(context, key, value)
        return key

    if operation == 'get_composite_key':
        part1 = args[0]
        part2 = args[1]

        key = _build__composite_key(part1, part2)
        context = GetContext()
        result = Get(context, key)
        return result


def _build__composite_key(addr1, addr2):
    text = concat(addr1, '_')
    key = concat(text, addr2)
    return key

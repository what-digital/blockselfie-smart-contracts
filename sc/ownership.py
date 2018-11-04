"""
Testing:
- build sc/ownership.py test 0710 05 True False False set_composite_key ["ab", "cd", "123somevalue"]
- build sc/ownership.py test 0710 05 True False False get_composite_key ["ab", "cd"]

Importing:
- build sc/ownership.py
- import contract sc/ownership.avm 0710 05 True False False


Testinvoke:

- testinvoke 0xce0fb320187933b8fa5ef91b2b64ad6bb827ace0 set_composite_key ["ab", "cd", "123somevalue"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y


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

    if operation == 'set_owner':
        owner = args[0]
        context = GetContext()
        Put(context, 'owner', owner)

    elif operation == 'get_owner':
        context = GetContext()
        owner = Get(context, 'owner')
        return owner

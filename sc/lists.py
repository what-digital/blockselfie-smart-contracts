"""

Contract History
-

Testing:
- build sc/lists.py test 0710 05 True False False


Importing:
- build sc/lists.py
- import contract sc/lists.avm 0710 05 True False False


Testinvoke:




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




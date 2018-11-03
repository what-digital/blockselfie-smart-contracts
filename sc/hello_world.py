"""
In prompt.py, you need to execute `config sc-events on` to see the events showing up.
Test & Build:
neo> build 2-print-and-notify.py test 07 05 True False
"""

from boa.interop.Neo.Runtime import Log, Notify


def Main():
    # Print translates to a `Log` call, and is best used with simple strings for
    # development info. To print variables such as lists and objects, use `Notify`.
    print("Hello world via print()")
    Log("Hello World via Log")
    Notify("Hello World via Notify")

    # Sending multiple arguments as notify payload:
    msg = ["Hello", "World", "as", "Array"]
    Notify(msg)

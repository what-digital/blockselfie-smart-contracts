#!/usr/bin/env python3

from neorpc.Client import RPCClient, RPCEndpoint
from neorpc.Settings import SettingsHolder
from binascii import hexlify, unhexlify

settings = SettingsHolder()
settings.setup_privnet()

client = RPCClient(config=settings)
scripthash = "ce0fb320187933b8fa5ef91b2b64ad6bb827ace0"
endpoint = "http://neo-privnet.what.digital:30333"
part1 = hexlify(b'ab').decode()
part2 = hexlify(b'cd').decode()

try:
    result = client.invoke_contract_fn(scripthash,'get_composite_key',params=[{"type":5,"value":part1}, {"type":5,"value":part2}], endpoint=RPCEndpoint(client=None, address=endpoint))
    if result:
        print(result)

except Exception as e:
    print("Error: {}".format(e))
    print('')

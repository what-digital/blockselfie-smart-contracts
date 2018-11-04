import binascii
import hashlib
from neo.Implementations.Wallets.peewee.UserWallet import UserWallet
from neo.Core.TX.Transaction import ContractTransaction, TransactionOutput
from neo.Core.TX.InvocationTransaction import InvocationTransaction
from neo.Core.TX.TransactionAttribute import TransactionAttribute, TransactionAttributeUsage
from neo.Core.CoinReference import CoinReference
from neo.SmartContract.ContractParameterContext import ContractParametersContext
from neocore.Fixed8 import Fixed8
from neocore.UInt256 import UInt256
from neocore.UInt160 import UInt160
from neocore.KeyPair import KeyPair
from neo import Blockchain
from base58 import b58decode
from neo.VM.ScriptBuilder import ScriptBuilder
from neo.Wallets.utils import to_aes_key

"""
    Example 1
    Sending NEO or GAS happens via a ContractTransaction
    For more information regarding different transaction types read point 3 of:
    http://docs.neo.org/en-us/network/network-protocol.html#data-type
    The standard ``Transaction`` looks as follows (taken from the above source)
    +------+------------+-----------+--------------------------------------------------+
    | Size |   Field    | DataType  |                   Description                    |
    +------+------------+-----------+--------------------------------------------------+
    | 1    | Type       | uint8     | Type of transaction                              |
    | 1    | Version    | uint8     | Trading version, currently 0                     |
    | ?    | -          | -         | Data specific to transaction types               |
    | ?*?  | Attributes | tx_attr[] | Additional features that the transaction has     |
    | 34*? | Inputs     | tx_in[]   | Input                                            |
    | 60*? | Outputs    | tx_out[]  | Output                                           |
    | ?*?  | Scripts    | script[]  | List of scripts used to validate the transaction |
    +------+------------+-----------+--------------------------------------------------+
"""


def create_raw_sc_method_call_tx(
        source_address,
        source_address_wif,
        smartcontract_scripthash,
        smartcontract_method,
        smartcontract_method_args,
):
    source_script_hash = address_to_scripthash(source_address)

    # start by creating a base InvocationTransaction
    # the inputs, outputs and Type do not have to be set anymore.
    invocation_tx = InvocationTransaction()

    # often times smart contract developers use the function ``CheckWitness`` to determine if the transaction is signed by somebody eligible of calling a certain method
    # in order to pass that check you want to add the corresponding script_hash as a transaction attribute (this is generally the script_hash of the public key you use for signing)
    # Note that for public functions like the NEP-5 'getBalance' and alike this would not be needed, but it doesn't hurt either
    invocation_tx.Attributes.append(
        TransactionAttribute(usage=TransactionAttributeUsage.Script, data=source_script_hash))

    smartcontract_scripthash = UInt160.ParseString(smartcontract_scripthash)
    # next we need to build a 'script' that gets executed against the smart contract.
    # this is basically the script that calls the entry point of the contract with the necessary parameters
    sb = ScriptBuilder()

    # call the method on the contract (assumes contract address is a NEP-5 token)
    sb.EmitAppCallWithOperationAndArgs(
        smartcontract_scripthash,
        smartcontract_method,
        smartcontract_method_args,
    )
    invocation_tx.Script = binascii.unhexlify(sb.ToArray())

    # at this point we've build our unsigned transaction and it's time to sign it before we get the raw output that we can send to the network via RPC
    # we need to create a Wallet instance for helping us with signing
    wallet = UserWallet.Create('path', to_aes_key('mypassword'), generate_default_key=False)

    # if you have a WIF use the following
    # this WIF comes from the `neo-test1-w.wallet` fixture wallet
    private_key = KeyPair.PrivateKeyFromWIF(source_address_wif)

    # if you have a NEP2 encrypted key use the following instead
    # private_key = KeyPair.PrivateKeyFromNEP2("NEP2 key string", "password string")

    # we add the key to our wallet
    wallet.CreateKey(private_key)

    # and now we're ready to sign
    context = ContractParametersContext(invocation_tx)
    wallet.Sign(context)

    invocation_tx.scripts = context.GetScripts()
    raw_tx = invocation_tx.ToArray()

    print(raw_tx)

    return raw_tx.decode()


def address_to_scripthash(address: str) -> UInt160:
    """Just a helper method"""
    AddressVersion = 23  # fixed at this point
    data = b58decode(address)
    if len(data) != 25:
        raise ValueError('Not correct Address, wrong length.')
    if data[0] != AddressVersion:
        raise ValueError('Not correct Coin Version')

    checksum_data = data[:21]
    checksum = hashlib.sha256(hashlib.sha256(checksum_data).digest()).digest()[:4]
    if checksum != data[21:]:
        raise Exception('Address format error')
    return UInt160(data=data[1:21])


def read_contract_method(
        smartcontract_scripthash,
        smartcontract_method,
        smartcontract_params,
):
    """
    :param smartcontract_scripthash:
    :param smartcontract_method:
    :param smartcontract_params: [{"type":5,"value":part1}, {"type":5,"value":part2}]
    :return:
    """
    try:
        result = client.invoke_contract_fn(
            smartcontract_scripthash,
            smartcontract_method,
            params=smartcontract_params,
            endpoint=RPCEndpoint(client=None, address=endpoint),
        )

        if result and result.get('error'):
            print(result.get('error').get('message'))
            return result.get('error').get('message')

        if result and result.get('stack', [{}])[0].get('value'):
            hex_value = result.get('stack')[0].get('value')
            string_value = bytes.fromhex(hex_value).decode('utf-8')
            print(string_value)
            return string_value
        print("No value!")

    except Exception as e:
        print("Error: {}".format(e))


from neorpc.Client import RPCClient, RPCEndpoint
from neorpc.Settings import SettingsHolder
from binascii import hexlify, unhexlify

settings = SettingsHolder()
settings.setup_privnet()

client = RPCClient(config=settings)
endpoint = "http://neo-privnet.what.digital:30333"






WALLETS = {

    "main_wallet": {
        'address': "AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y",
        'wif': "KxDgvEKzgSBPPfuVfw67oPQBSjidEiqTHURKSDL1R7yGaGYAeYnr",
    },
    "wallet_chris": {
        'address': "ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc",
        'wif': "L3QGJ5FMg7LQWYkVekkwRDyYL3HXTw3ntYrTupjp3EViru7kTGN7",
    },
    "wallet_mario": {
        'address': "AeT1nT8AM9jvDBiYWVKHj3NC6eACnmnpdU",
        'wif': "L3cm5QTxQncntWBVGZxFNSS2C7GEoL4Q3Mk8iKVXVvMTBrpjAyPM",
    }
}

SMART_CONTRACTS = {
    'ownership': {
        'scripthash': "6739aef754964ea9dba65761b16acb8e6efdfcd0",
        'methods': [
            'set_owner',
            'get_owner',
        ]
    },
    "composite_keys": {
        "scripthash": "0x4e24294d8a3fb9d3b5636003396e4ad42f5a3ef4",
        "methods": [
            "set_composite_key",
            "get_composite_key",
        ]
    },
    "identity": {
        "scripthash": "0xafc632a57a1b170bc4b8661b29c6fde27d6895f6",
        "methods": [
            "create_verification_request",
            "confirm_verification_request",
            "get_image_hashes_for_target_address",
            "get_verification_request_status",
        ]
    }
}


def set_owner():
    raw_tx = create_raw_sc_method_call_tx(
        source_address="AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y",
        source_address_wif="KxDgvEKzgSBPPfuVfw67oPQBSjidEiqTHURKSDL1R7yGaGYAeYnr",
        smartcontract_scripthash="6739aef754964ea9dba65761b16acb8e6efdfcd0",
        smartcontract_method="set_owner",
        smartcontract_method_args=[
            b"Mario Yeah Yeah Yeah",
        ],
    )

    try:
        result = client.send_raw_tx(raw_tx, id=2, endpoint=RPCEndpoint(client=None, address=endpoint))
        if result:
            print(result)

    except Exception as e:
        print("Error: {}".format(e))
        print('')


def get_owner():
    return read_contract_method(
        SMART_CONTRACTS.get('ownership').get('scripthash'),
        "get_owner",
        [],
    )

# get_owner()


def set_composite_key():
    raw_tx = create_raw_sc_method_call_tx(
        source_address=WALLETS.get('main_wallet').get('address'),
        source_address_wif=WALLETS.get('main_wallet').get('wif'),
        smartcontract_scripthash=SMART_CONTRACTS.get('composite_keys').get('scripthash'),
        smartcontract_method="set_key_by_composites",
        smartcontract_method_args=[
            b"ab",
            b"cd",
            b"compositevalue123",
        ],
    )

    result = client.send_raw_tx(raw_tx, id=2, endpoint=RPCEndpoint(client=None, address=endpoint))
    if result:
        print(result)



# set_composite_key()

def get_key(key):
    return read_contract_method(
        SMART_CONTRACTS.get('composite_keys').get('scripthash'),
        "get_key",
        [{"type": 5, "value": key}],
    )

# get_key("abcd")


def get_composite_key(key_part1, key_part2):
    return read_contract_method(
        SMART_CONTRACTS.get('composite_keys').get('scripthash'),
        "get_key_by_composites",
        [{"type": 5, "value": key_part1},{"type": 5, "value": key_part2}],
    )

# get_composite_key("ab", "cd")


def create_verification_request():
    raw_tx = create_raw_sc_method_call_tx(
        source_address=WALLETS.get('wallet_chris').get('address'),
        source_address_wif=WALLETS.get('wallet_chris').get('wif'),
        smartcontract_scripthash=SMART_CONTRACTS.get('identity').get('scripthash'),
        smartcontract_method="create_verification_request",
        smartcontract_method_args=[
            bytes(WALLETS.get('wallet_mario').get('address'), 'utf-8'),  # source_address
            bytes(WALLETS.get('wallet_chris').get('address'), 'utf-8'),  # target_address
        ],
    )

    result = client.send_raw_tx(raw_tx, id=2, endpoint=RPCEndpoint(client=None, address=endpoint))
    if result:
        print(result)


# create_verification_request()

def get_verification_request_status(source_address, target_address):
    return read_contract_method(
        SMART_CONTRACTS.get('identity').get('scripthash'),
        "get_verification_request_status",
        [{"type": "String", "value": source_address}, {"type": "String", "value": target_address}],
    )

get_verification_request_status(
    source_address=WALLETS.get('wallet_mario').get('address'),
    target_address=WALLETS.get('wallet_chris').get('address'),
)


def confirm_verification_request():
    raw_tx = create_raw_sc_method_call_tx(
        source_address=WALLETS.get('wallet_mario').get('address'),
        source_address_wif=WALLETS.get('wallet_mario').get('wif'),
        smartcontract_scripthash=SMART_CONTRACTS.get('identity').get('scripthash'),
        smartcontract_method="confirm_verification_request",
        smartcontract_method_args=[
            bytes(WALLETS.get('wallet_mario').get('address'), 'utf-8'),  # source_address
            bytes(WALLETS.get('wallet_chris').get('address'), 'utf-8'),  # target_address
            bytes("example-image-has-from-python", 'utf-8'),  # image hash
        ],
    )

    result = client.send_raw_tx(raw_tx, id=2, endpoint=RPCEndpoint(client=None, address=endpoint))
    if result:
        print(result)


# confirm_verification_request()


def get_image_hashes(target_address):
    return read_contract_method(
        SMART_CONTRACTS.get('identity').get('scripthash'),
        "get_image_hashes_for_target_address",
        [{"type": "String", "value": target_address}],
    )


get_image_hashes(
    target_address=WALLETS.get('wallet_chris').get('address')
)

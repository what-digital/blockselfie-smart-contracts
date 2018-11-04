"""

SC Script Hashes:

- v1.0: 0xa6bded14c4cda7a64e87c1a98b2a34beec5071c3


Testing:
- build sc/identity.py test 0710 07 True False False get_image_hashes_for_target_address ["ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc"]

Importing:
- build sc/identity.py
- import contract sc/identity.avm 0710 07 True False False
- contract search IdentityWhatDigital

Using:

Source Address: AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
Target Address: ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc

To be executed by target:
- testinvoke 0xa6bded14c4cda7a64e87c1a98b2a34beec5071c3 create_verification_request ["AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y", "ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc"] --from-addr=ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc

To be executed by source:
- testinvoke 0xa6bded14c4cda7a64e87c1a98b2a34beec5071c3 confirm_verification_request ["AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y", "ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc", "123imagehash"] --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y

To be executed by third-party (read only)
- testinvoke 0xa6bded14c4cda7a64e87c1a98b2a34beec5071c3 get_image_hashes_for_target_address ["ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc"]

To be executed by third-party (read only)
- testinvoke 0xa6bded14c4cda7a64e87c1a98b2a34beec5071c3 get_verification_request_status ["AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y", "ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc"]

"""
from boa.interop.Neo.Runtime import Log, Notify
from boa.interop.Neo.Storage import Get, Put, GetContext
from boa.interop.Neo.Runtime import GetTrigger, CheckWitness
from boa.builtins import concat


# a verification request can have the following stati
PENDING_STATUS = "PENDING"
CONFIRMED_STATUS = "CONFIRMED"


def Main(operation, args):

    nargs = len(args)
    if nargs == 0:
        print("No arguments supplied")
        return 0

    if operation == 'create_verification_request':
        source_address = args[0]
        target_address = args[1]
        return create_verification_request(source_address, target_address)

    elif operation == 'confirm_verification_request':
        if nargs < 2:
            print("required arguments: [image_hash] [target_address]")
            return 0
        source_address = args[0]
        target_address = args[1]
        image_hash = args[2]
        return confirm_verification_request(source_address, target_address, image_hash)

    elif operation == 'get_image_hashes_for_target_address':
        target_address = args[0]
        return get_image_hashes_for_target_address(target_address)

    elif operation == 'get_verification_request_status':
        source_address = args[0]
        target_address = args[1]
        return get_verification_request_status(source_address, target_address)


def create_verification_request(source_address, target_address):
    """
    The target user is doing this!
    :param target_address:
    :param source_address:
    :return:
    """

    msg = concat("Target users requests verification from ", source_address)
    Notify(msg)

    # if not CheckWitness(target_address):
    #     Notify("target_address argument is not the same as the tx sender")
    #     return False

    context = GetContext()
    key = _build_verification_request_key(source_address, target_address)
    result = Get(context, key)

    if not result:
        msg = concat("Verification request has been created for source ", source_address)
        Notify(msg)
        Put(context, key, PENDING_STATUS)
        return True

    Notify("Verification has already been started or completed for this source target combination")
    return False


def confirm_verification_request(source_address, target_address, image_hash):
    """
    The source user is doing this!
    :param source_address:
    :param image_hash:
    :param target_address:
    :return:
    """

    context = GetContext()

    msg = concat("Source user is confirming verification for ", target_address)
    Notify(msg)

    # if not CheckWitness(source_address):
    #     Notify("source_address argument is not the same as the tx sender")
    #     return False

    key = _build_verification_request_key(source_address, target_address)
    result = Get(context, key)

    # if value for {target}_{source/sender} is PENDING, set to CONFIRMED
    if result == PENDING_STATUS:
        Put(context, key, CONFIRMED_STATUS)

        comma_separated_list_of_image_hashes = Get(context, target_address)

        if comma_separated_list_of_image_hashes:
            comma_separated_list_of_image_hashes = concat(comma_separated_list_of_image_hashes, image_hash)
        else:
            comma_separated_list_of_image_hashes = concat(image_hash, ",")

        Put(context, target_address, comma_separated_list_of_image_hashes)
        msg = concat('The verification request has been confirmed by ', source_address)
        Notify(msg)
        return True

    Notify("Verification has not yet been initiated by the target address (or another error occurred)")
    return False


def get_image_hashes_for_target_address(target_address):
    """
    anyone can get this information
    :param target_address:
    :return:
    """

    context = GetContext()
    comma_separated_list_of_image_hashes = Get(context, target_address)

    Notify(comma_separated_list_of_image_hashes)
    return comma_separated_list_of_image_hashes


def get_verification_request_status(source_address, target_address):
    context = GetContext()
    key = _build_verification_request_key(source_address, target_address)
    result = Get(context, key)
    Notify(result)
    return result


def _build_verification_request_key(source_address, target_address):
    text = concat(source_address, '_')
    key = concat(text, target_address)
    return key

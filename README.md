## Installation

- `mkvirtualenv neo-python --python /usr/local/bin/python3`
- `pip install -r requirements.txt`


## Run neo-python with the what-digital node

- `np-prompt --privnet neo-privnet.what.digital`
- `open wallet wallet.wallet` # password is `coz`

## Funding of Wallets

- send gas ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc 555 --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y
- send neo ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc 555 --from-addr=AK2nJJpJr6o664CWJKi1QRXjqeic2zRp8y

## Build smartcontracts

### Hello World

- `build sc/hello_world.py test '' 01 False False False`
- import contract path/to/sample2.avm {input_params} {return_type} {needs_storage} {needs_dynamic_invoke} [is_payable]
- import contract sc/hello_world.py "" 01 False False False


### Identity

- build sc/identity.py test '' 01 True False False create_verification_request ALA1eYePMiNVfiHvQGVnupDFmjoPFwSoUc AeT1nT8AM9jvDBiYWVKHj3NC6eACnmnpdU

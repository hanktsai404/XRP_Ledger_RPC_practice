'''
This file stands for lib to store json rpc format

Some format note:
    1. Address is made up of r ## ID ## checksum (25 bytes)

    2. ECDSA public key is compressed with prefix (33 bytes)
        0x02 if y-coordinate is even
        0x03 if y-coordinate is odd

    3. Signature: DER form (same as bitcoin)
        Sig = 0x30 ## len(following data) (one byte) ## 0x02 ## len(r) (one byte) ## r in Big-Endian
            ## 0x02 ## len(s) ## s in Big-Endian
        For secp256k1, usually len(r) = len(s) = 20, but when their (r,s) first byte is greater than 0x7F,
        they must be prepended with 0x00
        With no first byte > 0x7F, the signature length is 70 bytes
'''
import json

def get_rpc_format(method = None):
    if method == None:
        return None
    with open("RPC_format.json", "r") as format_file:
        call = json.loads(format_file.read())[method]
    return call

# Account_info
def account_info(account = None):
    if account == None:
        return None
    call = get_rpc_format("account_info")
    call["params"][0]["account"] = account["address"]
    # print(call)
    return call

# Fee_info
def fee_info():
    call = get_rpc_format("fee")
    # print(call)
    return call

def submit_tx(blob = None):
    if blob == None:
        return None
    call = get_rpc_format("submit")
    call["params"][0]["tx_blob"] = blob
    return call

def sign(tx = None, secret = None):
    '''This is for test use, one should never deliver her secret to an 
        untrusted server or in an insecure channel'''
    if tx == None or secret == None:
        return None
    call = get_rpc_format("sign")
    call["params"][0]["secret"] = secret
    call["params"][0]["tx_json"] = tx
    print(call)
    return call
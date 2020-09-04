'''
This file stores function to create, sign, send and track transactions
Transaction formats are stored in tx_format.json
'''
import json
from requests import post

def get_tx_format(tx_type = None):
    if tx_type == None:
        return None
    with open("tx_format.json", "r") as tx_format_file:
        form = json.loads(tx_format_file.read())[tx_type]
    return form

def get_last_ledger():
    with open("RPC_format.json", "r") as rpc_file:
        call = json.loads(rpc_file.read())["ledger_closed"]
    with open("testnet_keys.json", "r") as url_file:
        url = json.loads(url_file.read())["testnet_url"]
    result = post(url, json = call).json()["result"]["ledger_index"]
    print("get last ledger!")
    return result


def bytes_to_hex(bytes_array):
    result = str()
    for byte in bytes_array:
        str_hex = str(hex(int(byte)))[2:].upper()
        while len(str_hex) < 2:
            str_hex = "0" + str_hex
        # print(str(byte) + "  "+str_bin)
        result = result + str_hex
    return result


# Direct XRP payment
def get_direct_payment_tx(account = None, dest = None, amount = None, fee = None, public_key = None, sig = None):
    if account == None or dest == None or amount == None or fee == None:
        return None
    form = get_tx_format("payment")
    form["Account"] = account["address"]
    form["Destination"] = dest["address"]
    form["Amount"] = amount
    form["Fee"] = fee
    form["LastLedgerSequence"] = get_last_ledger() + 20  # Wait until 20 ledgers later
    form["Sequence"] = account["Sequence"] + 1
    if not public_key == None and not sig == None:
        form["SigningPubKey"] = public_key.upper()
        form["TxnSignature"] = sig.upper()
    return form

def get_direct_payment_blob(account = None, dest = None, amount = None, fee = None):
    if account == None or dest == None or amount == None or fee == None:
        return None
    tx = get_direct_payment_tx(account, dest, amount, fee)
    from tx_serialization import serialize as serial
    return serial.serialize_tx(tx, for_signing = True)
    # print(blob)

def signed_tx_to_hex(tx):
    from tx_serialization import serialize as serial
    result = serial.serialize_tx(tx, for_signing = False)
    result = bytes_to_hex(result)
    return result

# Testing
if __name__ == "__main__":
    print("Last ledger's id:")
    print(get_last_ledger())
    print()
    print("Demo payment tx:")
    print(get_direct_payment_tx("1234567", "2345678", "10"))
    print()
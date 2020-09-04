'''
This program connects to XRP Ledger's testnet, and the project is not for production use.
We will perform a way to trace current account balances.
Then, we conduct a direct transaction, and see whether the balance change.
Since the author doesn't own a fuded XRP account, we can only conduct this on testnet
The major issue here is that we don't know how ripple transmit secret to private key.
Either can we generate key by ourself since all testnet accounts are generated and funded by the official website
The issue will be fixed on further commitment, now we let the users input the key theirselves

All of the files in tx_serialization are from ripple's sample code
https://github.com/ripple/xrpl-dev-portal/tree/master/content/_code-samples/tx-serialization
'''
import json
import requests
import RPC_call_lib as call
import tx_lib as tx 
from tx_serialization import serialize as serial
from ECDSA import secp256k1 as ecc
from ECDSA import sign


'''
====================================Initialization==========================================
'''
# Read data from json
with open("testnet_keys.json", "r") as data_file:  # url & two keys
    testnet_data = json.loads(data_file.read())
    # print("Keys json open sucessfully!")
    testnet_url = testnet_data["testnet_url"]
    send_account = testnet_data["key1"]
    receive_account = testnet_data["key2"]

send_account["address"] = input("Please enter your address:")
send_account["secret_int"] = input("Please enter your secret key:")
send_account["secret_int"] = int(send_account["secret_int"], 16)

# Get public key
send_account["public_key"] = ecc.get_str_public_key(send_account["secret_int"])
# receive_account["public_key"] = ecc.get_str_public_key(receive_account["secret_int"])

'''
=======================================Functions=========================================
'''
def print_account_info(account, name):
    info = requests.post(testnet_url, json = call.account_info(account)).json()
    account["Sequence"] = info["result"]["account_data"]["Sequence"]
    balance = info["result"]["account_data"]["Balance"]
    queue_count = info["result"]["queue_data"]["txn_count"]
    print("The "+name+" address is: "+account["address"])
    print("Balance:\t" + balance)
    print("#Queue txn:\t" + str(queue_count))
    print()


def print_fee():
    fee_info = requests.post(testnet_url, json = call.fee_info()).json()
    print("The fee information of the server is as follows:")
    base_fee = fee_info["result"]["drops"]["base_fee"]
    median_fee = fee_info["result"]["drops"]["median_fee"]
    minimum_fee = fee_info["result"]["drops"]["minimum_fee"]
    open_ledger_fee = fee_info["result"]["drops"]["open_ledger_fee"]
    print("Base fee:\t\t" + base_fee)
    print("Median fee:\t\t" + median_fee)
    print("Minimum fee:\t\t" + minimum_fee)
    print("Open ledger fee:\t" + open_ledger_fee)
    print()

def server_sign(tx, account):
    ''' For test purpose, unfortunately server sign does not support in test net server'''
    res = requests.post(testnet_url, json = call.sign(tx, account["secret"])).json()
    print(res)
    return res["result"]["tx_blob"]

'''
======================================Main program=========================================
'''
# Ask for account's info
print_account_info(send_account, "sending")
print_account_info(receive_account, "receiving")

# Ask for fee info
# print_fee()

# Ask for sending amount and fee
send_amount = int(input("XRP amount to deliver:"))
send_amount = str(send_amount * 1000000)  # XRP to drop

fee = input("Fee to be destroyed (in drops):")

# Get the tx (server_tx for testing)
payment_tx = tx.get_direct_payment_blob(send_account, receive_account, send_amount, fee)  # tx in bytes
sig = sign.ecdsa_sign(payment_tx, send_account["secret_int"]) # sig in hex

signed_payment = tx.get_direct_payment_tx(send_account, receive_account, send_amount, fee, send_account["public_key"], sig)
print(json.dumps(signed_payment, indent = 2))

tx_blob = tx.signed_tx_to_hex(signed_payment)  # tx_blob must be in hex

# Submit
submit_res = requests.post(testnet_url, json = call.submit_tx(tx_blob)).json()
print(json.dumps(submit_res, indent = 2))

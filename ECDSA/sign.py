'''
This file works with secp256k1.py
This program is responsible for calculating hash value and ECDSA signature
In XRP Ledger, we use SHA512 half as hash function
'''
import hashlib
from ECDSA import secp256k1
from sympy import mod_inverse
from random import randint

def tx_to_hash(tx):
    # print(tx.hex().upper())
    hash_value = hashlib.sha512()
    hash_value.update(tx)
    # print(hash_value.hexdigest())
    return hash_value.hexdigest()[0:64]

def get_DER_format(sig):
    '''
    input (r, s) in byte without 0x
    Signature: DER form (same as bitcoin)
        Sig = 0x30 ## len(following data) (one byte) ## 0x02 ## len(r) (one byte) ## r in Big-Endian
            ## 0x02 ## len(s) ## s in Big-Endian
        For secp256k1, usually len(r) = len(s) = 20, but when their (r,s) first byte is greater than 0x7F,
        they must be prepended with 0x00
        With no first byte > 0x7F, the signature length is 70 bytes
    '''
    r = sig[0]
    s = sig[1]
    if not len(r)%2 == 0:
        r = "0" + r
    if not len(s)%2 == 0:
        s = "0" + s
    if int(r[:2], 16) > 0x7f:
        r = "00" + r
    if int(s[:2], 16) > 0x7f:
        s = "00" + s
    
    r_len = hex(len(r) // 2)[2:] # len in byte
    if not len(r_len) == 2:
        r_len = "0" + r_len
    s_len = hex(len(s) // 2)[2:]
    if not len(s_len) == 2:
        s_len = "0" + s_len
    
    temp = "02" + r_len + r + "02" + s_len + s
    t_len = hex(len(temp) // 2)[2:]
    if not len(t_len) == 2:
        t_len = "0" + t_len
    return ("30" + t_len + temp)

def ecdsa_sign(tx, secret_int):
    # 1.2. Calculate hash
    tx_hash = int(tx_to_hash(tx), 16)
    print("tx_hash:")
    print(hex(tx_hash))
    print()
    print("secret int:")
    print(hex(secret_int))
    print()
    while True:
        # 3. Select a randon integer
        k_E = randint(2 ** 255, secp256k1.n-1)
        # 4. Calculate k_E * G
        R_point = secp256k1.scalar_mult(k_E, secp256k1.curve.g)
        r = R_point.x
        if r == 0: continue
        # 5. Calculate s
        s = (mod_inverse(k_E, secp256k1.n) * (tx_hash + (secret_int * r))) % secp256k1.n
        if s == 0: continue
        break
    
    sig = get_DER_format((hex(r)[2:], hex(s)[2:]))
    return sig

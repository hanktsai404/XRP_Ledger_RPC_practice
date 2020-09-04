'''
The cryptography package used in here are not capable for production.
We may switch ECDSA process to cold wallet (using embbeded system) later.
To install these package, use pip
    pip install sympy  https://pypi.org/project/tinyec/
    pip install tinyec  https://www.sympy.org/en/index.html
'''
from tinyec.ec import SubGroup, Curve

name = 'secp256k1'
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
n = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141
a = 0
b = 7
g = (55066263022277343669578718895168534326250603453777594175500187360389116729240, 32670510020758816978083085130507043184471273380659243275938904335757337482424)
h = 1
curve = Curve(a, b, SubGroup(p, g, n, h), name)

def is_even(target_int):
    '''Check if target is even or not'''
    return (int(str(target_int)[-1]) % 2 == 0)


def to_32_bytes_hex(target_int):
    '''Return hex in 32 bytes (256 bits)'''
    result = hex(target_int)
    result = result[2:]
    while True:
        if len(result) >= 64:  # 2 * 32 = 64
            break
        result = "0" + result
    return result


'''
ECDSA public key is compressed with prefix (33 bytes)
    0x02 if y-coordinate is even
     0x03 if y-coordinate is odd
'''
def get_str_public_key(secret):
    '''Given a private key, return the corresponding public key'''
    pub_k_point = secret * curve.g
    prefix = "03"  # y-coordinate is odd
    if is_even(pub_k_point.y):
        prefix = "02"
    pub_k = prefix + to_32_bytes_hex(pub_k_point.x)
    return pub_k

def scalar_mult(k, point):
    return (k * point)

def decode_secret(secret):
    '''Issue: how is the secret transmitted into private key?'''
    pass

# For testing
if __name__ == "__main__":
    # k = 30841466623270472059305507292879076905131222194802424691128988518654198144322
    # print("The testing public key is:" + get_str_public_key(k))
    # The answer should be 0380a58256b2b9a3f118c6a1ad762987e9ea84274e970f37c9c56ba6d09056712e
    pass
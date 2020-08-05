# we use secp256k1 / 256-bit curve for EC pairs
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib

def generate_ec_key_pairs():
    """generate ecdsa key pairs"""
    private = SigningKey.generate(curve=SECP256k1)
    public = private.verifying_key
    
    keys = {
            'private': private.to_string().hex(), 
            'public': public.to_string().hex()
            }
    return keys

def reverse_bytes(string):
    """reverse bytes: given big-endian change to little-endian and vice-versa"""

    ba = bytearray.fromhex(string)
    ba.reverse()
    rev = (''.join(format(x, '02x') for x in ba)).upper()
    return rev

def hash160(string):
    """given string -> return hash160 (first sha256 then ripemd160)"""

    hexstr = string.decode('hex')
    hash160 = hashlib.new('ripemd160', hashlib.new('sha256', hexstr).digest()).digest()
    hash160hex = hash160.encode('hex')
    return hash160hex

class Base58:
    encode = {i: "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"[i] for i in range(58)}
    decode = {"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"[i]: i for i in range(58)}

    @staticmethod
    def base58encode(string):
        """encode string to base58"""
        num = int(string, 16)
        
        output = ""
        while True:
            quot = num // 58
            rem = num % 58

            if quot == num:
                break
    
            output = Base58.encode[rem] + output
            num = quot
        return output

    @staticmethod    
    def base58decode(string):
        """decode string to base58"""

        size = len(string)
        value = 0
        for i, s in enumerate(string):
            value += Base58.decode[string[size-i-1]] * (58**i)
        return hex(value)[2:]


if __name__ == '__main__':
    # a = generate_ec_key_pairs()
    # print(a)
    # x = reverse_bytes("520a")

    s = "abc71284bc7af72"
    t = "2o9upwhcJCR"
    x = Base58.base58encode(s)
    y = Base58.base58decode(t)
    print(x)
    print(y)
# we use secp256k1 / 256-bit curve for EC pairs
from ecdsa import SigningKey, VerifyingKey, SECP256k1
import hashlib
from script_interpreter import ScriptInterpreter

def generate_ec_key_pairs():
    """generate ecdsa key pairs"""
    private = SigningKey.generate(curve=SECP256k1)
    public = private.verifying_key
    
    keys = {
            'private': private.to_string().hex(), 
            'public': public.to_string().hex()
            }

    # print("ppkey-make: ", private.to_string())
    return keys

def reverse_bytes(string):
    """reverse bytes: given big-endian change to little-endian and vice-versa"""
    ba = bytearray.fromhex(string)
    ba.reverse()
    rev = (''.join(format(x, '02x') for x in ba)).upper()
    return rev


def hash160(string):
    """given string -> return hash160 (first sha256 then ripemd160)"""

    hash160 = hashlib.new('ripemd160', hashlib.sha256(str.encode(string)).digest())
    hash160hex = hash160.hexdigest()
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

def double_sha256(text):
    hash1 = hashlib.sha256(str.encode(text)).hexdigest()
    hash2 = hashlib.sha256(str.encode(hash1)).hexdigest()
    return hash2

def calculate_merkle_root(hashes, arity=2):
    if(len(hashes) == 0):
        return None
    if len(hashes) == 1:
        return double_sha256(hashes[0] + hashes[0])
    # remaining = arity - (len(hashes) % arity)
    remaining = (len(hashes) % arity)
    for i in range(remaining):
        hashes.append(hashes[-1])

    new_hashes = []
    for i in range(0, len(hashes), arity):
        combined_hash = "".join(hashes[i:i+arity])
        new_hashes.append(double_sha256(combined_hash))

    return calculate_merkle_root(new_hashes, arity)

def create_script_pub_key(pub_key):
    return hash160(pub_key)

def create_script_sig(keys, serialized_txn):
    """serialized_txn is usually the messaage to make the 
    use of digital signature one time thing
    """
    digital_sig = ScriptInterpreter.get_digital_signature(serialized_txn, keys['private'])
    return digital_sig + keys['public']

if __name__ == '__main__':
    # a = generate_ec_key_pairs()
    # print(a)
    # x = reverse_bytes("520a")

    # s = "abc71284bc7af72"
    # t = "2o9upwhcJCR"
    # x = Base58.base58encode(s)
    # y = Base58.base58decode(t)
    # print(x)
    # print(y)
    pass
    # hashes = [
    #     'aa',
    #     'bb',
    #     'cc',
    #     'dd',
    #     'ee',
    #     'ff',
    #     '22'
    # ]
    # print(calculate_merkle_root(hashes, 3))
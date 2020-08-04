# we use secp256k1 / 256-bit curve for EC pairs
from ecdsa import SigningKey, VerifyingKey, SECP256k1

def generate_ec_key_pairs():
    private = SigningKey.generate(curve=SECP256k1)
    public = private.verifying_key
    
    keys = {
            'private': private.to_string().hex(), 
            'public': public.to_string().hex()
            }
    return keys

def sign_key(public, message):
    return public.sign(b'{}'.format(message))

# convert to little-endian format 
def reverse_bytes(string):
    ba = bytearray.fromhex(string).reverse()
    rev = (''.join(format(x, '02x') for x in ba)).upper()
    return rev

if __name__ == '__main__':
    a = generate_ec_key_pairs()
    print(a)
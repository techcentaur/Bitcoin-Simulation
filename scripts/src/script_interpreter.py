import utils
import ecdsa
from hashlib import sha256
from ecdsa import SigningKey, SECP256k1, VerifyingKey

class ScriptInterpreter:
    @staticmethod
    def verify_pay_to_pubkey_hash(script_signature, pub_key_script, message):
        """
        Bitcoin version:
            out: scriptPubKey: OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
            inp: scriptSig: <digital-signature> <pubKey>
        """

        signature = script_signature[:128]
        pub_key = script_signature[128:]
        
        pub_hash160 = utils.hash160(pub_key)
        if not (pub_hash160.strip() == pub_key_script.strip()):
            return False

        message = str.encode(message)
        vk = VerifyingKey.from_string(bytearray.fromhex(pub_key),
                            curve=ecdsa.SECP256k1)
        return vk.verify(bytearray.fromhex(signature), message)

    @staticmethod
    def get_digital_signature(message, private_key):
        """ message should be of class bytes
            private_key is a hex string
        """
        sk = SigningKey.from_string(bytearray.fromhex(private_key), curve=SECP256k1)

        signature = sk.sign(str.encode(message))
        signature = bytearray(signature).hex()
        return signature
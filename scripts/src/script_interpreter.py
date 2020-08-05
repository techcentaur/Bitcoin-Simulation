import utils
import ecdsa
from hashlib import sha256

class ScriptInterpreter:
    @staticmethod
    def verify_pay_to_pubkey_hash(script_signature, pub_key_script, message):
        """
        Bitcoin version:
            scriptPubKey: OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
            scriptSig: <sig> <pubKey>
        """

        signature = script_signature[:-64]
        pub_key = script_signature[-64:]
        
        pub_hash160 = utils.hash160(pub_key)
        if not (pub_hash160.strip() == pub_key_script.strip()):
            return False

        vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(pub_key),
                            curve=ecdsa.SECP256k1,
                            hashfunc=sha256)
        # message should be of class bytes
        return (vk.verify(bytes.fromhex(signature), message)):
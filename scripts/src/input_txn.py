from utils import reverse_bytes

class InputTXN:
    def __init__(self, txnid, vout, signature_script):
        self.txnid = txnid
        self.vout = vout
        self.signature_script = signature_script

    def get_txn_input_data(self):
    	reverse_txid = reverse_bytes(self.txnid)
    	vout_to_hex = self.vout
    	vout_to_hex = '0'*(8-len(vout_to_hex)) + vout_to_hex
    	reverse_vout = reverse_bytes(vout_to_hex)
    	scriptsig_size = hex(len(self.signature_script)//2)[2:]
    	return reverse_txid + reverse_vout + scriptsig_size + self.signature_script + "ffffffff"

    def create_copy(self):
    	return InputTXN(self.txnid, self.vout, self.signature_script)
    	

if __name__ == "__main__":
	# inptxn = InputTXN("123abcd4092e",2, "aedfasdfsdfe")
	# print(inptxn.get_txn_input_data())
    pass

from utils import reverse_bytes

class OutputTXN:
    def __init__(self, amount, script_pub_key):
        self.amount = amount
        self.script_pub_key = script_pub_key

    def get_txn_output_data(self):
    	hex_amount = hex(self.amount)[2:]
    	hex_amount = (16 - len(hex_amount))*'0' + hex_amount
    	reverse_amount = reverse_bytes(hex_amount)
    	pubkey_size = hex(len(self.script_pub_key)//2)[2:]
    	return reverse_amount + pubkey_size + self.script_pub_key

    def create_copy(self):
    	return OutputTXN(amount, script_pub_key)

if __name__ == "__main__":
	output_txn = OutputTXN(314, "abcdef123456")
	print(output_txn.get_txn_output_data())
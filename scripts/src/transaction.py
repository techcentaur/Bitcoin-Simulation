from input_txn import InputTXN 
from output_txn import OutputTXN 
from utils import double_sha256, create_script_sig, create_script_pub_key
import config 

class TXN:
    def __init__(self, inp_txns, out_txns):
        self.inp_txns = inp_txns
        self.out_txns = out_txns
        self.create_txid()

    def create_txid(self):
        data = self.get_txn_data()
        self.txid = double_sha256(data)

    def get_txn_data(self):
        inp_count = hex(len(self.inp_txns))[2:]
        if(len(inp_count) == 1):
        	inp_count = '0' + inp_count

        datas = [inp_count]
        for inp in self.inp_txns:
        	datas.append(inp.get_txn_input_data())

        out_count = hex(len(self.out_txns))[2:]
        if(len(out_count) == 1):
        	out_count = '0' + out_count

        datas.append(out_count)
        for out in self.out_txns:
        	datas.append(out.get_txn_output_data())

        return "".join(datas)

    def create_copy(self):
    	inp_copy = [inp.create_copy() for inp in self.inp_txns]
    	out_copy = [out.create_copy() for out in self.out_txns]
    	return TXN(inp_copy, out_copy)

    @staticmethod
    def create_coinbase_txn(keys):
    	script_sig = create_script_sig(keys, "I am inevitable")
    	inp = InputTXN('0'*64, "f"*8, script_sig)

    	script_pub_key = create_script_pub_key(keys['public'])
    	out = OutputTXN(config.reward, script_pub_key)

    	txn = TXN([inp], [out])
    	return txn


if __name__ == "__main__":
	# inptxn = InputTXN("123abcd4092e",2, "aedfasdfsdfe")
	# output_txn = OutputTXN(314, "abcdef123456")
	# print(inptxn.get_txn_input_data())
	# print(output_txn.get_txn_output_data())
	# txn = TXN([inptxn], [output_txn])
	# print(txn.txid)

    pass

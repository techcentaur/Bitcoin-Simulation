from input_txn import InputTXN 
from output_txn import OutputTXN 

class TXN:
    def __init__(self, inp_txns, out_txns, txn_hash=None):
        self.inp_txns = inp_txns
        self.out_txns = out_txns
        self.txnid = txn_hash

    def create_txid(self):
        data = get_txn_data()
        self.txid = reverse_bytes(hash(hash(data)))

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

if __name__ == "__main__":
	inptxn = InputTXN("123abcd4092e",2, "aedfasdfsdfe")
	output_txn = OutputTXN(314, "abcdef123456")
	print(inptxn.get_txn_input_data())
	print(output_txn.get_txn_output_data())
	txn = TXN([inptxn], [output_txn])
	print(txn.get_txn_data())



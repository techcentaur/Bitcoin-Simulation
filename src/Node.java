public class Node{
	private Blockchain blockchain;

	// this is for verification of the incoming txns in blocks
	private List<UTXO> unspentTransactions; 


	public boolean verifyBlock(Block block){
		for(Transaction txn: block.getTransaction()){
			//
		}
	}

	public void addInBlockchain(Block block){

	}

	public List<OutputTXN> getAmountFromSpendableUTXOs(float amount){

	}

	public List<OutputTXN> getAllSpendableUTXOs(){

	}

	public void sendCoin(String address, float amount){

	}
}
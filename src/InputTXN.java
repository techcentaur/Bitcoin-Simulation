public class InputTXN{
	private String txnId;
	private int txnOutputIndex;

	private String pubKey;

	public boolean useTransaction(String pubKeyHash){
		// check if this hash is valid for pubKey
		return true;
	}
}
import java.util.List;

public class Block {
    private String hash;

    private int version;
    private int numTransactions;

    private long height;
    private long nonce;
    private long blockIndex;

    private String previousBlock;
    private String merkelRoot;

    private List<String> transactions;

    public static Block mineBlock(){
        return new Block();
    }

    public static Block createGenesisBlock(){
        return new Block();
    }
}

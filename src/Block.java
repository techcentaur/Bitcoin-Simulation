import java.util.List;

public class Block {

    private BlockHeader header;
    private String hash;

    private int numTransactions;

    private long height;
    private long blockIndex;

    private List<String> transactions;

    public static Block mineBlock(){
        return new Block();
    }

    public static Block createGenesisBlock(){
        return new Block();
    }
}

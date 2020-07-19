import java.util.List;

public class BlockHeader {
    private int version;
    private String previousBlock;
    private String merkelRoot;
    private int nBits;
	private long nonce;

    public int getVersion() {
        return version;
    }

    public void setVersion(int version) {
        this.version = version;
    }

    public String getPreviousBlock() {
        return previousBlock;
    }

    public void setPreviousBlock(String previousBlock) {
        this.previousBlock = previousBlock;
    }

    public String getMerkelRoot() {
        return merkelRoot;
    }

    public void setMerkelRoot(String merkelRoot) {
        this.merkelRoot = merkelRoot;
    }

    public int getnBits() {
        return nBits;
    }

    public void setnBits(int nBits) {
        this.nBits = nBits;
    }

    public long getNonce() {
        return nonce;
    }

    public void setNonce(long nonce) {
        this.nonce = nonce;
    }
}
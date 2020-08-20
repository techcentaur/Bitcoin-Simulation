## Bitcoin-Simulation

### Introduction

Bitcoin is a decentralized digital cryptocurrency that is built upon the central idea of coming to a consensus on what verified peer-to-peer transactions happened (to avoid double-spending); this consensus is between all nodes participating within a network without reinforcement by an entity with extra power than others.

Specifically, peer-to-peer transactions are verified by other nodes on network through cryptographical utilities with the share of a public distributed ledger called a blockchain. Introduction of this currency in the network has arisen once during the creation of genesis block. It now continues to be introduced as a reward for mining an appropriate block in the blockchain.

## Simulation Architecture

### Key-Pair at Node
We use the Elliptic Curve Digital Signature Algorithm (ECDSA) as the algorithm to generate private and public key. We use hash160 of the public key for verifying the signature script and base58 encoding for the better visualization of addresses to ease the peer-to-peer transaction.

```python
class Node:
    def __init__(self):
        self.keys = utils.generate_ec_key_pairs()
        self.pub_key_hash = utils.hash160(self.keys['public'])
        self.address = utils.Base58.base58encode(hash160)
```
### Proof of Work

Central to the issue of consensus is the problem of how do all nodes on the network agree on what transactions have been made. Proof of work is a cryptographic puzzle that when one node solves first, others can verify on their own and agree to it.

Explicitly, the Bitcoin mining process incorporates a proof of work system based on Adam Back's Hashcash. It ensures two properties:

- A node that has performed `work` must have made some effort (it need to be proved.)
- That proof should be efficiently verifiable by other nodes.

#### Design Implementation:

- A target hash has been set: that starts with a particular number of 0's. For e.g. "000000xxxx...x" starts with 6 zeros.
- We double-hash (SHA-256) the serialized block header with a value called `nonce` until a hash is generated which is less than target hash,
- If so then we have successfully mined a block.
- But while doing this how do we know if some other node has mined the block first while we are still mining?
- We have decided that our node will perform 1000 nonce values and then check its messages if it had received a newly mined correct block from the network.
- If yes, we stop our mining, add that block in our block-chain, and start again on a new set of transactions in waiting pool (add those who are not yet included in mined block)
- If no, then we continue our mining.
        
    
Here's a snippet of code:

```python
class Proof:
    def __init__(self, block):
        self.quit = False
        self.block = block

        # Here's our target hash in hex
        self.target_hash = "0"*block.bits + "1" + "0"*(64 - block.bits)

    def run(self, start):
        # do for 1000 nonce values and then check messages
        for nonce in range(start+1, sys.maxsize): # 2^63-1
            if self.quit:
                return None 
            _hash = self.get_hash(nonce)
            if _hash < self.target_hash:
                return Work(nonce, _hash)

            if(nonce % 1000 == 0):
                return nonce

    def get_hash(self, nonce):
        # double hash serialized block header with nonce 
        return double_sha256(self.block.get_serialized_block_header(nonce))
```
### Coinbase Transaction
Coinbase is the first transaction in any block that is created as an incentive for successfully mining a block. Since its input transaction reference is to none, it has been decided that vout would be -1 and sig script would be any random hex string and txnid is 64 bytes - all-zero string. And its output contains the amount as a reward of 50 bitcoins (in our simulation), and script pub key contains the pub-key hash160 of the node that mined that block.

```python
     ##########---------- TXN ----------##########
     [@] TXNID : cd552474b06342559a3ee0f2b12aca6d8e82af4f360a9cf1b22343f244480b09
         #####----- Input_txn -----#####
         [@] TXNID : 0000000000000000000000000000000000000000000000000000000000000000
         [@] Vout : -1
         [@] Sig Script : d1db4326fa3a7c3fc8f312ff7c649728e4fdcd18b29e56bb47d85bd2fb4395f14747e095f2fd0b2ef56359
         420d7766da98c3cf17f50b848403ff7aa7df1bcae6ae94e33927517778961c398e412ad6d7e1e550f2e19c
         d0c7785e72cb266625b87b442553e203e848c29528e011b0ca268a0023f354f1282412931c7f0087ce4a

         #####----- Output TXN -----#####
         [@] Amount : 50
         [@] Script Pub Key : 9e58390d0660fb71a85edc814f201e701211b632
```

We implement code in this fashion:
```python
    @staticmethod
    def create_coinbase_txn(keys):
        script_sig = create_script_sig(keys, "I am inevitable")
        inp = InputTXN('0'*64, -1, script_sig)

        script_pub_key = create_script_pub_key(keys['public'])
        out = OutputTXN(config.reward, script_pub_key)

        txn = TXN([inp], [out])
        return txn
```
### Genesis Block
- A genesis block is the first block of a blockchain. The genesis block is almost always hardcoded into the software of the applications that utilize its blockchain (as in the Bitcoin software). It is a particular case such that it does not refer to a previous block, and it produces the first unspendable subsidy.
- Our genesis block is also hard-coded in the blockchain. When a node starts, we give him a blockchain that already comes with the genesis block. This block has one coinbase transaction that rewards node-0 50 coins.
- We chose its hash as `000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f` because this is the hash of the first block of bitcoin (and it starts with at-least three zeros which is our bits limit).
- Prev-block-hash can be anything, and since it doesn't refer to anything, we chose it to be zero.
- It consists of one coinbase transaction, as defined above.


It looks like this (where the keys have usual meanings):

```python
 ##########---------- Block ----------##########
 [@] Nonce : 0
 [@] Hash : 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
 [@] Prev Block Hash : 0000000000000000000000000000000000000000000000000000000000000000
 [@] Bits : 3
 [@] Merkle Root : 6ae340ab52b654e0a2d92a3474ae8c2e74b8cfb7cc6d066a7e3f9ce4fc3c05a7
     ##########---------- TXN ----------##########
     [@] TXNID : cd552474b06342559a3ee0f2b12aca6d8e82af4f360a9cf1b22343f244480b09
         #####----- Input_txn -----#####
         [@] TXNID : 0000000000000000000000000000000000000000000000000000000000000000
         [@] Vout : -1
         [@] Sig Script : d1db4326fa3a7c3fc8f312ff7c649728e4fdcd18b29e56bb47d85bd2fb4395f14747e095f2fd0b2ef56359
         420d7766da98c3cf17f50b848403ff7aa7df1bcae6ae94e33927517778961c398e412ad6d7e1e550f2e19c
         d0c7785e72cb266625b87b442553e203e848c29528e011b0ca268a0023f354f1282412931c7f0087ce4a

         #####----- Output TXN -----#####
         [@] Amount : 50
         [@] Script Pub Key : 9e58390d0660fb71a85edc814f201e701211b632
```
## DesignChoices and Implementation Details
### Node's Working and Process Handling

Any node in the bitcoin network has the capability to do the following tasks:
- Create a peer-to-peer transaction
- Check for the received block if someone mined it first and verify it
- Check for any received transaction from the network and add it in its transaction pool
- Mine for the new block (this is optional, but we assume every node is participating in mining.)


Since in our simulation one thread is a node, our node has `messages()` as a queue. This thread does mining work for 1000 nonce values at a time and then stops briefly to check its messages and do the following task if required: 1. check received a transaction, check received block, or make a transaction. If no block is encountered, it continues to mine from the last nonce value, otherwise stops and starts mining for the next block.

```python
def check_messages(self):
    while len(self.messages):
        with self.lock:
            msg_type, msg = self.messages.popleft()
        
        if msg_type == "txn":
            _txn = msg.create_copy()
            self.receive_txn(_txn)
        elif msg_type == "block":
            block = msg.create_copy()
            self.recieve_block(block)
        elif msg_type == "new_txn":
            reciever_address, amount = msg[0], msg[1]
            ret = self.create_txn(reciever_address, amount)
```
### Block Verification

- Calculate the block hash from the block header and nonce to check if the hash is calculated correctly.
- Check the integrity of the hash of Merkle root tree
- Check if all input transactions exist as UTXO (unspent transaction outputs)
- For each input transaction:
- Verify the scripting signatures and pubkeyscript
- Verify that difference of output and input is < 0
    
- For coinbase transaction:
- Verify its vout and that its amount is no more than incentive from creating block and block fees in case any transaction it has a positive difference in input-amount and output-amount
- If everything above is true, the block is successfully verified
    


Here's the snippet of the code.

```python
    def verify_block(self, block):
        serial = block.get_serialized_block_header(block.nonce)
        
        # verifying hash of block
        hash_hex = double_sha256(serial)
        if not (hash_hex == block.hash and 
            block.merkle_root == block.get_merkle_root_hash()):
            return False

        # block.txns[0] is coinbase [ASSUMPTION]
        coinbase_future_reward = 0.0
        for txn in block.txns[1:]:
            input_amount = 0.0
            for inp_txn in txn.inp_txns:
                if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                    return False

                output_txn = self.UTXOdb.get_txn_by_txnid(inp_txn.txnid).out_txns[inp_txn.vout]
                if not ScriptInterpreter.verify_pay_to_pubkey_hash(
                    inp_txn.signature_script,
                    output_txn.script_pub_key,
                    inp_txn.txnid
                    ):
                    return False

                input_amount += output_txn.amount 

            output_amount = 0.0
            for out_txn in txn.out_txns:
                output_amount += out_txn.amount

            if output_amount > input_amount:
                return False
            coinbase_future_reward += (input_amount - output_amount)

        # verify coinbase
        coinbase = block.txns[0]
        if not ((len(coinbase.inp_txns) == 1) and (int(coinbase.inp_txns[0].txnid, 16) == 0)
                        and (int(coinbase.inp_txns[0].vout) == -1)
                        and (len(coinbase.out_txns) == 1)):
            return False
        
        if coinbase.out_txns[0].amount > coinbase_future_reward + config.reward:
            return False

        return True
```
### Managing Unspent Transaction Outputs (UTXOs)
- Every node maintains the unspent transaction outputs (UTXOs) on their own. To verify if a given transaction is correctly created.
- We have designed an n-depth-Trie data structure for it.
- This is a tree data structure whose any node can have 0-f (hex) values till a certain depth, and then at the nth index, the transaction and its possible vouts are stored in a list. This facilitates the fast searching, adding and removal of transaction references.
- For e.g. if we have a txn with id: ab23bcf65 and it has possible vout of 0, 1, 2; say we have a 2-depth Trie DS. We save it like this:
- a $->$ b $->$ ["ab23bcf65": {vout:[0, 1, 2]}]
- if I add another txn: a923bcf65 with vout as 0, 1; it will be added as:
                a $->$ [ b $->$ ["ab23bcf65": {vout:[0, 1, 2]}],
                9 $->$ ["a923bcf65": {vout:[0, 1]}]]    
    
- Benefits:
- Fewer data in memory at a time
- A quick search for UTXOs, addition and removal
   

### Chain Stabilization and Reorganization}

We maintain the main branch of blockchain as new blocks are getting added. This is checked by `self.longest\_active\_head` in `chain\_stabilize.py`. 

Say a new block B arrives:
- If B's previous hash is the `self.longest\_active\_head` of the main branch, we add the block. Removing B's input\_transaction references from UTXO database and adding new output references to it.
- If not we check where the B's previous hash is and add it there (without any change to UTXO database)
- If after adding B the side chain becomes the longest chain in blockchain
- Then we backtrack all the transaction of the main branch till the intersectional node and then continue on the side branch (by making a necessary change to UTXOs)
- This would effectively make the side branch as the main branch
        
    
- At last, we check if the side branch and main branch differs by a gap of `orphan\_threshold.`
- If yes, then we remove the side branch and check if the transactions they had contained are already added in the main blockchain
- If no, then we circulate them again on the network.
    


Below are the snippets of code for this implementation.
- Backtracking on previous main branch till the cross-section block and then moving in the new main branch
    ```python
        def reorganize_blocks(self, reorg_dict):
        # removing blocks in back-track of prev main chain
        for block in reorg_dict['blocks_to_remove']:
            for txn in block.txns:
                self.UTXOdb.remove_by_txn(txn)

            for txn in block.txns[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.add_by_txnid(inp_txn.txnid, inp_txn.vout)

        # adding blocks in front-track of new main chain
        for block in reorg_dict['blocks_to_add']:
            for txn in block.txns[1:]:
                for inp_txn in txn.inp_txns:
                    self.UTXOdb.remove_by_txnid(inp_txn.txnid, inp_txn.vout)
            
            for txn in block.txns:
                self.UTXOdb.add_by_txn(txn)
- Distribution of unadded transactions of orphan nodes on the network
    ```python
        def orphan_txns_redistribute(self):
        o_blocks = self.stabilize.check_for_orphan_nodes()
        if o_blocks:
            for block in o_blocks:
                for txn in block.txns:
                    for inp_txn in txn.inp_txns:
                        if not self.UTXOdb.search_by_txnid(inp_txn.txnid, inp_txn.vout):
                            break
                    else:
                        # redistribute on network
                        self.network.distribute_txn(txn, self.node)
    ```

### Verification of Pay to Pub Key Hash (P2PKH)}

In the Bitcoin implementation, the `script\_pub\_key` is written in an interpretive language called `Script`. It works on a series of upcode and a stack machine.

Usually, the scriptPubKey and scriptSig are something like this:

```
scriptPubKey: OP_DUP OP_HASH160 <pubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
scriptSig: <digital-signature> <pubKey>
```
We assumed our scriptPubKey to be only `<pubKeyHash>` and the rest remains the same.

Here's how we implement it to verify.

```python
class ScriptInterpreter:
    @staticmethod
    def verify_pay_to_pubkey_hash(script_signature, pub_key_script, message):
        signature = script_signature[:128]
        pub_key = script_signature[128:]

        pub_hash160 = utils.hash160(pub_key)
        if not (pub_hash160.strip() == pub_key_script.strip()):
            return False

        vk = VerifyingKey.from_string(bytearray.fromhex(pub_key),
                            curve=ecdsa.SECP256k1)
        return vk.verify(bytearray.fromhex(signature), str.encode(message))
```
### Relevance of Network
Network in a peer-2-peer decentralized currency should not be something that knows all nodes. But for the 'simplicity in simulation,' we assume Network to be in a star topology. Which can with simple ease extended to a ring topology as it usually is. Our Network consists of these static methods. That any node can lock and use.

```python
class Network:
    nodes  = [] # star topology (can be extended to ring)
    address_map = {} # pub_key_hash -> index in nodes

    @staticmethod
    def add_node(n):
        pass

    @staticmethod
    def create_nodes(num_nodes):
        pass

    @staticmethod
    def get_blockchain():
        pass

    @staticmethod
    def distribute_txn(txn, src_node):
        pass

    @staticmethod
    def distribute_block(block, src_node):
        pass
```
## Graphs

### Arity of Merkle Tree vs Time Taken by transaction

\includesvg[]{first.svg}

\noindent We can see from the graph above that the merkle root has very little effect on the time taken to perform the transactions. This is mainly because most of the time is spent in message propagation and mining, not calculating the merkle root of the block.

### Time Taken by transaction vs Number of Nodes

\includesvg[]{last.svg}

We can see from the above graph that the time taken to complete the transactions has little effect of the number of nodes too. The time taken increases with the number of nodes because number of message to be passed increases. On the other hand, time taken should decrease with increasing number of nodes because the number of miners increases. We see a little increment in the time taken with increasing number of nodes.

## How To Run
Run the following command to execute a demo blockchain network:

> python3 main.py


## Sample Code output
### Nodes after Genesis Block addition
```

 ##########---------- Node ----------##########
 [@] Private Key : 7070ffdae5897a54d2124914587caad3b6e1648f2e5eacd0ae2d8eeb25bf0a0b
 [@] Public Key : 32f0cebd6f98e066648c0e1d92c5a5de64705292aa03ba81f6aa6184f9cc83bf222dfae4
 8d5ce5b56cba07c538efba84f82be699824f1678596b0009f1ed8c5a
 [@] Pub Key Hash : dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c
 [@] Blockchain
9 -> 9 -> {'99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e37b100>}}
     None
 ##########---------- Node ----------##########
 [@] Private Key : 20b2965794b6d2e3bb0da6200b663fa565e7459853a396c885933822520ec12f
 [@] Public Key : eef5bc528f92a677cf25b2a574858a8260ee27ed8ff9134a99c8f54f629c74e21b1b19
 ca93bd181ef7e9922295f576f7ad0111b29cd68009812ce081c74e5a31
 [@] Pub Key Hash : f10c89ae22a31d7e95abdab913e2d1eee1fe0092
 [@] Blockchain
9 -> 9 -> {'99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e37b370>}}
     None
 ##########---------- Node ----------##########
 [@] Private Key : 5c68085c1ae7b08e23c2dc16d1e08dd9ba42e5c5f765b75ca42ef4e67c60af34
 [@] Public Key : 03501620f33d91a4796a9064f44bd7385475b224880c56233e28ba987c6900981c7c9de
 88de22ccbeef5c7a36fa2da407c63bdf14cf2f42b8aafb46dbbdaaa41
 [@] Pub Key Hash : 47a4352e855f1eb66d2a1edaf873428545035b17
 [@] Blockchain
9 -> 9 -> {'99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e37b730>}}
     None

```
### Transactions Created
```
[****************------ CREATING-TXN-----************]
[#] From:  dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c
[#] To:  f10c89ae22a31d7e95abdab913e2d1eee1fe0092
[+] Amount:  10
[****************------ CREATING-TXN-----************]
[#] From:  dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c
[#] To:  47a4352e855f1eb66d2a1edaf873428545035b17
[+] Amount:  10
T:  Thread-1 [CREATED] [TXN]
T:  Thread-1 [CREATED] [TXN]
```
### Nodes receive Transaction
```
T:  Thread-1 [RECEIVED] [TXN]
T:  Thread-1 [RECEIVED] [TXN]
T:  Thread-3 [RECEIVED] [TXN]
T:  Thread-2 [RECEIVED] [TXN]
T:  Thread-3 [RECEIVED] [TXN]
T:  Thread-2 [RECEIVED] [TXN]

```
### Node 1 creates Block
```
 ##########---------- Block ----------##########
 [@] Nonce : 36841
 [@] Hash : 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55
 [@] Prev Block Hash : 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f
 [@] Bits : 3
 [@] Merkle Root : 21931f86c91616da9528f15df4b3da43b879c0325eddfa29a80236c806f148a3
     ##########---------- TXN ----------##########
     [@] TXNID : 3371529ac1139726e934c9c1ee530ac6f6d3e458f5f90a5a40d23284d4ffa8c5
         #####----- Input_txn -----#####
         [@] TXNID : 0000000000000000000000000000000000000000000000000000000000000000
         [@] Vout : -1
         [@] Sig Script : bbe841999d597959e8ecaeffd4370fc986cad10e2db82db103f4
         7b39435557caa809c8f471fadce5d93073ec43952aa9aca76bb5e992a6f0416d142e23cac18732f
         0cebd6f98e066648c0e1d92c5a5de64705292aa03ba81f6aa6184f9cc83bf222dfae48d5ce5b56c
         ba07c538efba84f82be699824f1678596b0009f1ed8c5a

         #####----- Output TXN -----#####
         [@] Amount : 50
         [@] Script Pub Key : dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c


     ##########---------- TXN ----------##########
     [@] TXNID : 22eac2119f1fb2ab42f89b4984dc11d63e9f2fdfc5f0133d7d1de5f3ed93f6b9
         #####----- Input_txn -----#####
         [@] TXNID : 99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548
         [@] Vout : 0
         [@] Sig Script : 40ad21a23b1757c92e8ccf6d480435494be144faa87f9c883b3c1100fa2d876e4c1946
         8e465237dfe5faf3ef552d25df69c56382d1a2582e9588a973e6f9b34632f0cebd6f98e066648c0
         e1d92c5a5de64705292aa03ba81f6aa6184f9cc83bf222dfae48d5ce5b56cba07c538efba84f82b
         e699824f1678596b0009f1ed8c5a

         #####----- Output TXN -----#####
         [@] Amount : 10
         [@] Script Pub Key : f10c89ae22a31d7e95abdab913e2d1eee1fe0092

         #####----- Output TXN -----#####
         [@] Amount : 40
         [@] Script Pub Key : dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c


     ##########---------- TXN ----------##########
     [@] TXNID : 8d1da70aaa10685f9b0776a4b519a4f953e15cd720e748246877b2c21ecad641
         #####----- Input_txn -----#####
         [@] TXNID : 99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548
         [@] Vout : 0
         [@] Sig Script : f82fd437bf99fa92c9b1b1037660a00e5e5e6d03839a3a112863fcb0271410352aa255
         ec5d3092dd9830bd610ba743b090a699b195a9bdc0d8f0bca5d347cb8a32f0cebd6f98e066648c0e
         1d92c5a5de64705292aa03ba81f6aa6184f9cc83bf222dfae48d5ce5b56cba07c538efba84f82be6
         99824f1678596b0009f1ed8c5a

         #####----- Output TXN -----#####
         [@] Amount : 10
         [@] Script Pub Key : 47a4352e855f1eb66d2a1edaf873428545035b17

         #####----- Output TXN -----#####
         [@] Amount : 40
         [@] Script Pub Key : dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c



```
### Threads receive block
```
T:  Thread-1 [MINED] [BLOCK]
T:  Thread-3 [RECEIVED] [BLOCK]
T:  Thread-2 [RECEIVED] [BLOCK]
```
### Final Nodes state
```
 ##########---------- Node ----------##########
 [@] Private Key : 7070ffdae5897a54d2124914587caad3b6e1648f2e5eacd0ae2d8eeb25bf0a0b
 [@] Public Key : 32f0cebd6f98e066648c0e1d92c5a5de64705292aa03ba81f6aa6184f9cc83bf222d
 fae48d5ce5b56cba07c538efba84f82be699824f1678596b0009f1ed8c5a
 [@] Pub Key Hash : dc8b202ad8ecadffafc7d1aa5aa4b696bdaa437c
 [@] Blockchain
9 -> 9 -> {'99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548': {'vout': [], 'txn': <transaction.TXN object at 0x7fa59e37b100>}}
3 -> 3 -> {'3371529ac1139726e934c9c1ee530ac6f6d3e458f5f90a5a40d23284d4ffa8c5': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e384d00>}}
2 -> 2 -> {'22eac2119f1fb2ab42f89b4984dc11d63e9f2fdfc5f0133d7d1de5f3ed93f6b9': {'vout': [1], 'txn': <transaction.TXN object at 0x7fa59e3846d0>}}
8 -> d -> {'8d1da70aaa10685f9b0776a4b519a4f953e15cd720e748246877b2c21ecad641': {'vout': [1], 'txn': <transaction.TXN object at 0x7fa59e384280>}}
c -> 0 -> {'c0583a7c8b452431e7325fc89bbcf71b45d371e0703dbcaaf0d932f6994f2b51': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e38b640>}}
7 -> 3 -> {'731f1e1b47aae77f6af664dd0dcf8cd86092fd3e3a5bdc767ac28e0bce1ccb51': {'vout': [0, 1], 'txn': <transaction.TXN object at 0x7fa59e38b220>}}
b -> e -> {'be40b74b74987db30c5bd7ccfef438db8916ecf41c6c169793dbb615b575ed31': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e395220>}}
f -> 9 -> {'f953022d66559099b0a6273bed8264d31eb2d17c31ed4755ef4d2981c4abf329': {'vout': [0, 1], 'txn': <transaction.TXN object at 0x7fa59e395a00>}}
     None
 p: 0000000000000000000000000000000000000000000000000000000000000000 h: 0 id: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f child: -> 
    [ p: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f h: 1 id: 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55 child: -> 
        [ p: 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55 h: 2 id: 0000fee2b5d27728dd0f1059fed245cbcf5679f43bc1dda3c8f3e74bbe7ae566 child: -> 
            [ p: 0000fee2b5d27728dd0f1059fed245cbcf5679f43bc1dda3c8f3e74bbe7ae566 h: 3 id: 000090b4c68274236560f4ce15b53ad6a6de5c7e3631513a5ccc210008e3116c child: -> 
                []]]]

 ##########---------- Node ----------##########
 [@] Private Key : 20b2965794b6d2e3bb0da6200b663fa565e7459853a396c885933822520ec12f
 [@] Public Key : eef5bc528f92a677cf25b2a574858a8260ee27ed8ff9134a99c8f54f629c74e21b1b
 19ca93bd181ef7e9922295f576f7ad0111b29cd68009812ce081c74e5a31
 [@] Pub Key Hash : f10c89ae22a31d7e95abdab913e2d1eee1fe0092
 [@] Blockchain
9 -> 9 -> {'99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548': {'vout': [], 'txn': <transaction.TXN object at 0x7fa59e37b370>}}
3 -> 3 -> {'3371529ac1139726e934c9c1ee530ac6f6d3e458f5f90a5a40d23284d4ffa8c5': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e384190>}}
2 -> 2 -> {'22eac2119f1fb2ab42f89b4984dc11d63e9f2fdfc5f0133d7d1de5f3ed93f6b9': {'vout': [1], 'txn': <transaction.TXN object at 0x7fa59e384730>}}
8 -> d -> {'8d1da70aaa10685f9b0776a4b519a4f953e15cd720e748246877b2c21ecad641': {'vout': [1], 'txn': <transaction.TXN object at 0x7fa59e384490>}}
c -> 0 -> {'c0583a7c8b452431e7325fc89bbcf71b45d371e0703dbcaaf0d932f6994f2b51': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e384be0>}}
7 -> 3 -> {'731f1e1b47aae77f6af664dd0dcf8cd86092fd3e3a5bdc767ac28e0bce1ccb51': {'vout': [0, 1], 'txn': <transaction.TXN object at 0x7fa59e38d340>}}
b -> e -> {'be40b74b74987db30c5bd7ccfef438db8916ecf41c6c169793dbb615b575ed31': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e38ddf0>}}
f -> 9 -> {'f953022d66559099b0a6273bed8264d31eb2d17c31ed4755ef4d2981c4abf329': {'vout': [0, 1], 'txn': <transaction.TXN object at 0x7fa59e38db80>}}
     None
 p: 0000000000000000000000000000000000000000000000000000000000000000 h: 0 id: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f child: -> 
    [ p: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f h: 1 id: 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55 child: -> 
        [ p: 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55 h: 2 id: 0000fee2b5d27728dd0f1059fed245cbcf5679f43bc1dda3c8f3e74bbe7ae566 child: -> 
            [ p: 0000fee2b5d27728dd0f1059fed245cbcf5679f43bc1dda3c8f3e74bbe7ae566 h: 3 id: 000090b4c68274236560f4ce15b53ad6a6de5c7e3631513a5ccc210008e3116c child: -> 
                []]]]

 ##########---------- Node ----------##########
 [@] Private Key : 5c68085c1ae7b08e23c2dc16d1e08dd9ba42e5c5f765b75ca42ef4e67c60af34
 [@] Public Key : 03501620f33d91a4796a9064f44bd7385475b224880c56233e28ba987c6900981c7c9
 de88de22ccbeef5c7a36fa2da407c63bdf14cf2f42b8aafb46dbbdaaa41
 [@] Pub Key Hash : 47a4352e855f1eb66d2a1edaf873428545035b17
 [@] Blockchain
9 -> 9 -> {'99261eb646696af903700b6126056eac289ed2e7cd7648572de8219544837548': {'vout': [], 'txn': <transaction.TXN object at 0x7fa59e37b730>}}
3 -> 3 -> {'3371529ac1139726e934c9c1ee530ac6f6d3e458f5f90a5a40d23284d4ffa8c5': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e38b6d0>}}
2 -> 2 -> {'22eac2119f1fb2ab42f89b4984dc11d63e9f2fdfc5f0133d7d1de5f3ed93f6b9': {'vout': [1], 'txn': <transaction.TXN object at 0x7fa59e38b7f0>}}
8 -> d -> {'8d1da70aaa10685f9b0776a4b519a4f953e15cd720e748246877b2c21ecad641': {'vout': [1], 'txn': <transaction.TXN object at 0x7fa59e38b970>}}
c -> 0 -> {'c0583a7c8b452431e7325fc89bbcf71b45d371e0703dbcaaf0d932f6994f2b51': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e384eb0>}}
7 -> 3 -> {'731f1e1b47aae77f6af664dd0dcf8cd86092fd3e3a5bdc767ac28e0bce1ccb51': {'vout': [0, 1], 'txn': <transaction.TXN object at 0x7fa59e384d60>}}
b -> e -> {'be40b74b74987db30c5bd7ccfef438db8916ecf41c6c169793dbb615b575ed31': {'vout': [0], 'txn': <transaction.TXN object at 0x7fa59e38dee0>}}
f -> 9 -> {'f953022d66559099b0a6273bed8264d31eb2d17c31ed4755ef4d2981c4abf329': {'vout': [0, 1], 'txn': <transaction.TXN object at 0x7fa59e38dca0>}}
     None
 p: 0000000000000000000000000000000000000000000000000000000000000000 h: 0 id: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f child: -> 
    [ p: 000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f h: 1 id: 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55 child: -> 
        [ p: 0000450737917e2d614173fe1e8d866507411c75c797c38355aa342675388b55 h: 2 id: 0000fee2b5d27728dd0f1059fed245cbcf5679f43bc1dda3c8f3e74bbe7ae566 child: -> 
            [ p: 0000fee2b5d27728dd0f1059fed245cbcf5679f43bc1dda3c8f3e74bbe7ae566 h: 3 id: 000090b4c68274236560f4ce15b53ad6a6de5c7e3631513a5ccc210008e3116c child: -> 
                []]]]

```

## References
- [Bitcoin Developer Reference](https://developer.bitcoin.org/index.html)
- [Bitcoin White Paper](https://bitcoin.org/bitcoin.pdf)
- [Bitcoin Wiki Page](https://en.bitcoin.it/wiki/Main_Page)

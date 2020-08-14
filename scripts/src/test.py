import threading

from network import Network
import node
import time

def run_thread(n):
    while True:
        n.start_mining()


def main():
    Network.create_nodes(num_nodes=5)
    genesis_block = node.Node.create_genesis_block(Network.nodes[0].keys)
    genesis_block.print()
    # print("gen-txn-id: ", genesis_block.txns[0].txnid)
    Network.nodes[0].coin_recieved_txnid((genesis_block.txns[0].txnid, 0))

    # """Bitcoin doc: genesis block is almost always hardcoded into the software of
    # the applications that utilize its block chain."""

    for i, n in enumerate(Network.nodes):
        Network.address_map[n.pub_key_hash] = i
        ret = n.save_genesis_block(genesis_block.create_copy())
        if not ret:
            print("[*] Can't add gen block") 

    for n in Network.nodes:
        n.print()

    threads = []
    for i in range(len(Network.nodes)):
        threads.append(threading.Thread(target=run_thread, args=(Network.nodes[i], )))

    for t in threads:
        t.start()

    # # # here will add some testing txns by the main threads
    lock = threading.Lock()
    # print("[Address map]", Network.address_map)

    def make_txn(from_i, to_i, amount):
        print("[****************------ CREATING-TXN-----************]")
        Network.nodes[from_i].messages.append(("new_txn", (Network.nodes[to_i].pub_key_hash, amount)))
        print("[#] From: ", Network.nodes[from_i].pub_key_hash)
        print("[#] To: ", Network.nodes[to_i].pub_key_hash)
        print("[+] Amount: ", amount)

    with lock:
        make_txn(0, 1, 10)
        make_txn(0, 2, 10)
    
    time.sleep(20)
    with lock:
        make_txn(1, 2, 5)
        make_txn(2, 0, 5)

    # Network.nodes[0].create_txn(Network.address_map[1], 10)

    time.sleep(50)


    print("[#] After transactions all over")
    for n in Network.nodes:
        n.print()
        print(n)

    # for t in threads:
    #     t.join()

    # all threads finish their work

if __name__ == '__main__':
    main()


import threading

from network import Network
import node

def run_thread(worker, lock):
    worker.start_process(lock)

def main():
    Network.create_nodes(num_nodes=2)
    genesis_block = node.Node.create_genesis_block(Network.nodes[0].keys)

    """Bitcoin doc: genesis block is almost always hardcoded into the software of
    the applications that utilize its block chain."""
    for n in Network.nodes:
        ret = n.save_genesis_block(genesis_block.create_copy())
        if not ret:
            print("[*] Can't add gen block") 

    for n in Network.nodes:
        print(n)

    # threads = []
    # for i in range(len(Network.nodes)):
    #     threads.append(threading.Thread(target=Network.nodes[i].start_mining, args=()))

    # for t in threads:
    #     t.start()

    # lock = threading.Lock()
    # with lock:
    #     for n in Network.nodes:
    #         print(n)

    # here will add some testing txns by the main threads

    # for t in threads:
    #     t.join()

    # all threads finish their work

if __name__ == '__main__':
    main()


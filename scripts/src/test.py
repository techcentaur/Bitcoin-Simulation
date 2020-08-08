import threading
from network import Network

def run_thread(worker, lock):
    worker.start_process(lock)

def main():
    Network.create_nodes(num_nodes=1)
    Network.nodes[0].create_genesis_block()
    
    threads = []
    for i in range(len(net.nodes)):
        threads.append(threading.Thread(target=net.nodes[i].start_mining, args=()))

    for t in threads:
        t.start()

    # here will add some testing txns by the main threads
    
    # for t in threads:
    #     t.join()

    # all threads finish their work

if __name__ == '__main__':
    main()
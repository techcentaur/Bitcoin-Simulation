import threading
import network

def run_thread(worker, lock):
    worker.start_process(lock)

def main():
    net = network.Network()
    net.create_nodes(num_nodes=4)
    net.nodes[0].create_genesis_block()
    threads = []
    for i in range(len(net.nodes)):
        threads.append(threading.Thread(target=net.nodes[i].start_mining, args=())

    for t in threads:
        t.start()

    # for t in threads:
    #     t.join()

    # all threads finish their work

if __name__ == '__main__':
    main()
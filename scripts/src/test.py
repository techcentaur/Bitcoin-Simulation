import threading
import network

def run_thread(worker, lock):
    worker.start_process(lock)

def main():
    net = network.Network()
    net.create_nodes(num_nodes=4)

    threads = []
    for n in range(len(net.nodes)):
        threads.append(threading.Thread(target=run_thread, args=(net.nodes[n], threading.Lock(),)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    # all threads finish their work

if __name__ == '__main__':
    main()
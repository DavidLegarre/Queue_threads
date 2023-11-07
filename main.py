from threading import Thread

from process import tokenCounter, worker_function

thread_number = 10


def main():
    threads = [Thread(target=worker_function, name=f"Thread_{i}", daemon=True) for i in range(thread_number)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    while not tokenCounter.event.is_set() and all((thread.is_alive() for thread in threads)):
        pass

    if tokenCounter.event.is_set():
        print("Token Limit exceeded")
    else:
        print("Everything went fine!")


if __name__ == '__main__':
    main()

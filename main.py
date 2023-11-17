from datetime import datetime
from queue import Queue
from threading import Thread

from src.data.data import agent, client
from src.gui.gui import run_app


def main():
    transcribe_queue = Queue()
    window_thread = Thread(target=run_app,
                           args=(transcribe_queue,),
                           daemon=True)
    conversation = client + agent
    sorted_conversation = sorted(conversation, key=lambda x: datetime.strptime(x[1], "%H:%M:%S"))

    for conversation in sorted_conversation:
        message_dict = {
            "speaker": conversation[0],
            "timestamp": conversation[1],
            "message": conversation[2],
        }
        transcribe_queue.put(message_dict)

    window_thread.start()
    window_thread.join()


if __name__ == '__main__':
    main()

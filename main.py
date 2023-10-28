# This is a sample Python script.
import threading
import uuid
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from queue import Queue

from process import process_transcriber_queue, process_audio_queue, process_classify_queue
from utils import NUM_AUDIO_THREADS, NUM_TRANSCRIBE_THREADS, NUM_CLASSIFY_THREADS
from utils import logger, NUM_AUDIOS

audio_queue = Queue()
transcriber_queue = Queue()
classify_queue = Queue()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    audios = [str(uuid.uuid4()) for _ in range(NUM_AUDIOS)]
    logger.debug("This is a debug message")
    logger.info("This is a info message")

    # Fill Queues
    for audio in audios:
        audio_queue.put(audio)

    audio_threads = [
        threading.Thread(target=process_audio_queue, args=(audio_queue, transcriber_queue),
                         name=f"audio_thread_{_}")
        for _ in range(NUM_AUDIO_THREADS)
    ]

    transcriber_threads = [
        threading.Thread(target=process_transcriber_queue, args=(transcriber_queue, classify_queue),
                         name=f"transcriber_thread_{_}")
        for _ in range(NUM_TRANSCRIBE_THREADS)
    ]

    classify_threads = [
        threading.Thread(target=process_classify_queue, args=(classify_queue,), name=f"classify_thread_{_}")
        for _ in range(NUM_CLASSIFY_THREADS)
    ]

    [thread.start() for thread in audio_threads]
    [thread.start() for thread in transcriber_threads]
    [thread.start() for thread in classify_threads]

    for thread in audio_threads:
        thread.join()
    for thread in transcriber_threads:
        thread.join()
    for thread in classify_threads:
        thread.join()

    logger.warning("All threads finished!")

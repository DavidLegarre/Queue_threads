import threading
import time
from queue import Queue, Empty

from utils import AUDIO_DELAY, NUM_AUDIO_THREADS, TRANSCRIBE_DELAY, NUM_TRANSCRIBE_THREADS, CLASSIFY_DELAY, \
    NUM_CLASSIFY_THREADS
from utils import logger, get_random_string, classify

audio_queue_finished = threading.Event()
audio_threads_count = 0
transcribers_finished = threading.Event()
transcribers_count = 0
classifiers_count = 0
lock = threading.Lock()
i = 1


def process_audio_queue(audio_queue: Queue, transcriber_queue: Queue):
    thread_name = threading.current_thread().name
    global audio_threads_count

    while not audio_queue.empty():
        audio = audio_queue.get()
        logger.info(f"Audio downloaded: {audio=}")
        audio = audio + ".mp3"
        time.sleep(AUDIO_DELAY)
        transcriber_queue.put(audio)

    audio_threads_count += 1
    logger.warning(f"Thread {thread_name} finished...")
    if audio_threads_count == NUM_AUDIO_THREADS:
        logger.warning(f"All audio threads finished")
        for _ in range(NUM_TRANSCRIBE_THREADS):
            transcriber_queue.put(None)


def process_transcriber_queue(transcriber_queue: Queue, classify_queue: Queue):
    thread_name = threading.current_thread().name
    global transcribers_count

    while True:
        audio_file = transcriber_queue.get()
        if audio_file is None:
            break
        logger.info(f"Transcribing file: {audio_file}")
        transcription = get_random_string(7)
        time.sleep(TRANSCRIBE_DELAY)
        logger.info(f"Finished transcribing audio {audio_file} as {transcription}")
        classify_queue.put(transcription)
    transcribers_count += 1
    logger.warning(f"Thread {thread_name} finished")
    if transcribers_count == NUM_TRANSCRIBE_THREADS:
        logger.warning(f"All transcriber threads finished")
        classify_queue.put(None)
        for _ in range(NUM_CLASSIFY_THREADS):
            classify_queue.put(None)


def process_classify_queue(classify_queue: Queue):
    thread_name = threading.current_thread().name
    global classifiers_count
    global i

    while True:
        transcription = classify_queue.get()
        if transcription is None:
            break
        logger.info(f"Classifying: {transcription}")
        category = classify()
        time.sleep(CLASSIFY_DELAY)
        logger.info(f"transcription '{transcription} classified as {category}'")
        with lock:
            with open("database.txt", "a") as f:
                f.write(f"{i}: {transcription} ------- {category} (written by {thread_name})\n")
            i += 1
    logger.warning(f"Classify queue empty, {thread_name} exiting...")
    classifiers_count += 1
    if classifiers_count == NUM_CLASSIFY_THREADS:
        logger.warning(f"All classifier threads finished")

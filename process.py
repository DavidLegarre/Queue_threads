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
i = 0


def process_audio_queue(audio_queue: Queue, transcriber_queue: Queue):
    thread_name = threading.current_thread().name
    global audio_threads_count
    while not audio_queue.empty():
        audio = audio_queue.get()
        logger.info(f"Downloading audio with id:{audio}")
        audio = audio + ".mp3"
        time.sleep(AUDIO_DELAY)
        logger.info(f"Audio Downloaded {audio}")
        transcriber_queue.put(audio)
        audio_queue.task_done()

    audio_threads_count += 1
    logger.warning(f"Audio queue empty, {thread_name} exiting...")
    if audio_threads_count == NUM_AUDIO_THREADS:
        logger.warning("All audio threads finished")
        audio_queue_finished.set()


def process_transcriber_queue(transcriber_queue: Queue, classify_queue: Queue):
    thread_name = threading.current_thread().name
    global transcribers_count
    while not (audio_queue_finished.is_set() and transcriber_queue.empty()):
        audio = transcriber_queue.get()
        logger.info(f"Transcribing audio {audio}")
        transcription = get_random_string(7)
        time.sleep(TRANSCRIBE_DELAY)
        logger.info(f"Finished transcribing audio {audio} as {transcription}")
        classify_queue.put(transcription)
        transcriber_queue.task_done()
    transcribers_count += 1
    logger.warning(f"Transcribe queue empty, {thread_name} exiting...")
    if transcribers_count == NUM_TRANSCRIBE_THREADS:
        logger.warning("All transcriber threads finished")
        transcribers_finished.set()


def process_classify_queue(classify_queue: Queue):
    thread_name = threading.current_thread().name
    global classifiers_count
    global i

    while not transcribers_finished.is_set():
        try:
            transcription = classify_queue.get_nowait()
            logger.info(f"classifying transcription: {transcription}")
            time.sleep(CLASSIFY_DELAY)
            category = classify()
            logger.info(f"transcription '{transcription} classified as {category}'")
            with lock:
                with open("database.txt", "a") as f:
                    f.write(f"{i}: {transcription} ------- {category} (written by {thread_name})\n")
                i += 1
        except Empty:
            continue
        finally:
            classify_queue.task_done()

        logger.warning(f"Classify queue empty, {thread_name} exiting...")
        classifiers_count += 1
        if classifiers_count == NUM_CLASSIFY_THREADS:
            logger.warning(f"All classifier threads finished")

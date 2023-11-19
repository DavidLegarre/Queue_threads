import sounddevice as sd


def callback(indata, frames, time, status):
    if status:
        print(status)


def capture_loopback():
    print("Capturing loopback audio... Press Ctrl+C to stop.")
    with sd.InputStream(callback=callback):
        try:
            sd.sleep(15)  # Adjust the sleep duration or use a different stopping condition
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    capture_loopback()

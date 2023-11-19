import pyaudio

def display_audio_devices():
    p = pyaudio.PyAudio()
    print("Available audio devices:")
    for i in range(p.get_device_count()):
        device_info = p.get_device_info_by_index(i)
        if 'VB-Audio' in device_info['name']:
            print(f"Device {i}: {device_info['name']}, {device_info['hostApi']}")

    p.terminate()

if __name__ == "__main__":
    display_audio_devices()

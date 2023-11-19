import wave

import pyaudio


FORMAT = pyaudio.paInt16
CHANNELS = 2  # Change to 1 if you want mono output
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 10  # You can set the duration you want to listen to the audio

def main():
    p = pyaudio.PyAudio()
    device_index = 18

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK,
                    input_device_index=device_index)
    print(f"Device index is: {device_index}")
    print("Listening...")

    frames = []
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Finished recording.")

    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save the recorded audio to a WAV file
    output_file = "output.wav"
    wf = wave.open(output_file, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print(f"Audio saved to '{output_file}'")

if __name__ == '__main__':
    main()

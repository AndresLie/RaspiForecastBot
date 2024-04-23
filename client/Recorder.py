import pyaudio
import audioop
import wave
import time

# Audio settings
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024  # Increased buffer size for better handling of audio data
THRESHOLD = 500  # audio levels not exceeding this value are considered silence
SILENCE_LIMIT = 2  # silence for more than 2 seconds stops recording

def Record():
    audio = pyaudio.PyAudio()

    # Adjust settings dynamically based on the environment
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    print("Recording... Adjust your microphone if needed.")
    frames = []
    last_sound_time = time.time()
    silence_threshold = 0.5  # More sensitive to silence detection

    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        rms = audioop.rms(data, 2)

        if rms > THRESHOLD:
            frames.append(data)
            last_sound_time = time.time()
        elif (time.time() - last_sound_time) > SILENCE_LIMIT:
            print("Finished recording.")
            break
        else:
            frames.append(data)  # Append silence frames to maintain continuity

    stream.stop_stream()
    stream.close()
    audio.terminate()

    save_recording(frames)

def save_recording(frames):
    wave_file = wave.open("recording.wav", 'wb')
    wave_file.setnchannels(CHANNELS)
    wave_file.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
    wave_file.setframerate(RATE)
    wave_file.writeframes(b''.join(frames))
    wave_file.close()
    print("Recording saved to 'recording.wav'")

if __name__ == '__main__':
    Record()

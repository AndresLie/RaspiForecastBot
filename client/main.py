import os
import asyncio
from eff_word_net.streams import SimpleMicStream
from eff_word_net.engine import HotwordDetector
from eff_word_net import samples_loc
from Recorder import Record
from ClientRequest import send_data
from Spinner import start_motor_thread, stop_motor_thread

# Setup hotword detector and microphone stream
hello_hw = HotwordDetector(
    hotword="mobile",
    reference_file=os.path.join(samples_loc, "mobile_ref.json"),
    threshold=0.955,
)

async def listen_and_process():
    mic_stream = SimpleMicStream()
    mic_stream.start_stream()
    print("Say 'Mobile'")
    skip_frames = 0  # Number of frames to skip after detection

    try:
        while True:
            if skip_frames > 0:
                mic_stream.getFrame()  # Get and discard frame
                skip_frames -= 1
                continue

            frame = mic_stream.getFrame()
            result = hello_hw.scoreFrame(frame)
            if result is None:
                continue
            if result["match"]:
                print("Wakeword uttered", result["confidence"])
                skip_frames = 10  # Set how many frames to skip after a detection

                start_motor_thread(0.003)
                await asyncio.get_event_loop().run_in_executor(None, Record)
                stop_motor_thread()
                
                await asyncio.get_event_loop().run_in_executor(None, send_data, "recording.wav")
                print("Ready for next command")

    except KeyboardInterrupt:
        print("Stopping...")

# Run the coroutine in the event loop
if __name__ == "__main__":
    asyncio.run(listen_and_process())

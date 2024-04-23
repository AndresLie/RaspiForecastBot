import os
from gtts import gTTS
import pygame

def TTS(text, lang):
    if lang == "chinese":
        lang = "zh-tw"

    tts = gTTS(text=text, lang=lang)
    tts.save("response.mp3")

    # Initialize pygame mixer
    pygame.mixer.init()
    
    # Load the MP3 file
    pygame.mixer.music.load("response.mp3")
    
    # Play the MP3 file
    pygame.mixer.music.play()

    # Wait for playback to finish
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    # Stop the music if it's still playing and clean up
    pygame.mixer.music.stop()
    pygame.mixer.quit()

# Example usage
# TTS("你好, 这是google的语音测试", "chinese")

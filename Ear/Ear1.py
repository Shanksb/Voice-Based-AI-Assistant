import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

def listen_and_transcribe():
    print("Loading AI model...")
    model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
    
    sample_rate = 16000
    duration = 5
    
    print("Listening... (Press Ctrl+C to stop)")
    while True:
        audio_chunk = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
        sd.wait()
        
        audio_data = np.squeeze(audio_chunk)
        
        segments, _ = model.transcribe(audio_data, beam_size=5)
        
        for segment in segments:
            text = segment.text.strip()
            if text:
                print(text)

if __name__ == "__main__":
    listen_and_transcribe()
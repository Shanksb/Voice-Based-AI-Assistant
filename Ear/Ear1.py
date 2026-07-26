import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel

def listen_and_transcribe():
    print("Loading AI model...")
    model = WhisperModel(
        "base.en",
        device="cpu",
        compute_type="float32",
        cpu_threads=8,
        )
    
    sample_rate = 16000
    duration = 8
    
    print("Listening... (Press Ctrl+C to stop)")
    try:
        while True:
            audio_chunk = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()
            
            audio_data = np.squeeze(audio_chunk)
            
            segments, _ = model.transcribe(audio_data, beam_size=5, vad_filter=True,
                                           language="en",
                                            temperature=0.0,
                                            initial_prompt="Hello, my name is Shashank. I am speaking English with a slight Indian accent."
                                            )
        
            for segment in segments:
                text = segment.text.strip()
                if text:
                    print(text)

    except KeyboardInterrupt:
        print("\nStopping the Ear. Goodbye!")    

if __name__ == "__main__":
    listen_and_transcribe()
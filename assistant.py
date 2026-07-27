import os
import sys
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from groq import Groq

API_KEY = "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"

if API_KEY == "PASTE_YOUR_ACTUAL_API_KEY_HERE" or API_KEY == "":
    print("\n🛑 ERROR: The Brain is missing its API Key!")
    print("Please go to console.groq.com, create a key, and paste it into line 12 of this script.")
    sys.exit()

client = Groq(api_key=API_KEY)

def think(user_input):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, witty, and concise AI assistant named Jarvis. Keep your answers short and conversational. Do not use markdown formatting in your responses."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7, 
    )
    
    return completion.choices[0].message.content

def listen_and_respond():
    print("Loading AI")

    ear_model = WhisperModel(
        "base.en",
        device="cpu",
        cpu_threads=8,
    )

    sample_rate = 16000
    duration = 10

    print("AI Online(Press Ctrl+C to stop)")
    try:
        while True:
            audio_chunk = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait()

            audio_data = np.squeeze(audio_chunk)

            segments, _ = ear_model.transcribe(audio_data, beam_size=5, vad_filter=True,
                                                language="en",
                                                temperature=0.0,
                                                initial_prompt="Hello, my name is Shashank. I am speaking English with a slight Indian accent."
                                                )

            full_transcription = ""
            for segment in segments:
                full_transcription += segment.text.strip() + " "

            full_transcription = full_transcription.strip()

            if full_transcription:
                print(f"\n You: {full_transcription}")
                print("Jarvis is thinking...")
                
                # Hand the text to the Groq API
                answer = think(full_transcription)
                
                print(f" Jarvis: {answer}")
                print("\nListening...") # Prompt the user that it's ready again

    except KeyboardInterrupt:
        print("\n\nShutting down Jarvis. Goodbye!")

if __name__ == "__main__":
    listen_and_respond()
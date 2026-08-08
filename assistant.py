import os
import sys
import sounddevice as sd
import numpy as np
from faster_whisper import WhisperModel
from groq import Groq
from dotenv import load_dotenv
import win32com.client 
from ddgs import DDGS 
import datetime

load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")

if API_KEY is None or API_KEY == "":
    print("\nERROR: The Brain is missing its API Key!")
    print("Please make sure you have a .env file with your GROQ_API_KEY set.")
    sys.exit()

client = Groq(api_key=API_KEY)

speaker = win32com.client.Dispatch("SAPI.SpVoice")
speaker.Rate = 2 

def speak(text):
    speaker.Speak(text)


def search_web(query):
    print(f"Jarvis is searching the web for: '{query}'...")
    try:
        if "news" in query.lower():
            results = DDGS().news(query, max_results=3)
        else:
            results = DDGS().text(query, max_results=3)
            
        if not results:
            print("Search returned empty.")
            return "No search results found."
        
        search_text = ""
        for res in results:
            title = res.get('title', '')
            body = res.get('body', '')
            search_text += f"- {title}: {body}\n"
        return search_text
        
    except Exception as e:
        print(f"SEARCH ERROR: {e}")
        return f"Search failed: {e}"

def think(user_input):
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    current_year = datetime.datetime.now().strftime("%Y")

    system_prompt = """You are a helpful, witty, and concise AI assistant named Jarvis. 
    Keep your answers short and conversational. Do not use markdown formatting.
    Today's date is {current_date}.
    
    CRITICAL RULE: If the user asks about current events, real-time data, weather, or something you don't know, you must reply EXACTLY with this format:
    SEARCH: [your search query]
    
    Do not add any other text if you are searching."""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.7, 
    )
    
    response = completion.choices[0].message.content.strip()

    if response.startswith("SEARCH:"):
        query = response.replace("SEARCH:", "").strip()

        search_results = search_web(query)

        messages.append({"role": "assistant", "content": response})
        messages.append({
            "role": "user", 
            "content": f"Here are the live search results:\n{search_results}\n\nBased ONLY on this information, answer my original question briefly."
        })
        
        messages[0]["content"] = "You are Jarvis. Answer the user using ONLY the search results provided. If the results contain news headlines, read them to the user naturally as if you are a news anchor. If the search results say 'Search failed', apologize."
        
        final_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            temperature=0.7,
        )
        return final_completion.choices[0].message.content.strip()
    return response

def listen_and_respond():
    print("Loading AI...")
    
    ear_model = WhisperModel("base.en", device="cpu", cpu_threads=8)
    
    sample_rate = 16000
    duration = 10
    
    print("AI Online (Press Ctrl+C to stop)")
    
    try:
        while True:
            audio_chunk = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='float32')
            sd.wait() 
            audio_data = np.squeeze(audio_chunk)
            
            segments, _ = ear_model.transcribe(
                audio_data, 
                beam_size=5, 
                vad_filter=True, 
                language="en", 
                temperature=0.0, 
                initial_prompt="Hello, my name is Shashank. I am speaking English with a slight Indian accent."
            )
            
            full_transcription = ""
            for segment in segments:
                full_transcription += segment.text.strip() + " "
            
            full_transcription = full_transcription.strip()
            
            if full_transcription:
                print(f"\nYou: {full_transcription}")
                print("Jarvis is thinking...")
                
                # Hand the text to the upgraded Brain
                answer = think(full_transcription)
                
                print(f"Jarvis: {answer}")
                speak(answer)
                
                print("\nListening...") 

    except KeyboardInterrupt:
        print("\n\nShutting down Jarvis. Goodbye!")


if __name__ == "__main__":
    listen_and_respond()
import os
import sys
from groq import Groq

API_KEY = "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"


if API_KEY == "PASTE_YOUR_ACTUAL_API_KEY_HERE" or API_KEY == "":
    print("\n🛑 ERROR: The Brain is missing its API Key!")
    print("Please go to console.groq.com, create a key, and paste it into line 7 of this script.")
    sys.exit() # This cleanly stops the program

client = Groq(api_key=API_KEY)

def think(user_input):
    print("Thinking...")
    
    # 3. SEND THE MESSAGE
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, witty, and concise AI assistant named Jarvis. Keep your answers short and conversational."
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=0.7, 
    )
    
    response = completion.choices[0].message.content
    return response

if __name__ == "__main__":
    test_question = "Hey Jarvis, what is the distance to the moon?"
    print(f"You asked: {test_question}")
    
    answer = think(test_question)
    
    print(f"\nJarvis says: {answer}")
import os
import sys
from groq import Groq
from dotenv import load_dotenv

# 1. SETUP: Load the hidden variables
load_dotenv()

# Grab the key from the .env file instead of hardcoding it here
API_KEY = os.getenv("GROQ_API_KEY")

if API_KEY is None or API_KEY == "":
    print("\n🛑 ERROR: The Brain is missing its API Key!")
    print("Please make sure you have a .env file with your GROQ_API_KEY set.")
    sys.exit() # This cleanly stops the program

# 2. WAKE UP THE BRAIN
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
    
    # 4. GET THE REPLY
    response = completion.choices[0].message.content
    return response

# 5. THE IGNITION SWITCH
if __name__ == "__main__":
    test_question = "Hey Jarvis, what is the distance to the moon?"
    print(f"You asked: {test_question}")
    
    answer = think(test_question)
    
    print(f"\nJarvis says: {answer}")
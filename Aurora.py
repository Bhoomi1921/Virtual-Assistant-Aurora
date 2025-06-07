import pyttsx3 
import speech_recognition as sr 
from datetime import datetime
import webbrowser
import requests
import json
import base64
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize APIs
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
SPOTIFY_REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI', 'http://example.com/callback')

# Initialize the text-to-speech engine
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("Sorry, there's a problem with the speech recognition service.")
            return None

def get_spotify_token():
    """Get access token from Spotify API"""
    auth_string = f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}"
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": f"Basic {auth_base64}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    
    response = requests.post(url, headers=headers, data=data)
    json_result = json.loads(response.content)
    return json_result["access_token"]

def search_spotify(query, search_type="track"):
    """Search for items on Spotify"""
    token = get_spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    url = f"https://api.spotify.com/v1/search?q={query}&type={search_type}&limit=1"
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def play_on_spotify(song_name):
    """Play a song on Spotify (requires Spotify app to be open)"""
    result = search_spotify(song_name)
    if result and 'tracks' in result and 'items' in result['tracks']:
        if len(result['tracks']['items']) > 0:
            track_uri = result['tracks']['items'][0]['uri']
            webbrowser.open(track_uri)
            return True
    return False

def ask_openai(prompt):
    """Get response from OpenAI's API"""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data
    )
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    return None

def handle_command(command):
    if 'time' in command:
        now = datetime.now()
        time_string = now.strftime("%H:%M:%S")
        speak(f"The current time is {time_string}")
    elif 'date' in command:
        today = datetime.today().date()
        date_string = today.strftime("%B %d, %Y")
        speak(f"Today's date is {date_string}")
    elif 'calculate' in command:
        try:
            expression = command.split('calculate', 1)[1].strip()
            result = eval(expression)
            speak(f"The result of {expression} is {result}")
        except Exception as e:
            speak(f"Sorry, I couldn't calculate that. Error: {e}")
    elif 'hello arora' in command or 'hi arora' in command.lower():
        speak("Hello! How can I assist you today?")
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye! Have a great day.")
        return False
    elif 'google' in command:
        speak("Opening Google")
        webbrowser.open_new_tab("https://www.google.com")
    elif 'youtube' in command:
        speak("Opening YouTube")
        webbrowser.open_new_tab("https://www.youtube.com")
    elif 'linkedin' in command:
        speak("Opening LinkedIn")
        webbrowser.open_new_tab("https://www.linkedin.com/feed/")
    elif 'open chat gpt' in command or 'open chatgpt' in command:
        speak("Opening ChatGPT")
        webbrowser.open_new_tab("https://chat.openai.com/")
    elif 'open copilot' in command:
        speak("Opening Copilot")
        webbrowser.open_new_tab("https://copilot.microsoft.com/")
    elif command.startswith("play"):
        try:
            song = ' '.join(command.split(" ")[1:])
            speak(f"Searching for {song} on Spotify")
            if play_on_spotify(song):
                speak(f"Playing {song}")
            else:
                speak(f"Sorry, I couldn't find {song} on Spotify")
        except Exception as e:
            speak(f"Sorry, I couldn't play that song. Error: {e}")
    elif 'what is' in command or 'who is' in command or 'explain' in command:
        response = ask_openai(command)
        if response:
            speak(response)
        else:
            speak("Sorry, I couldn't get an answer to that question.")
    else:
        # For any other command, ask OpenAI
        response = ask_openai(command)
        if response:
            speak(response)
        else:
            speak("Sorry, I don't understand that command.")
    return True

def main():
    speak("Hello, I am Aurora. How can I assist you today?")
    active = True
    while True:
        if active:
            command = listen()
            if command:
                command = command.lower()
                if 'aurora' in command:
                    speak("Yes, how can I assist you?")
                    active = True
                else:
                    active = handle_command(command)
        else:
            try:
                if 'arora' in listen().lower():
                    active = True
            except Exception as e:
                active = False

if __name__ == "__main__":
    main()
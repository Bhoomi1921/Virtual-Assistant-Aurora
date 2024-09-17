import pyttsx3 
import speech_recognition as sr 
from datetime import datetime
import webbrowser
import Music

# Initialize the text-to-speech engine
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
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
    elif 'hello' in command or 'hi' in command:
        speak("Hello! How can I assist you today?")
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye! Have a great day.")
        return False
    elif 'google' in command:
        speak("OK")
        webbrowser.open_new_tab("www.google.com")
        speak("Here it is")
    elif 'youtube' in command:
        speak("OK")
        webbrowser.open_new_tab("www.youtube.com")
        speak("Here it is")
    elif 'linkedin' in command:
        speak("OK")
        webbrowser.open_new_tab("https://www.linkedin.com/feed/")
        speak("Here it is")
    elif 'open chat gpt' in command:
        speak("OK")
        webbrowser.open_new_tab("https://chatgpt.com/")
        speak("here it is")
    elif 'open copilot' in command:
        speak("OK")
        webbrowser.open_new_tab("https://copilot.com/")
        speak("here it is")
   
    elif command.startswith("play"):
        try:
            song = command.split(" ")[1]
            link = Music.music[song]
            webbrowser.open_new_tab(link)
            speak("here it is")
        except Exception as e:
            speak(f"Sorry I can not play that song {e}")
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


import speech_recognition as sr
import webbrowser
import pyttsx3
import musiclibrary
import requests
from google import genai
import time
# from gtts import gTTS
# import pygame
# import os

recognizer = sr.Recognizer()
newsapi = " "

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 180)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(str(text[:300]))
    engine.runAndWait()
    engine.stop()

# def speak(text):
#     tts = gTTS(text)
#     tts.save('temp.mp3')

#     # initialize pygame mixer
#     pygame.mixer.init()

#     # load the mp3 file
#     pygame.mixer.music.load('temp.mp3')

#     # play the mp3 file
#     pygame.mixer.music.play()

#     # keep the program running until the music stops playing
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

#     pygame.mixer.music.unload()
#     os.remove("temp.mp3")


def aiprocess(command):
    client = genai.Client(
    api_key=" "
    )

# Generate response
    response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=f"""
    You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Assistant.

    User: {command}
    """
    )
    
    return(response.text)
      
def processcommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
        speak("opening google")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        speak("opening facebook")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        speak("opening youtube")
    elif "open crex" in c.lower():
        webbrowser.open("https://crex.com")
        speak("opening crex")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
        speak("opening linkedin")
    elif c.lower().startswith("play"):
        song = c.lower().replace("play","").strip()
        link = musiclibrary.music[song]
        webbrowser.open(link)
    
    elif "news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code==200:
            # parse the JSON response
            data = r.json()

            # extract the articles
            articles = data.get('articles' , [])

            # print the headlines
            for article in articles:
                speak(article['title'])

    else:
        # let openAI handle the request
        output = aiprocess(c)
        print(output)
        speak(output[:300])
           

if __name__ == "__main__":
    speak("Initilalizing Jarvis.......")
    while True:
        # listen for the wake word "jarvis"
        # obtain audio from the microphone

        r = sr.Recognizer()
        
        print("recognizing....") 
        try:
            with sr.Microphone() as source:
                print("listening.....")
                audio = r.listen(source, timeout=3, phrase_time_limit=3)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("yes")
                time.sleep(1)
                
                
                # listen for command
                with sr.Microphone() as source:
                    print("jarvis active...")
                    audio = r.listen(source, timeout=3, phrase_time_limit=3)
                    command = r.recognize_google(audio)

                    processcommand(command)
                    time.sleep(2)
            
                
        except Exception as e:
            print("Error; {0}".format(e))
        
    
